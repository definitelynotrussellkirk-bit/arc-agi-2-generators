# ARC Additional Puzzle Bank — 21 Puzzles (Set 19)

This nineteenth pack continues the numbering with **`E127–E133`**, **`M127–M133`**, and **`H127–H133`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
slide_until_contact(board, cells, direction)
```

Intuition: move a connected shape as a rigid object in one direction until the **next** step would hit a wall, blocker, or border. It is used directly in **E127**, **M127**, and **H127**.

Design goals for this set:

- easy: rigid translation, rectangle completion, segment filling, guide reflection, frequency bars, checker filling, and selector-based extraction

- medium: independent lane motion, component packing, command-driven transforms, nearest-seed filling, depth recoloring, dihedral matching, and transform analogy

- hard: commanded room slides, obstacle-aware shortest-path filling, template mosaics, transformed overlaps, hole-count ranking, phase-composed tiling, and joint color+geometry analogy

## E127 — Slide to Dock
**Difficulty:** easy
**Train pairs:** 4
**Skills:** translation, contact stopping, same-size movement
**Suggested staged path:** First identify the fixed dock stripe. Then ignore everything except the moving colored object and ask how far it can shift right before the next step would hit the dock.

**Train 1 — input**
```text
000000090
040000090
040000090
044000090
000000090
000000090
```

**Train 1 — output**
```text
000000090
000004090
000004090
000004490
000000090
000000090
```

**Train 2 — input**
```text
0000000090
0000000090
0020000090
0222000090
0020000090
0000000090
0000000090
```

**Train 2 — output**
```text
0000000090
0000000090
0000002090
0000022290
0000002090
0000000090
0000000090
```

**Train 3 — input**
```text
00000000090
00770000090
00077000090
00000000090
00000000090
00000000090
```

**Train 3 — output**
```text
00000000090
00000077090
00000007790
00000000090
00000000090
00000000090
```

**Train 4 — input**
```text
000000090
000000090
000000090
033300090
003000090
003000090
000000090
```

**Train 4 — output**
```text
000000090
000000090
000000090
000033390
000003090
000003090
000000090
```

**Test — input**
```text
0000000090
0000000090
0660000090
0600000090
0000000090
0000000090
```

**Test — output**
```text
0000000090
0000000090
0000006690
0000006090
0000000090
0000000090
```

**Written solution**

There is a single colored object and a full-height dock stripe of 9s near the right side. Move the whole object right as one rigid shape until another step would collide with the dock. Keep the dock unchanged.

**Reference program**
```python
def rule_e127(g):
    h,w=size(g)
    dock_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    obj_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,9)]
    obj_color=next(g[r][c] for r,c in obj_cells)
    new_cells=slide_until_contact(g, obj_cells, (0,1))
    out=blank(h,w,0)
    for r,c in dock_cells:
        out[r][c]=9
    for r,c in new_cells:
        out[r][c]=obj_color
    return out
```

## E128 — Rectangle from Four Corners
**Difficulty:** easy
**Train pairs:** 4
**Skills:** bounding box, corner detection, same-size fill
**Suggested staged path:** Treat the four nonzero cells as markers, not as the final object. Their bounding box tells you the rectangle that must be painted.

**Train 1 — input**
```text
00000000
06000600
00000000
00000000
06000600
00000000
00000000
```

**Train 1 — output**
```text
00000000
06666600
06666600
06666600
06666600
00000000
00000000
```

**Train 2 — input**
```text
000000000
000000000
000300030
000000000
000000000
000000000
000300030
000000000
```

**Train 2 — output**
```text
000000000
000000000
000333330
000333330
000333330
000333330
000333330
000000000
```

**Train 3 — input**
```text
0000000000
0000700070
0000000000
0000000000
0000700070
0000000000
```

**Train 3 — output**
```text
0000000000
0000777770
0000777770
0000777770
0000777770
0000000000
```

**Train 4 — input**
```text
000000000
000000000
000000000
020020000
000000000
000000000
000000000
020020000
000000000
```

**Train 4 — output**
```text
000000000
000000000
000000000
022220000
022220000
022220000
022220000
022220000
000000000
```

**Test — input**
```text
0000000000
0000000000
0040000400
0000000000
0000000000
0040000400
0000000000
```

**Test — output**
```text
0000000000
0000000000
0044444400
0044444400
0044444400
0044444400
0000000000
```

**Written solution**

The input gives the four corners of a rectangle in one color. Fill every cell inside that bounding box, including the border, with the same color.

**Reference program**
```python
def rule_e128(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    color=next(v for row in g for v in row if v!=0)
    r0,c0,r1,c1=bbox(cells)
    out=clone(g)
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=color
    return out
```

## E129 — Complete the Segments
**Difficulty:** easy
**Train pairs:** 4
**Skills:** endpoint detection, horizontal/vertical filling, multi-color local logic
**Suggested staged path:** For each color separately, locate the two aligned endpoints. Then fill the cells between them instead of treating the endpoints as isolated dots.

**Train 1 — input**
```text
000000000
040004000
000000000
000000020
000000000
000000020
000000000
```

**Train 1 — output**
```text
000000000
044444000
000000000
000000020
000000020
000000020
000000000
```

**Train 2 — input**
```text
00000000
00000000
00300000
00000000
00000000
00006060
00300000
00000000
```

**Train 2 — output**
```text
00000000
00000000
00300000
00300000
00300000
00306660
00300000
00000000
```

**Train 3 — input**
```text
0000000000
0000000700
0000000000
0500500000
0000000700
0000000000
```

**Train 3 — output**
```text
0000000000
0000000700
0000000700
0555500700
0000000700
0000000000
```

**Train 4 — input**
```text
00000000000
00000000030
00000000000
00000000000
00000000030
00800000800
00000000000
```

**Train 4 — output**
```text
00000000000
00000000030
00000000030
00000000030
00000000030
00888888800
00000000000
```

**Test — input**
```text
0000000000
0000000070
0000000000
0004040000
0000000070
0000000000
0200000200
0000000000
```

**Test — output**
```text
0000000000
0000000070
0000000070
0004440070
0000000070
0000000000
0222222200
0000000000
```

**Written solution**

Each color appears exactly twice and the two cells are aligned horizontally or vertically. Fill the straight segment joining each pair, preserving the color.

**Reference program**
```python
def rule_e129(g):
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    out=clone(g)
    for color,cells in pos.items():
        if len(cells)==2:
            for r,c in fill_line_between(cells[0], cells[1]):
                out[r][c]=color
    return out
```

## E130 — Reflect Across the Guide
**Difficulty:** easy
**Train pairs:** 4
**Skills:** reflection, axis detection, crop output
**Suggested staged path:** Find the all-5 guide line first. Then look only at the motif on one side and reflect it across that line, ignoring the original absolute padding.

**Train 1 — input**
```text
00000500000
00000500000
04400500000
04000500000
00000500000
00000500000
00000500000
```

**Train 1 — output**
```text
44
04
```

**Train 2 — input**
```text
000000000
000600000
000600000
000660000
555555555
000000000
000000000
000000000
000000000
```

**Train 2 — output**
```text
66
60
60
```

**Train 3 — input**
```text
000000050000
000000050000
000000050000
022000050000
002200050000
000000050000
000000050000
000000050000
```

**Train 3 — output**
```text
022
220
```

**Train 4 — input**
```text
0000000000
0000080000
0000088800
0000000000
0000000000
0000000000
5555555555
0000000000
0000000000
0000000000
```

**Train 4 — output**
```text
888
800
```

**Test — input**
```text
00005000000
00005000000
77705000000
07005000000
07005000000
00005000000
00005000000
```

**Test — output**
```text
777
070
070
```

**Written solution**

A full row or full column of 5s is the mirror axis. Reflect the colored motif across that guide and output only the reflected motif, cropped to its bounding box.

**Reference program**
```python
def rule_e130(g):
    h,w=size(g)
    # detect guide
    guide_row=None; guide_col=None
    for r in range(h):
        if all(g[r][c]==5 for c in range(w)):
            guide_row=r; break
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            guide_col=c; break
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    color=next(g[r][c] for r,c in cells)
    if guide_col is not None:
        refl=reflect_across_vertical(cells, guide_col)
    else:
        refl=reflect_across_horizontal(cells, guide_row)
    # place in crop
    r0,c0,r1,c1=bbox(refl)
    out=blank(r1-r0+1,c1-c0+1,0)
    for r,c in refl:
        out[r-r0][c-c0]=color
    return out
```

## E131 — Frequency-Sorted Color Bar
**Difficulty:** easy
**Train pairs:** 4
**Skills:** counting, sorting, variable-size output
**Suggested staged path:** Forget the exact positions of the colored dots. Count how many times each color occurs, then turn those counts into an ordered strip.

**Train 1 — input**
```text
0000000000
0200200200
0000000000
0040040070
0000000000
0000000000
0000000000
```

**Train 1 — output**
```text
222447
```

**Train 2 — input**
```text
060060060
000000000
006003003
000000000
080080000
000000000
000000000
```

**Train 2 — output**
```text
66663388
```

**Train 3 — input**
```text
0000000000
0500200200
0000000000
0020070070
0000000000
0000000000
0000000000
0000000000
```

**Train 3 — output**
```text
222775
```

**Train 4 — input**
```text
04004004000
00000000000
00400900200
00000000000
02000000000
00000000000
00000000000
```

**Train 4 — output**
```text
4444229
```

**Test — input**
```text
0300300800
0000000000
0080080060
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — output**
```text
888336
```

**Written solution**

Count every nonzero color. Build a single output row by repeating each color as many times as it appears in the input, ordering the color blocks by descending frequency and breaking ties by smaller color value first.

**Reference program**
```python
def rule_e131(g):
    cnt=Counter(v for row in g for v in row if v!=0)
    seq=[]
    for color,count in sorted(cnt.items(), key=lambda kv:(-kv[1], kv[0])):
        seq.extend([color]*count)
    return [seq]
```

## E132 — Checker Fill Inside the Frame
**Difficulty:** easy
**Train pairs:** 4
**Skills:** frame detection, parity, palette marker use
**Suggested staged path:** Separate the frame color from the singleton palette marker. Once you know the interior box, paint only alternating cells starting from the interior's top-left corner.

**Train 1 — input**
```text
300000000
000000000
005555550
005000050
005000050
005000050
005555550
000000000
```

**Train 1 — output**
```text
300000000
000000000
005555550
005303050
005030350
005303050
005555550
000000000
```

**Train 2 — input**
```text
0000000000
0000777770
0000700070
0000700070
0000700070
0000777770
2000000000
```

**Train 2 — output**
```text
0000000000
0000777770
0000720270
0000702070
0000720270
0000777770
2000000000
```

**Train 3 — input**
```text
000000008
000000000
000000000
044444000
040004000
040004000
040004000
044444000
000000000
```

**Train 3 — output**
```text
000000008
000000000
000000000
044444000
048084000
040804000
048084000
044444000
000000000
```

**Train 4 — input**
```text
00000000000
00000000000
00066666660
00060000060
00060000060
00060000060
00066666660
20000000000
```

**Train 4 — output**
```text
00000000000
00000000000
00066666660
00062020260
00060202060
00062020260
00066666660
20000000000
```

**Test — input**
```text
000000004
088888800
080000800
080000800
080000800
088888800
000000000
```

**Test — output**
```text
000000004
088888800
084040800
080404800
084040800
088888800
000000000
```

**Written solution**

The most common nonzero color is a rectangular frame, and the lone other color is the paint color. Preserve the frame, then fill the interior with a checkerboard of the paint color on even parity cells and 0 on odd parity cells.

**Reference program**
```python
def rule_e132(g):
    cnt=Counter(v for row in g for v in row if v!=0)
    frame_color=max(cnt, key=lambda k: cnt[k])
    paint_color=min(cnt, key=lambda k: cnt[k])
    frame_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==frame_color]
    r0,c0,r1,c1=bbox(frame_cells)
    out=clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            out[r][c]=paint_color if ((r-(r0+1)) + (c-(c0+1)))%2==0 else 0
    return out
```

## E133 — Select the Marked Motif
**Difficulty:** easy
**Train pairs:** 4
**Skills:** selection by position, crop output, panel parsing
**Suggested staged path:** Use the selector cell in the header to decide which of the three motif panels matters. Then ignore the other panels entirely.

**Train 1 — input**
```text
0010000000000
0000000000000
0040070002200
0444070000200
0040077700220
```

**Train 1 — output**
```text
040
444
040
```

**Train 2 — input**
```text
0000001000000
0000000000000
0303066608000
0030006008800
0303006000880
```

**Train 2 — output**
```text
666
060
060
```

**Train 3 — input**
```text
0000000000100
0000000000000
0500020200700
0500002007770
0555020200700
```

**Train 3 — output**
```text
070
777
070
```

**Train 4 — input**
```text
0000001000000
0000000000000
0880040003330
0080044000300
0088004400300
```

**Train 4 — output**
```text
400
440
044
```

**Test — input**
```text
0010000000000
0000000000000
0606002005000
0060022205500
0606002000550
```

**Test — output**
```text
606
060
606
```

**Written solution**

Three 3×3 motifs are shown, and a single selector cell in the top row points to one of them by column position. Output only the selected 3×3 motif.

**Reference program**
```python
def rule_e133(g):
    selector_col=next(c for c,v in enumerate(g[0]) if v!=0)
    if selector_col <4:
        st=1
    elif selector_col<8:
        st=5
    else:
        st=9
    return [row[st:st+3] for row in g[2:5]]
```

## M127 — Lane Docking
**Difficulty:** medium
**Train pairs:** 4
**Skills:** independent component motion, rigid translation, shared blocker geometry
**Suggested staged path:** Treat each lane separately so the board stops looking like one global problem. Inside each lane, slide the component right until the wall stops it.

**Train 1 — input**
```text
999999999999
920000000009
920000000009
922000000009
999999999999
904400000009
900440000009
900000000009
999999999999
900000000009
907700000009
900000000009
999999999999
```

**Train 1 — output**
```text
999999999999
900000000209
900000000209
900000000229
999999999999
900000004409
900000000449
900000000009
999999999999
900000000009
900000000779
900000000009
999999999999
```

**Train 2 — input**
```text
9999999999999
9030000000009
9333000000009
9030000000009
9999999999999
9000000000009
9660000000009
9600000000009
9999999999999
9055500000009
9005000000009
9005000000009
9999999999999
```

**Train 2 — output**
```text
9999999999999
9000000000309
9000000003339
9000000000309
9999999999999
9000000000009
9000000000669
9000000000609
9999999999999
9000000005559
9000000000509
9000000000509
9999999999999
```

**Train 3 — input**
```text
99999999999
90000000009
98800000009
98800000009
99999999999
90200000009
90222000009
90000000009
99999999999
94000000009
90400000009
90040000009
99999999999
```

**Train 3 — output**
```text
99999999999
90000000009
90000000889
90000000889
99999999999
90000002009
90000002229
90000000009
99999999999
90000000049
90000000049
90000000049
99999999999
```

**Train 4 — input**
```text
999999999999
970700000009
977700000009
900000000009
999999999999
903000000009
903000000009
903000000009
999999999999
906600000009
966000000009
900000000009
999999999999
```

**Train 4 — output**
```text
999999999999
907070000009
907770000009
900000000009
999999999999
900000000039
900000000039
900000000039
999999999999
900000000669
900000006609
900000000009
999999999999
```

**Test — input**
```text
9999999999999
9440000000009
9400000000009
9000000000009
9999999999999
9022000000009
9022000000009
9000000000009
9999999999999
9080000000009
9888000000009
9080000000009
9999999999999
```

**Test — output**
```text
9999999999999
9000000000449
9000000000409
9000000000009
9999999999999
9000000000229
9000000000229
9000000000009
9999999999999
9000000000809
9000000008889
9000000000809
9999999999999
```

**Written solution**

The 9s form walls and three independent horizontal lanes. In each lane, move the colored component right as a rigid object until the next step would hit the wall, then keep the walls unchanged.

**Reference program**
```python
def rule_m127(g):
    h,w=size(g)
    out=blank(h,w,0)
    # keep walls 9
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                out[r][c]=9
    comps=[comp for comp in components_nonzero(g) if comp["color"]!=9]
    # slide each independently east
    for comp in comps:
        temp=clone(out)
        # put comp original just so slide uses walls only? use out with no components
        board=clone(out)
        # but boundaries only; other comps in separate lanes
        cells=comp["cells"]
        for r,c in cells:
            board[r][c]=comp["color"]
        new_cells=slide_until_contact(board,cells,(0,1))
        for r,c in new_cells:
            out[r][c]=comp["color"]
    return out
```

## M128 — Pack Components by Area
**Difficulty:** medium
**Train pairs:** 4
**Skills:** connected components, cropping, sorting by size
**Suggested staged path:** Extract each disconnected object first. Once each object is cropped, the remaining task is just ordering and horizontal packing.

**Train 1 — input**
```text
0000000000000
0040000000000
0444000022000
0040000002200
0000000000000
0770000000000
0700000000000
0000000000000
0000000000000
```

**Train 1 — output**
```text
0400220077
4440022070
0400000000
```

**Train 2 — input**
```text
00000000000000
00333000000000
00030000000000
00030000000000
00000000050000
00000000055500
08800000000000
08800000000000
00000000000000
00000000000000
```

**Train 2 — output**
```text
3330500088
0300555088
0300000000
```

**Train 3 — input**
```text
000000000000000
060600000000000
066600000000000
000000000007000
000000000077700
000200000007000
000020000000000
000002000000000
000000000000000
```

**Train 3 — output**
```text
6060070020202
6660777000000
0000070000000
```

**Train 4 — input**
```text
0000000000000
0550000000000
0055000008800
0000000008000
0000000000000
0044400000000
0000000000000
0000000002200
0000000002200
0000000000000
```

**Train 4 — output**
```text
2205500444088
2200550000080
```

**Test — input**
```text
00000000000000
00777000000000
00070000000000
00070000000060
00000000000600
03000000006000
03330000000000
00000000000000
00000000000000
```

**Test — output**
```text
7770300060606
0700333000000
0700000000000
```

**Written solution**

Find every connected nonzero component, crop it to its own bounding box, sort the cropped objects by descending area and then ascending color, and pack them left-to-right with a single zero column between neighbors.

**Reference program**
```python
def rule_m128(g):
    comps=components_nonzero(g)
    parts=[]
    for comp in comps:
        part=crop_bbox(g, comp["cells"])
        area=len(comp["cells"])
        parts.append((area, comp["color"], part))
    parts.sort(key=lambda x:(-x[0], x[1]))
    return pack_horiz([p[2] for p in parts], gap=1, pad=0)
```

## M129 — Legend Transform Strip
**Difficulty:** medium
**Train pairs:** 4
**Skills:** command decoding, shape transforms, panel packing
**Suggested staged path:** Read the command above each motif as an instruction, not as part of the motif. Apply the transform to each 3×3 panel, then join the transformed panels into one strip.

**Train 1 — input**
```text
0010002000300
0000000000000
0040070002020
0444070000200
0040077702020
```

**Train 1 — output**
```text
04007770202
44407000020
04007000202
```

**Train 2 — input**
```text
0040003000100
0000000000000
0333066008000
0030006008800
0030006600880
```

**Train 2 — output**
```text
03000660800
03000600880
33306600088
```

**Train 3 — input**
```text
0020004000200
0000000000000
0500020000700
0500022007770
0555002200700
```

**Train 3 — output**
```text
55502200070
50000220777
50000020070
```

**Train 4 — input**
```text
0030001000400
0000000000000
0808004003300
0080044400300
0808004000330
```

**Train 4 — output**
```text
80800400330
08004440030
80800400033
```

**Test — input**
```text
0020003000400
0000000000000
0666020205000
0060002005000
0060020205550
```

**Test — output**
```text
00602020555
66600200005
00602020005
```

**Written solution**

Each header digit tells how to transform the motif underneath: 1=identity, 2=rotate 90°, 3=flip horizontally, 4=rotate 180°. Transform the three motifs accordingly and pack the resulting 3×3 panels into one horizontal strip with one zero column gap.

**Reference program**
```python
def rule_m129(g):
    starts=[1,5,9]
    outs=[]
    for st in starts:
        cmd=g[0][st+1]
        mg=[row[st:st+3] for row in g[2:5]]
        outs.append(apply_transform(mg, CMD_TO_TF[cmd]))
    return pack_horiz(outs, gap=1, pad=0)
```

## M130 — Nearest-Seed Chamber Fill
**Difficulty:** medium
**Train pairs:** 4
**Skills:** Manhattan distance, region coloring, ties to background
**Suggested staged path:** The frame fixes the region of interest. After that, every empty interior cell only needs to know which seed is closest.

**Train 1 — input**
```text
00000000000
05555555550
05000000050
05020000050
05000000050
05000004050
05000000050
05555555550
00000000000
```

**Train 1 — output**
```text
00000000000
05555555550
05222204450
05222204450
05222044450
05220444450
05220444450
05555555550
00000000000
```

**Train 2 — input**
```text
0000000000
0055555550
0056000050
0050000050
0050000050
0050000350
0055555550
0000000000
```

**Train 2 — output**
```text
0000000000
0055555550
0056666350
0056663350
0056633350
0056333350
0055555550
0000000000
```

**Train 3 — input**
```text
000000000000
000000000000
055555555550
050200000050
050000000050
050004000050
050000000050
050000007050
055555555550
000000000000
```

**Train 3 — output**
```text
000000000000
000000000000
055555555550
052220007750
052204447750
050044447750
050044477750
050044777750
055555555550
000000000000
```

**Train 4 — input**
```text
000000000
055555550
050008050
050000050
050000050
053000050
050000050
055555550
000000000
```

**Train 4 — output**
```text
000000000
055555550
050888850
053088850
053308850
053330050
053330050
055555550
000000000
```

**Test — input**
```text
00000000000
05555555550
05000000050
05400000050
05000006050
05000000050
05000000050
05000200050
05555555550
00000000000
```

**Test — output**
```text
00000000000
05555555550
05444066650
05444066650
05440666650
05442266650
05422226650
05222222250
05555555550
00000000000
```

**Written solution**

Inside the rectangular frame, every zero cell takes the color of the closest seed by Manhattan distance. If two or more seeds tie for closest, the cell stays 0. Keep the seeds and the frame as they are.

**Reference program**
```python
def rule_m130(g):
    h,w=size(g)
    frame_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    r0,c0,r1,c1=bbox(frame_cells)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    out=clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c] in (0,):
                dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]
                mind=min(d for d,_ in dists)
                cols={color for d,color in dists if d==mind}
                out[r][c]=next(iter(cols)) if len(cols)==1 else 0
    return out
```

## M131 — Palette-Recolored Nested Frames
**Difficulty:** medium
**Train pairs:** 4
**Skills:** nesting depth, palette strip, cropped output
**Suggested staged path:** Ignore the palette row until after you count the nested frames. Then map outermost-to-innermost depth onto the palette colors in order.

**Train 1 — input**
```text
000000000000
008888888000
008000008000
008088808000
008080808000
008088808000
008000008000
008888888000
000000000000
360000000000
```

**Train 1 — output**
```text
3333333
3000003
3066603
3060603
3066603
3000003
3333333
```

**Train 2 — input**
```text
0000000000000
0888888888000
0800000008000
0808888808000
0808000808000
0808080808000
0808000808000
0808888808000
0800000008000
0888888888000
2470000000000
```

**Train 2 — output**
```text
222222222
200000002
204444402
204000402
204070402
204000402
204444402
200000002
222222222
```

**Train 3 — input**
```text
08888888880
08000000080
08088888080
08080008080
08088888080
08000000080
08888888880
00000000000
85000000000
```

**Train 3 — output**
```text
888888888
800000008
805555508
805000508
805555508
800000008
888888888
```

**Train 4 — input**
```text
00000000000000
00088888888800
00080000000800
00080888880800
00080800080800
00080808080800
00080800080800
00080888880800
00080000000800
00088888888800
00000000000000
62400000000000
```

**Train 4 — output**
```text
666666666
600000006
602222206
602000206
602040206
602000206
602222206
600000006
666666666
```

**Test — input**
```text
00000000000
08888888880
08000000080
08088888080
08080008080
08080808080
08080008080
08088888080
08000000080
08888888880
35720000000
```

**Test — output**
```text
333333333
300000003
305555503
305000503
305070503
305000503
305555503
300000003
333333333
```

**Written solution**

The input contains concentric frames all drawn in the same placeholder color plus a palette strip on the bottom row. Crop the nested-frame region and recolor the outer frame with the first palette color, the next frame with the second, and so on inward.

**Reference program**
```python
def rule_m131(g):
    h,w=size(g)
    # palette from bottom row nonzero cells in order
    palette=[v for v in g[h-1] if v!=0]
    # find frame cells excluding bottom row palette if same color? frame color is most common nonzero not in bottom maybe
    frame_cells=[(r,c) for r in range(h-1) for c,v in enumerate(g[r]) if v!=0]
    r0,c0,r1,c1=bbox(frame_cells)
    depths=0
    while r0+2*depths<=r1-2*depths and c0+2*depths<=c1-2*depths:
        rr0,cc0,rr1,cc1=r0+2*depths,c0+2*depths,r1-2*depths,c1-2*depths
        if rr0>rr1 or cc0>cc1:
            break
        # check if there are frame cells along border
        border=[]
        for c in range(cc0,cc1+1):
            border.append(g[rr0][c]); border.append(g[rr1][c])
        for r in range(rr0,rr1+1):
            border.append(g[r][cc0]); border.append(g[r][cc1])
        if all(v!=0 for v in border):
            depths+=1
        else:
            break
    out=blank(r1-r0+1,c1-c0+1,0)
    for d in range(depths):
        color=palette[d]
        rr0,cc0,rr1,cc1=r0+2*d,c0+2*d,r1-2*d,c1-2*d
        for c in range(cc0,cc1+1):
            out[rr0-r0][c-c0]=color
            out[rr1-r0][c-c0]=color
        for r in range(rr0,rr1+1):
            out[r-r0][cc0-c0]=color
            out[r-r0][cc1-c0]=color
    return out
```

## M132 — Dihedral Match Matrix
**Difficulty:** medium
**Train pairs:** 4
**Skills:** shape normalization, rotation/reflection equivalence, relational output
**Suggested staged path:** Convert each motif into a shape mask before comparing anything. Then ask whether each top motif can become each bottom motif through a rotation or reflection.

**Train 1 — input**
```text
400000707
400000070
444000707
000000000
222000050
200000555
200000050
```

**Train 1 — output**
```text
80
00
```

**Train 2 — input**
```text
330000600
030000660
033000066
000000000
808000002
080000022
808000220
```

**Train 2 — output**
```text
00
08
```

**Train 3 — input**
```text
555000200
050000200
050000222
000000000
070000440
070000040
777000044
```

**Train 3 — output**
```text
80
00
```

**Train 4 — input**
```text
080000404
888000040
080000404
000000000
060000300
666000300
060000333
```

**Train 4 — output**
```text
80
00
```

**Test — input**
```text
700000550
770000050
077000055
000000000
022000808
220000080
200000808
```

**Test — output**
```text
80
00
```

**Written solution**

Compare the two top motifs against the two bottom motifs using shape only, ignoring color. Output a 2×2 matrix where a cell is 8 if the corresponding pair is equivalent under some rotation or reflection, otherwise 0.

**Reference program**
```python
def rule_m132(g):
    tops=[[row[0:3] for row in g[0:3]], [row[6:9] for row in g[0:3]]]
    bots=[[row[0:3] for row in g[4:7]], [row[6:9] for row in g[4:7]]]
    top_sigs=[shape_signature(m) for m in tops]
    bot_sigs=[shape_signature(m) for m in bots]
    out=blank(2,2,0)
    for i,ts in enumerate(top_sigs):
        eqs=dihedral_set(ts)
        for j,bs in enumerate(bot_sigs):
            out[i][j]=8 if bs in eqs else 0
    return out
```

## M133 — Transform Analogy
**Difficulty:** medium
**Train pairs:** 4
**Skills:** analogy, transform inference, crop output
**Suggested staged path:** Use the first two panels only to infer the geometric transform. Once that transform is identified, apply it to the third panel and output the result.

**Train 1 — input**
```text
40000040770
40000040070
44404440077
```

**Train 1 — output**
```text
077
070
770
```

**Train 2 — input**
```text
30000030600
33000330600
03303300666
```

**Train 2 — output**
```text
006
006
666
```

**Train 3 — input**
```text
88000080200
08008880220
08808000022
```

**Train 3 — output**
```text
022
220
200
```

**Train 4 — input**
```text
50005550440
50000050040
55500050044
```

**Train 4 — output**
```text
440
040
044
```

**Test — input**
```text
66600060300
06006660300
06000060333
```

**Test — output**
```text
333
300
300
```

**Written solution**

The second 3×3 panel is the first panel after one geometric transform from a small fixed family. Infer that transform from panel A to panel B, then apply the same transform to panel C and output the transformed 3×3 grid.

**Reference program**
```python
def rule_m133(g):
    A=[row[0:3] for row in g]
    B=[row[4:7] for row in g]
    C=[row[8:11] for row in g]
    tf_found=None
    for tf in ANALOGY_TFS:
        if apply_transform(A, tf)==B:
            tf_found=tf; break
    return apply_transform(C, tf_found)
```

## H127 — Commanded Room Slides
**Difficulty:** hard
**Train pairs:** 4
**Skills:** local command decoding, independent chambers, rigid motion
**Suggested staged path:** Split the board into four rooms first. In each room, treat the corner command digit as metadata, clear it from the scene, and slide the remaining object in the commanded direction.

**Train 1 — input**
```text
9999999999999
9200009307709
9044009000009
9040009000009
9000009000009
9000009000009
9999999999999
9400009100009
9000069000009
9000069033009
9000669033009
9000009000009
9999999999999
```

**Train 1 — output**
```text
9999999999999
9000009000009
9000009000009
9000009000009
9000009000009
9000009007709
9999999999999
9000009000009
9060009000009
9060009000009
9660009000009
9000009000009
9999999999999
```

**Train 2 — input**
```text
9999999999999
9100009400009
9000009005509
9022209000559
9002009000009
9002009000009
9999999999999
9280009300009
9088809000709
9000009007009
9000009070009
9000009000009
9999999999999
```

**Train 2 — output**
```text
9999999999999
9000009000009
9000009550009
9000009055009
9000009000009
9000009000009
9999999999999
9008009000009
9008889000009
9000009000709
9000009007009
9000009070009
9999999999999
```

**Train 3 — input**
```text
9999999999999
9300609200009
9006669000009
9000609044409
9000009000009
9000009000009
9999999999999
9100009400009
9000009002029
9005509002229
9005009000009
9000009000009
9999999999999
```

**Train 3 — output**
```text
9999999999999
9000009000009
9000009000009
9000609000009
9006669000009
9000609000009
9999999999999
9005509000009
9005009000009
9000009000009
9000009000009
9000009000009
9999999999999
```

**Train 4 — input**
```text
9999999999999
9400009100009
9007709000009
9007709030009
9000009030009
9000009033009
9999999999999
9366009200009
9006609050009
9000009005009
9000009000509
9000009000009
9999999999999
```

**Train 4 — output**
```text
9999999999999
9000009000009
9770009000009
9770009000009
9000009000009
9000009000009
9999999999999
9000009000009
9000009005009
9000009000509
9066009000059
9006609000009
9999999999999
```

**Test — input**
```text
9999999999999
9200009304009
9080009044409
9088809004009
9000009000009
9000009000009
9999999999999
9400009100009
9000777000009
9000009002209
9000009002009
9000009000009
9999999999999
```

**Test — output**
```text
9999999999999
9000009000009
9008009000009
9008889000009
9000009000009
9000009000009
9999999999999
9000009000009
9770000000009
9000009000009
9000009000009
9000009000009
9999999999999
```

**Written solution**

The 9s divide the board into four independent rooms. In each room, the top-left cell is a command: 1=up, 2=right, 3=down, 4=left. Remove that command marker, slide the colored object in that room as far as possible in the commanded direction, and keep the walls unchanged.

**Reference program**
```python
def rule_h127(g):
    out=blank(13,13,0)
    for r in range(13):
        for c in range(13):
            if g[r][c]==9:
                out[r][c]=9
    room_origins=[(1,1),(1,7),(7,1),(7,7)]
    for r0,c0 in room_origins:
        cmd=g[r0][c0]
        # room board with walls implicit via outer board and room cells only
        # extract object cells
        cells=[(r,c) for r in range(r0,r0+5) for c in range(c0,c0+5) if g[r][c]!=0 and g[r][c] not in {9,1,2,3,4}]
        if not cells:
            continue
        color=g[cells[0][0]][cells[0][1]]
        board=blank(13,13,0)
        # set room boundaries as blockers by marking all outside room interior around? easiest use global wall grid
        for rr in range(13):
            for cc in range(13):
                if rr==0 or rr==6 or rr==12 or cc==0 or cc==6 or cc==12:
                    board[rr][cc]=9
        for rr,cc in cells:
            board[rr][cc]=color
        new_cells=slide_until_contact(board, cells, DIRCMD[cmd])
        for rr,cc in new_cells:
            out[rr][cc]=color
    return out
```

## H128 — Blocked Geodesic Voronoi
**Difficulty:** hard
**Train pairs:** 4
**Skills:** shortest paths, obstacle-aware distance, tie handling
**Suggested staged path:** Do not use straight Manhattan distance across walls. First understand that the 5s are impassable, then color each empty cell by the seed with the shortest path through the open space.

**Train 1 — input**
```text
0000000000000
0555555555550
0520005000050
0500005000050
0500005000050
0505555555050
0500005000050
0500005000050
0500000000450
0555555555550
0000000000000
```

**Train 1 — output**
```text
0000000000000
0555555555550
0522225444450
0522225444450
0522225444450
0525555555450
0522205444450
0522045444450
0520444444450
0555555555550
0000000000000
```

**Train 2 — input**
```text
000000000000
055555555550
050000003050
055555550050
050002000050
050005000050
050005000050
050705000050
055555555550
000000000000
```

**Train 2 — output**
```text
000000000000
055555555550
053333333350
055555553350
052222223350
057725223350
057775223350
057775223350
055555555550
000000000000
```

**Train 3 — input**
```text
00000000000
05555555550
05800500050
05000500050
05000500050
05000500050
05055555550
05000000050
05000000450
05555555550
00000000000
```

**Train 3 — output**
```text
00000000000
05555555550
05888500050
05888500050
05888500050
05888500050
05855555550
05804444450
05044444450
05555555550
00000000000
```

**Train 4 — input**
```text
00000000000000
00555555555500
00560000000500
00500000000500
00555555550500
00500008050500
00500000050500
00500500050500
00500500050500
00500500002500
00555555555500
00000000000000
```

**Train 4 — output**
```text
00000000000000
00555555555500
00566666660500
00566666602500
00555555552500
00588888852500
00588888852500
00588588852500
00588588252500
00588522222500
00555555555500
00000000000000
```

**Test — input**
```text
0000000000000
0555555555550
0500000000750
0500500000050
0500500000050
0500504000050
0500500000050
0500555555550
0530500000050
0555555555550
0000000000000
```

**Test — output**
```text
0000000000000
0555555555550
0534444777750
0533544477750
0533544447750
0533544444750
0533544444750
0533555555550
0533500000050
0555555555550
0000000000000
```

**Written solution**

The frame and interior 5-cells are walls. For every reachable zero cell, compute the shortest path length to each colored seed while staying out of walls. Color the cell with the unique nearest seed, and leave ties as 0.

**Reference program**
```python
def rule_h128(g):
    return geodesic_fill(g)
```

## H129 — Commanded Template Mosaic
**Difficulty:** hard
**Train pairs:** 4
**Skills:** template selection, transform decoding, 2×2 composition
**Suggested staged path:** Separate the job into two parts: read the two source templates, then decode each command as a choice of template plus transform. After that, the output is just a 2×2 assembly.

**Train 1 — input**
```text
01060003080
00000000000
04000007000
04000007700
04440000770
```

**Train 1 — output**
```text
400077
400770
444700
004770
004077
444007
```

**Train 2 — input**
```text
05020007040
00000000000
03300008000
00300008000
00330008880
```

**Train 2 — output**
```text
800003
800333
888300
008330
008030
888033
```

**Train 3 — input**
```text
06010008030
00000000000
05000002200
05500000200
00550000220
```

**Train 3 — output**
```text
002500
222550
200055
220005
020055
022550
```

**Train 4 — input**
```text
04070002050
00000000000
06000003000
06000003300
06660000330
```

**Train 4 — output**
```text
666003
006033
006330
666300
600330
600033
```

**Test — input**
```text
08030005020
00000000000
07700004000
00700004000
00770004440
```

**Test — output**
```text
444077
004070
004770
400007
400777
444700
```

**Written solution**

Two source templates are shown in the input. Each command digit selects one of the templates and one transform: 1–4 mean template A with identity, rotate 90°, horizontal flip, or rotate 180°; 5–8 mean the same four transforms applied to template B. Build the 2×2 output mosaic in reading order from the four commands.

**Reference program**
```python
def rule_h129(g):
    A=[row[1:4] for row in g[2:5]]
    B=[row[7:10] for row in g[2:5]]
    cmd_positions=[1,3,7,9]
    tiles=[]
    for pos in cmd_positions:
        cmd=g[0][pos]
        base,tf=decode_cmd_h129(cmd)
        tile=apply_transform(A if base=='A' else B, tf)
        tiles.append(tile)
    top=pack_horiz(tiles[:2], gap=0, pad=0)
    bottom=pack_horiz(tiles[2:], gap=0, pad=0)
    return pack_vert([top,bottom], gap=0, pad=0)
```

## H130 — Overlap After Transform
**Difficulty:** hard
**Train pairs:** 4
**Skills:** intersection, transform decoding, mask reasoning
**Suggested staged path:** Ignore colors at first and compare only the occupied cells. Transform the right motif as commanded, then keep only the cells where both motifs occupy the same position.

**Train 1 — input**
```text
0002000
4000770
4000070
4440077
```

**Train 1 — output**
```text
000
800
800
```

**Train 2 — input**
```text
0003000
3000800
3300800
0330888
```

**Train 2 — output**
```text
000
000
088
```

**Train 3 — input**
```text
0004000
5500200
0500220
0550022
```

**Train 3 — output**
```text
880
080
008
```

**Train 4 — input**
```text
0001000
6000300
6000330
6660033
```

**Train 4 — output**
```text
800
800
088
```

**Test — input**
```text
0002000
7000440
7700040
0770044
```

**Test — output**
```text
000
880
000
```

**Written solution**

A command digit specifies how to transform the right-hand 3×3 motif: 1=identity, 2=rotate 90°, 3=flip horizontally, 4=rotate 180°. After transforming it, output a 3×3 grid with 8 exactly where the transformed right motif overlaps the left motif, and 0 elsewhere.

**Reference program**
```python
def rule_h130(g):
    cmd=g[0][3]
    A=[row[0:3] for row in g[1:4]]
    B=[row[4:7] for row in g[1:4]]
    tf_map={1:0,2:1,3:4,4:2}
    Bt=apply_transform(B, tf_map[cmd])
    out=blank(3,3,0)
    for r in range(3):
        for c in range(3):
            out[r][c]=8 if (A[r][c]!=0 and Bt[r][c]!=0) else 0
    return out
```

## H131 — Pack by Hole Count
**Difficulty:** hard
**Train pairs:** 4
**Skills:** hole counting, component ranking, cropped packing
**Suggested staged path:** First crop each component so hole counting becomes local. Then sort by the number of enclosed holes rather than by raw size alone.

**Train 1 — input**
```text
000000000000000000
044400077777000000
040400070707000000
044400077777000000
000000000000000000
000000000000020000
000000000000020000
000000000000022200
000000000000000000
000000000000000000
```

**Train 1 — output**
```text
7777704440200
7070704040200
7777704440222
```

**Train 2 — input**
```text
00000000000000000000
03333300000000000000
03030300088880000000
03333300080080000000
03030300080080000000
03333300088880000000
00000000000000000500
00000000000000005550
00000000000000000500
00000000000000000000
00000000000000000000
```

**Train 2 — output**
```text
33333088880050
30303080080555
33333080080050
30303088880000
33333000000000
```

**Train 3 — input**
```text
0000000000000000000
0066666000000000000
0060606000000077770
0066666000000070070
0000000000000070070
0000000000222077770
0000000000202000000
0000000000222000000
0000000000000000000
0000000000000000000
```

**Train 3 — output**
```text
66666077770222
60606070070202
66666070070222
00000077770000
```

**Train 4 — input**
```text
00000000000000000000
04444000333330000000
04004000303030000000
04004000333330000000
04444000303030000000
00000000333330000000
00000000000000000000
00000000000000008000
00000000000000008000
00000000000000008880
00000000000000000000
00000000000000000000
```

**Train 4 — output**
```text
33333044440800
30303040040800
33333040040888
30303044440000
33333000000000
```

**Test — input**
```text
000000000000000000
000000055555000000
077700050505000000
070700055555000000
077700000000000000
000000000000000000
000000000000000400
000000000000004440
000000000000000400
000000000000000000
000000000000000000
```

**Test — output**
```text
5555507770040
5050507070444
5555507770040
```

**Written solution**

Extract every connected component, count how many enclosed holes it has inside its own bounding box, crop the component, sort the cropped components by descending hole count and then descending area, and pack them left-to-right with one zero column between them.

**Reference program**
```python
def rule_h131(g):
    comps=components_nonzero(g)
    ranked=[]
    for comp in comps:
        holes=count_holes_in_component(g, comp["cells"])
        area=len(comp["cells"])
        part=crop_bbox(g, comp["cells"])
        ranked.append((holes, area, comp["color"], part))
    ranked.sort(key=lambda x:(-x[0], -x[1], x[2]))
    return pack_horiz([p[3] for p in ranked], gap=1, pad=0)
```

## H132 — Phase Transform Tile Grid
**Difficulty:** hard
**Train pairs:** 4
**Skills:** transform composition, tiling, guide-driven structure
**Suggested staged path:** Read the row guides and column guides separately before composing them. Each output tile is the base motif after one row transform and one column transform.

**Train 1 — input**
```text
01030
00000
14000
04000
24440
```

**Train 1 — output**
```text
400004
400004
444444
444444
400004
400004
```

**Train 2 — input**
```text
02030
00000
37000
07700
10770
```

**Train 2 — output**
```text
700700
770770
077077
077007
770077
700770
```

**Train 3 — input**
```text
01020
00000
25500
00500
20550
```

**Train 3 — output**
```text
005550
555050
500055
005550
555050
500055
```

**Train 4 — input**
```text
03010
00000
36000
06000
26660
```

**Train 4 — output**
```text
600006
600006
666666
666666
006600
006600
```

**Test — input**
```text
02010
00000
18000
08800
30880
```

**Test — output**
```text
088800
880880
800088
800008
880088
088880
```

**Written solution**

The lower-left 3×3 panel is the base motif. Row-guide digits on the left and column-guide digits on the top choose transforms from a small family, and each output tile is formed by composing the row transform with the column transform on the base motif. Assemble the resulting 2×2 tile grid.

**Reference program**
```python
def rule_h132(g):
    row_cmds=[g[2][0], g[4][0]]
    col_cmds=[g[0][1], g[0][3]]
    M=[row[1:4] for row in g[2:5]]
    rows=[]
    for rc in row_cmds:
        tiles=[]
        for cc in col_cmds:
            tiles.append(compose_phase_tf(rc, cc, M))
        rows.append(pack_horiz(tiles, gap=0, pad=0))
    return pack_vert(rows, gap=0, pad=0)
```

## H133 — Color-and-Transform Analogy
**Difficulty:** hard
**Train pairs:** 4
**Skills:** joint geometry and color analogy, transform inference, recoloring
**Suggested staged path:** Use the first two panels to infer two things at once: the geometric transform and the target color. Then apply both to the third panel.

**Train 1 — input**
```text
40000070440
40000070040
44407770044
```

**Train 1 — output**
```text
077
070
770
```

**Train 2 — input**
```text
30000060300
33000660300
03306600333
```

**Train 2 — output**
```text
006
006
666
```

**Train 3 — input**
```text
88000020800
08002220880
08802000088
```

**Train 3 — output**
```text
022
220
200
```

**Train 4 — input**
```text
50004440550
50000040050
55500040055
```

**Train 4 — output**
```text
440
040
044
```

**Test — input**
```text
66600030600
06003330600
06000030666
```

**Test — output**
```text
333
300
300
```

**Written solution**

Panel B is panel A after a geometric transform plus a recoloring from the source color to a target color. Infer the transform from the change in shape and infer the target color from panel B, then transform panel C in the same way and recolor all of its occupied cells to the target color.

**Reference program**
```python
def rule_h133(g):
    A=[row[0:3] for row in g]
    B=[row[4:7] for row in g]
    C=[row[8:11] for row in g]
    src=next(v for row in A for v in row if v!=0)
    tgt=next(v for row in B for v in row if v!=0)
    tf_found=None
    A_mask=[[1 if v!=0 else 0 for v in row] for row in A]
    B_mask=[[1 if v!=0 else 0 for v in row] for row in B]
    for tf in ANALOGY_TFS:
        if apply_transform(A_mask, tf)==B_mask:
            tf_found=tf; break
    Cmask=[[1 if v!=0 else 0 for v in row] for row in C]
    T=apply_transform(Cmask, tf_found)
    out=blank(3,3,0)
    for r in range(3):
        for c in range(3):
            out[r][c]=tgt if T[r][c] else 0
    return out
```
