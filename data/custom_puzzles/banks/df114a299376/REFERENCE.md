# ARC-style Puzzle Bank — 21 more puzzles (set 19)

This nineteenth bank leans into **panel decomposition, cross-panel voting, analogy, library lookup, and symbolic comparison**. The central move is to stop treating the whole grid as one monolith and instead split it into explicit subproblems: source panels, candidate panels, header panels, tiny lookup libraries, and relation outputs. Once the panels are separated, the solver can do a wide range of higher-level operations: choose by occupancy, compare under translation or rotation, take boolean merges, run panel-wise votes, infer an analogy transform, or mark the correct candidate set in a symbolic strip or matrix.

The core primitive introduced here is:

```text
extract_panels(grid, divider_color=9, axis='col')
Split a grid into a linear sequence of subgrids separated by full divider rows or columns. This turns multi-panel ARC layouts into explicit panel objects that can be selected, compared, voted over, used as examples in a tiny transformation library, or converted into symbolic outputs like strips and relation matrices.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set19_reference.py`.

## Index

### Easy

- **S19_E1** — Union of Two Panels

- **S19_E2** — Intersection of Two Panels

- **S19_E3** — Select the Largest Panel by Occupancy

- **S19_E4** — Header Count Selects the Candidate Panel

- **S19_E5** — Duplicate Panel Consensus

- **S19_E6** — Majority Occupancy Across Three Panels

- **S19_E7** — Key Color Selects the Matching Panel

### Medium

- **S19_M1** — Symmetric Difference of Two Panels

- **S19_M2** — Source-to-Candidate Match Under Translation

- **S19_M3** — Relation Strip: Which Candidates Match the Source?

- **S19_M4** — Operation Key Chooses the Boolean Merge

- **S19_M5** — Select the Candidate Matching the Source After Rotation

- **S19_M6** — Stamp the Template at Every Marker Panel

- **S19_M7** — Sort Four Panels by Occupancy into a 2×2 Mosaic

### Hard

- **S19_H1** — Congruence Matrix Under Dihedral Symmetry

- **S19_H2** — Analogy A:B::C:? with Panel Candidates

- **S19_H3** — Which Candidate Unions with the Source to Make the Target?

- **S19_H4** — Which Candidate XORs with the Source to Make the Target?

- **S19_H5** — Panel Library Lookup by Shape Key

- **S19_H6** — Rotate the Panels by Header Codes, Then Take the Majority

- **S19_H7** — Which Pair of Candidates Completes the Target with the Source?


# Easy


## S19_E1 — Union of Two Panels
**Skills:** panel splitting, occupancy union, same-size blank output

**Primitive note:** Use extract_panels across the divider column, then take the union of the two occupancy sets.

**Scaffold:**

- Split the input into the left panel and the right panel.
- Ignore the colors; only the occupied cells matter.
- Place every occupied cell from either panel into a blank output panel in color 8.

**Train 1 input**

```text
20000900000
20000900300
22000903330
00000900000
00000900000
```
**Train 1 output**

```text
80000
80800
88880
00000
00000
```
**Train 2 input**

```text
20000900000
02000900440
00200900440
00000900440
00000900000
```
**Train 2 output**

```text
80000
08880
00880
00880
00000
```
**Test input**

```text
02020900000
02220900000
00000900030
00000900030
00000900000
```
**Expected test output**

```text
08080
08880
00080
00080
00000
```
**Written solution**

Split the grid into its two side panels. Treat any nonzero cell in either panel as occupied. Align the panels cell-for-cell, take the union of their occupied cells, and write that union onto a blank output panel in color 8.

**Reference program**

```python
def solve_S19_E1(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(union_cells(a,b), h,w, 8)
```

## S19_E2 — Intersection of Two Panels
**Skills:** panel splitting, overlap detection, same-size output

**Primitive note:** Once the panels are extracted, keep only cells that are occupied in both of them at the same coordinates.

**Scaffold:**

- Split the grid into two panels.
- Compare them in the same coordinates.
- Keep only the cells that are occupied in both panels and paint them 8.

**Train 1 input**

```text
00000900300
02220903330
02220900300
00000900300
00000900000
```
**Train 1 output**

```text
00000
08880
00800
00000
00000
```
**Train 2 input**

```text
00000900000
02200904400
02200900400
02200900440
00000900000
```
**Train 2 output**

```text
00000
08800
00800
00800
00000
```
**Test input**

```text
00000900300
02020903330
02220900300
00000900300
00000900000
```
**Expected test output**

```text
00000
08080
00800
00000
00000
```
**Written solution**

Separate the two panels, align them, and compare each coordinate. A cell belongs in the output only when both panels have a nonzero value there. Paint those overlap cells onto a blank output grid in color 8.

**Reference program**

```python
def solve_S19_E2(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(inter_cells(a,b), h,w, 8)
```

## S19_E3 — Select the Largest Panel by Occupancy
**Skills:** panel extraction, object counting, argmax selection

**Primitive note:** Extract all panels and count their nonzero cells; the fullest panel wins.

**Scaffold:**

- Split the input into the three panels.
- Count how many cells are occupied in each one.
- Return the panel with the highest count, recolored to 8.

**Train 1 input**

```text
20009000090000
22009030090440
00009333090440
00009030090000
```
**Train 1 output**

```text
0000
0800
8880
0800
```
**Train 2 input**

```text
22009003094040
00009033394440
00009000090000
00009000090000
```
**Train 2 output**

```text
8080
8880
0000
0000
```
**Test input**

```text
20009000090000
20009030090000
22209003090400
00009000090440
```
**Expected test output**

```text
8000
8000
8880
0000
```
**Written solution**

Extract the three panels, count the nonzero cells in each, and choose the one with the largest occupancy. Copy that panel’s occupied shape to the output, but recolor it uniformly as 8.

**Reference program**

```python
def solve_S19_E3(grid):
    pans=extract_panels(grid, axis='col')
    best=max(pans, key=lambda p: (len(panel_occ(p)), -pans.index(p)))
    return recolor_panel(best, 8)
```

## S19_E4 — Header Count Selects the Candidate Panel
**Skills:** row-wise panel splitting, tiny header decoding, indexed selection

**Primitive note:** The first panel is a header; the number of marked cells in it tells you which later panel to select.

**Scaffold:**

- Split the stacked input into the header and three candidate panels.
- Count the nonzero header cells.
- Use that count as a 1-based index into the candidate panels and output the chosen one in color 8.

**Train 1 input**

```text
7700
9999
2000
2000
2200
0000
9999
0000
0330
0330
0000
9999
0000
0400
4440
0000
```
**Train 1 output**

```text
0000
0880
0880
0000
```
**Train 2 input**

```text
7770
9999
0220
0000
0000
0000
9999
3030
3330
0000
0000
9999
0000
4400
0440
0000
```
**Train 2 output**

```text
0000
8800
0880
0000
```
**Test input**

```text
7000
9999
2000
2000
2220
0000
9999
0000
0000
3300
3300
9999
0040
0444
0000
0000
```
**Expected test output**

```text
8000
8000
8880
0000
```
**Written solution**

Read the top header panel and count its nonzero cells. That count tells you which of the three candidate panels to choose below it. Copy the chosen candidate’s occupied cells to the output and recolor them 8.

**Reference program**

```python
def solve_S19_E4(grid):
    header,p1,p2,p3=extract_panels(grid, axis='row')
    n=sum(1 for row in header for v in row if v!=0)
    chosen=[p1,p2,p3][n-1]
    return recolor_panel(chosen,8)
```

## S19_E5 — Duplicate Panel Consensus
**Skills:** exact panel comparison, majority agreement, same-size output

**Primitive note:** Two of the three panels are exactly the same occupancy pattern; output the repeated one.

**Scaffold:**

- Split the input into three panels.
- Compare their occupied-cell patterns exactly.
- Find the pattern that appears twice and output it in color 8.

**Train 1 input**

```text
20009000094000
20009033094000
22009033094400
00009000090000
```
**Train 1 output**

```text
8000
8000
8800
0000
```
**Train 2 input**

```text
00009330094400
02009033090440
22209000090000
00009000090000
```
**Train 2 output**

```text
8800
0880
0000
0000
```
**Test input**

```text
20209303090000
22209333090000
00009000090440
00009000090000
```
**Expected test output**

```text
8080
8880
0000
0000
```
**Written solution**

Extract the three panels and compare their occupied coordinates exactly. Two panels match each other and one does not. Output the repeated pattern on a blank panel of the same size, recolored as 8.

**Reference program**

```python
def solve_S19_E5(grid):
    p1,p2,p3=extract_panels(grid, axis='col')
    occs=[panel_occ(p1), panel_occ(p2), panel_occ(p3)]
    # choose repeated exact occupancy
    if occs[0]==occs[1] or occs[0]==occs[2]:
        return recolor_panel(p1,8)
    return recolor_panel(p2,8)
```

## S19_E6 — Majority Occupancy Across Three Panels
**Skills:** panel voting, coordinate-wise counting, same-size synthesis

**Primitive note:** This is a cellwise majority vote across three aligned panels.

**Scaffold:**

- Split the input into three aligned panels.
- For each coordinate, count how many panels occupy it.
- Keep the coordinates that are occupied in at least two panels and paint them 8.

**Train 1 input**

```text
20000930000900000
20000930000900400
22000933000904440
00000900000900000
00000900000900000
```
**Train 1 output**

```text
80000
80000
88000
00000
00000
```
**Train 2 input**

```text
02020903030900000
02220903330900000
00000900000900000
00000900000900040
00000900000900040
```
**Train 2 output**

```text
08080
08880
00000
00000
00000
```
**Test input**

```text
00000900000944000
00200900300904400
02220903330900000
00000900000900000
00000900000900000
```
**Expected test output**

```text
00000
00800
08880
00000
00000
```
**Written solution**

Treat the three panels as aligned versions of the same coordinate system. For each cell position, count in how many panels that position is occupied. Put a color-8 cell in the output wherever at least two panels agree that the position is occupied.

**Reference program**

```python
def solve_S19_E6(grid):
    pans=extract_panels(grid, axis='col')
    h,w=dims(pans[0])
    return render_same_size(majority_cells(pans,2), h,w, 8)
```

## S19_E7 — Key Color Selects the Matching Panel
**Skills:** legend decoding, panel selection by color, same-size recolor

**Primitive note:** The first small panel is a color key; choose the candidate panel whose object uses that color.

**Scaffold:**

- Read the key panel and identify its nonzero color.
- Split the remaining candidates into separate panels.
- Choose the candidate whose object color matches the key and output it in color 8.

**Train 1 input**

```text
00920009000090000
30922009033090400
03900009033094440
00900009000090000
```
**Train 1 output**

```text
0000
0880
0880
0000
```
**Train 2 input**

```text
00920209003390000
40922209000094400
04900009000090440
00900009000090000
```
**Train 2 output**

```text
0000
8800
0880
0000
```
**Test input**

```text
00920009000090040
20920009000090444
02922209330090000
00900009330090000
```
**Expected test output**

```text
8000
8000
8880
0000
```
**Written solution**

The leftmost small panel is only a key: its nonzero value tells you which color to look for. Among the candidate panels, find the one whose nonzero cells use that same color. Copy its shape to the output and recolor it as 8.

**Reference program**

```python
def solve_S19_E7(grid):
    key,*cands=extract_panels(grid, axis='col')
    k=panel_color(key)
    for p in cands:
        if panel_color(p)==k:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```


# Medium


## S19_M1 — Symmetric Difference of Two Panels
**Skills:** panel extraction, boolean XOR, same-size synthesis

**Primitive note:** Take the cells occupied in exactly one of the two panels, not both.

**Scaffold:**

- Split the input into two panels.
- Compare occupancy coordinate by coordinate.
- Keep cells that appear in exactly one panel and paint them 8.

**Train 1 input**

```text
00000900000
02220903300
02220900300
00000900300
00000900000
```
**Train 1 output**

```text
00000
00080
08080
00800
00000
```
**Train 2 input**

```text
00000900000
02020900400
02220904440
00000900000
00000900000
```
**Train 2 output**

```text
00000
08880
00000
00000
00000
```
**Test input**

```text
00000900000
00200903300
02220900300
00000900300
00000900000
```
**Expected test output**

```text
00000
08000
08080
00800
00000
```
**Written solution**

Extract the two panels and compute their symmetric difference: a coordinate survives only when one panel occupies it and the other does not. Render that XOR result on a blank output grid in color 8.

**Reference program**

```python
def solve_S19_M1(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(xor_cells(a,b), h,w, 8)
```

## S19_M2 — Source-to-Candidate Match Under Translation
**Skills:** panel normalization, shape matching, selection

**Primitive note:** Normalize each panel by shifting its occupied cells to the top-left of its own bounding box.

**Scaffold:**

- Treat the first panel as the source shape.
- Normalize the source and every candidate by removing translation.
- Choose the candidate with the same normalized shape and output it in color 8.

**Train 1 input**

```text
2000900309000090000
2000903339040090000
2200900009040096600
0000900009044096600
```
**Train 1 output**

```text
0000
0800
0800
0880
```
**Train 2 input**

```text
2200930309000090000
0220933309000096600
0000900009044090660
0000900009000090000
```
**Train 2 output**

```text
0000
8800
0880
0000
```
**Test input**

```text
0200900009400096060
2220903009440096660
0000933309000090000
0000900009000090000
```
**Expected test output**

```text
0000
0800
8880
0000
```
**Written solution**

Take the first panel as the source. Ignore where the shape sits inside its panel by normalizing occupied cells relative to their own bounding box. Among the candidates, exactly one has the same normalized shape as the source; output that candidate’s shape recolored to 8.

**Reference program**

```python
def solve_S19_M2(grid):
    src,*cands=extract_panels(grid, axis='col')
    ns=normalize(panel_occ(src))
    for p in cands:
        if normalize(panel_occ(p))==ns:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```

## S19_M3 — Relation Strip: Which Candidates Match the Source?
**Skills:** symbolic output, normalized-shape comparison, multi-candidate scoring

**Primitive note:** The output is not another panel but a 1×N relation strip marking which candidates match the source under translation.

**Scaffold:**

- Normalize the source panel’s shape.
- Normalize each candidate panel the same way.
- Emit a 1×4 strip with 8 for matches and 0 for non-matches.

**Train 1 input**

```text
200090000900409600090000
200090300904449600090770
220090300900009660090770
000090330900009000090000
```
**Train 1 output**

```text
8080
```
**Train 2 input**

```text
220093030900009000097700
022093330944009066090770
000090000904409000090000
000090000900009000090000
```
**Train 2 output**

```text
0808
```
**Test input**

```text
020090030900009060097070
222090333940009666097770
000090000940009000090000
000090000944009000090000
```
**Expected test output**

```text
8080
```
**Written solution**

Use the first panel as a source shape and compare it to each candidate after translation normalization. For every candidate whose normalized occupied pattern matches the source, put an 8 in the corresponding output position; otherwise put 0.

**Reference program**

```python
def solve_S19_M3(grid):
    src,*cands=extract_panels(grid, axis='col')
    ns=normalize(panel_occ(src))
    out=[[8 if normalize(panel_occ(p))==ns else 0 for p in cands]]
    return out
```

## S19_M4 — Operation Key Chooses the Boolean Merge
**Skills:** header decoding, panel-wise boolean operations, same-size output

**Primitive note:** The top header marks which boolean operation to apply to the two panels below: union, intersection, XOR, or A-minus-B.

**Scaffold:**

- Read the header panel and determine the requested operation.
- Extract the two operand panels.
- Apply the chosen boolean merge to their occupied cells and render the result in color 8.

**Train 1 input**

```text
50000
00000
99999
20000
20000
22000
00000
00000
99999
00000
00300
03330
00000
00000
```
**Train 1 output**

```text
80000
80800
88880
00000
00000
```
**Train 2 input**

```text
00005
00000
99999
00000
02220
02220
00000
00000
99999
00300
03330
00300
00300
00000
```
**Train 2 output**

```text
00000
08880
00800
00000
00000
```
**Test input**

```text
00000
50000
99999
00000
02020
02220
00000
00000
99999
00000
00400
04440
00000
00000
```
**Expected test output**

```text
00000
08880
00000
00000
00000
```
**Written solution**

Interpret the top header as an operation code. Then split out the two operand panels below it and apply the indicated boolean rule to their occupied coordinates: union, intersection, XOR, or A-minus-B. Paint the resulting coordinate set onto a blank panel in color 8.

**Reference program**

```python
def solve_S19_M4(grid):
    header,a,b=extract_panels(grid, axis='row')
    h,w=dims(a)
    op=op_from_header(header)
    if op=='union':
        cells=union_cells(a,b)
    elif op=='inter':
        cells=inter_cells(a,b)
    elif op=='xor':
        cells=xor_cells(a,b)
    else:
        cells=minus_cells(a,b)
    return render_same_size(cells, h,w, 8)
```

## S19_M5 — Select the Candidate Matching the Source After Rotation
**Skills:** rotation matching, panel selection, normalized comparison

**Primitive note:** Only rotation is allowed here, not reflection.

**Scaffold:**

- Take the first panel as the source.
- Generate its four rotated forms after normalization.
- Select the candidate whose normalized shape matches one of those rotations and output it in color 8.

**Train 1 input**

```text
2000900309444090000
2000903339400090660
2200900009000090660
0000900009000090000
```
**Train 1 output**

```text
8880
8000
0000
0000
```
**Train 2 input**

```text
2200930309044090000
0220933309004496000
0000900009000096600
0000900009000090000
```
**Train 2 output**

```text
0880
0088
0000
0000
```
**Test input**

```text
0200930009000096060
2220930009040096660
0000933009440090000
0000900009040090000
```
**Expected test output**

```text
0000
0800
8800
0800
```
**Written solution**

Treat the first panel as a source shape and ignore translation. Generate the four rotation classes of that shape. Exactly one candidate matches one of those rotated forms, so output that candidate’s occupied pattern recolored as 8.

**Reference program**

```python
def solve_S19_M5(grid):
    src,*cands=extract_panels(grid, axis='col')
    src_occ=panel_occ(src)
    variants={normalize(rotate_times(list(src_occ),k)) for k in range(4)}
    for p in cands:
        if normalize(panel_occ(p)) in variants:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```

## S19_M6 — Stamp the Template at Every Marker Panel
**Skills:** template extraction, anchor offsets, repeated placement

**Primitive note:** The first panel is a template; the second panel supplies anchor markers where that template should be stamped.

**Scaffold:**

- Extract the template shape from the first panel.
- Measure its occupied-cell offsets from its own top-left occupied corner.
- For every marker in the second panel, place a copy of those offsets into the output and color them 8.

**Train 1 input**

```text
20000
22000
00000
00000
00000
99999
30000
00000
00000
00300
00000
```
**Train 1 output**

```text
80000
88000
00000
00800
00880
```
**Train 2 input**

```text
22000
00000
00000
00000
00000
99999
00030
03000
00000
30000
00000
```
**Train 2 output**

```text
00088
08800
00000
88000
00000
```
**Test input**

```text
02000
22000
00000
00000
00000
99999
03000
00000
00300
00000
00000
```
**Expected test output**

```text
00800
08800
00080
00880
00000
```
**Written solution**

Use the first panel as a template and convert its occupied cells into relative offsets from the template’s own top-left occupied cell. In the second panel, every marker cell is an anchor. Stamp the template offsets at each anchor location and combine all stamped copies into the color-8 output.

**Reference program**

```python
def solve_S19_M6(grid):
    template, markers=extract_panels(grid, axis='row')
    return stamp_template(template, markers, 3)
```

## S19_M7 — Sort Four Panels by Occupancy into a 2×2 Mosaic
**Skills:** panel counting, sorting, structured assembly

**Primitive note:** This puzzle turns a list of panels into an ordered mosaic based on occupancy counts.

**Scaffold:**

- Split the input into four equal panels.
- Count their occupied cells and sort from fewest to most.
- Place them into a 2×2 output mosaic in reading order, recolored to 8.

**Train 1 input**

```text
200933094009000
000900094409066
000900090009066
```
**Train 1 output**

```text
800880
000000
000000
800000
880088
000088
```
**Train 2 input**

```text
020930090409060
020900094409666
000900090009060
```
**Train 2 output**

```text
800080
000080
000000
080080
880888
000080
```
**Test input**

```text
200933090009060
220933090009660
000900090049000
```
**Expected test output**

```text
000800
000880
008000
080880
880880
000000
```
**Written solution**

Extract the four panels and rank them by number of occupied cells. Then build a 2×2 output canvas: smallest in the top-left, next in the top-right, third in the bottom-left, and largest in the bottom-right. Recolor all copied cells as 8.

**Reference program**

```python
def solve_S19_M7(grid):
    pans=extract_panels(grid, axis='col')
    ordered=sorted(pans, key=lambda p:(len(panel_occ(p)), pans.index(p)))
    # assemble 2x2 mosaic
    ph,pw=dims(ordered[0])
    out=blank(ph*2, pw*2, 0)
    positions=[(0,0),(0,pw),(ph,0),(ph,pw)]
    for p,(r0,c0) in zip(ordered,positions):
        for r,c in panel_occ(p):
            out[r0+r][c0+c]=8
    return out
```


# Hard


## S19_H1 — Congruence Matrix Under Dihedral Symmetry
**Skills:** pairwise comparison, dihedral normalization, symbolic matrix output

**Primitive note:** Two panels count as equivalent when one can be rotated or reflected to match the other.

**Scaffold:**

- Extract the three panels.
- For each ordered pair, test whether the second panel matches any dihedral variant of the first.
- Write a 3×3 matrix with 8 for equivalent pairs and 0 otherwise.

**Train 1 input**

```text
20009333090400
20009300094440
22009000090000
00009000090000
```
**Train 1 output**

```text
880
880
008
```
**Train 2 input**

```text
22009033090000
02209330090440
00009000090440
00009000090000
```
**Train 2 output**

```text
880
880
008
```
**Test input**

```text
02009333094040
22209030094440
00009000090000
00009000090000
```
**Expected test output**

```text
880
880
008
```
**Written solution**

Treat the input as three separate panels. For each panel, generate its full dihedral family: the four rotations and their mirror images. Then compare every ordered pair of panels. Put an 8 in the output matrix when the second panel’s normalized shape belongs to the first panel’s dihedral family; otherwise put 0.

**Reference program**

```python
def solve_S19_H1(grid):
    pans=extract_panels(grid, axis='col')
    n=len(pans)
    out=blank(n,n,0)
    for i,a in enumerate(pans):
        va=dihedral_variants(panel_occ(a))
        for j,b in enumerate(pans):
            if normalize(panel_occ(b)) in va:
                out[i][j]=8
    return out
```

## S19_H2 — Analogy A:B::C:? with Panel Candidates
**Skills:** transform inference, dihedral/rotation reasoning, candidate selection

**Primitive note:** Infer the transformation that takes panel A to panel B, then apply that same transformation to panel C.

**Scaffold:**

- Use the first two panels to infer a single transform class.
- Apply that transform to the third panel after normalization.
- Among the candidates, choose the one that matches the transformed third panel and output it in color 8.

**Train 1 input**

```text
20009333094400900609707090800
20009300090440906609777098880
22009000090000906009000090000
00009000090000900009000090000
```
**Train 1 output**

```text
0080
0880
0800
0000
```
**Train 2 input**

```text
22009033094000906009000098080
02209330094400966009770098880
00009000090000900009000090000
00009000090000900009000090000
```
**Train 2 output**

```text
0800
8800
0000
0000
```
**Test input**

```text
02009333094000906609000098080
22209030094000900609077098880
00009000094400900609077090000
00009000090000900009000090000
```
**Expected test output**

```text
0880
0080
0080
0000
```
**Written solution**

Look at the first pair of panels and determine which transformation maps A to B: one of the rotations or a horizontal reflection. Apply that same transform to panel C. Then scan the candidate panels and choose the one whose normalized shape matches the transformed C, outputting it in color 8.

**Reference program**

```python
def solve_S19_H2(grid):
    pans=extract_panels(grid, axis='col')
    a,b,c,*cands=pans
    tf=identify_transform(a,b)
    if tf=='flip':
        target=normalize(reflect_h_cells(list(panel_occ(c))))
    else:
        target=normalize(rotate_times(list(panel_occ(c)), int(tf[-1])))
    for p in cands:
        if normalize(panel_occ(p))==target:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```

## S19_H3 — Which Candidate Unions with the Source to Make the Target?
**Skills:** inverse boolean reasoning, candidate search, set union

**Primitive note:** This is a reverse boolean problem: instead of forming the union, you must identify which candidate completes the target when united with the source.

**Scaffold:**

- Extract the source panel, the target panel, and the candidates.
- For each candidate, union its occupied cells with the source.
- Choose the unique candidate whose union exactly equals the target and output it in color 8.

**Train 1 input**

```text
200092020900309000090000
220092220900309000090600
000090000900009004090600
000090000900009000090000
```
**Train 1 output**

```text
0080
0080
0000
0000
```
**Train 2 input**

```text
220092200900009004090000
000092200903009000096600
000090000903009000090000
000090000900009000090000
```
**Train 2 output**

```text
0000
8800
0000
0000
```
**Test input**

```text
020090200933009000090000
020092200900009440090000
000090000900009000090060
000090000900009000090000
```
**Expected test output**

```text
0000
8800
0000
0000
```
**Written solution**

Treat the first panel as the source and the second as the desired target. Test each candidate by taking the union of its occupied coordinates with the source. Exactly one candidate produces the target panel exactly; output that completing candidate, recolored as 8.

**Reference program**

```python
def solve_S19_H3(grid):
    src,target,*cands=extract_panels(grid, axis='col')
    target_occ=panel_occ(target)
    src_occ=panel_occ(src)
    for p in cands:
        if src_occ | panel_occ(p) == target_occ:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```

## S19_H4 — Which Candidate XORs with the Source to Make the Target?
**Skills:** inverse XOR reasoning, candidate search, boolean sets

**Primitive note:** Instead of forward XOR, this puzzle asks which candidate has the right disagreement pattern with the source.

**Scaffold:**

- Extract the source, target, and candidate panels.
- Compute source XOR candidate for each option.
- Choose the one whose XOR result equals the target and output it in color 8.

**Train 1 input**

```text
200090000903009400090000
220092000930009040090000
000090000900009000090060
000090000900009000090000
```
**Train 1 output**

```text
8000
0800
0000
0000
```
**Train 2 input**

```text
000090000900009400090000
022090220903309000090000
022090000900009004090660
000090000900009000090000
```
**Train 2 output**

```text
0000
0000
0880
0000
```
**Test input**

```text
020090000903009000090000
222092020903009404090000
000090000900009000090600
000090000900009000090000
```
**Expected test output**

```text
0800
0800
0000
0000
```
**Written solution**

The first panel is the source and the second is the target. For each candidate, compute which cells would survive a symmetric-difference operation with the source. The correct candidate is the one whose XOR pattern matches the target exactly; output that candidate’s shape in color 8.

**Reference program**

```python
def solve_S19_H4(grid):
    src,target,*cands=extract_panels(grid, axis='col')
    target_occ=panel_occ(target)
    src_occ=panel_occ(src)
    for p in cands:
        if src_occ ^ panel_occ(p) == target_occ:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)
```

## S19_H5 — Panel Library Lookup by Shape Key
**Skills:** panel pairing, library retrieval, dihedral key matching

**Primitive note:** The panels come in alternating key/value pairs, followed by a query key.

**Scaffold:**

- Split the input into key/value pairs plus a final query panel.
- Match the query to one of the keys using dihedral shape equivalence.
- Return the value panel paired with that key, recolored to 8.

**Train 1 input**

```text
2000930309440090600900009000090050
2000933309044096660907709880090550
2200900009000090000907709000090500
0000900009000090000900009000090000
```
**Train 1 output**

```text
0800
8880
0000
0000
```
**Train 2 input**

```text
2000900009040090060970709800095050
2200903309444090060977709800095550
0000903309000090000900009880090000
0000900009000090000900009000090000
```
**Train 2 output**

```text
8000
8000
8800
0000
```
**Test input**

```text
0200930009400090000977009088090550
2220933009400090660907709000090050
0000900009440090660900009000090050
0000900009000090000900009000090000
```
**Expected test output**

```text
0000
0880
0880
0000
```
**Written solution**

Interpret the panels as a tiny lookup library: key₁,value₁,key₂,value₂,key₃,value₃,query. Compare the query’s normalized shape to the keys, allowing rotations and reflections. Once the matching key is found, output the value panel paired with it, recolored as 8.

**Reference program**

```python
def solve_S19_H5(grid):
    pans=extract_panels(grid, axis='col')
    # alternating key,value ..., query last
    query=pans[-1]
    pairs=list(zip(pans[0:-1:2], pans[1:-1:2]))
    qn=normalize(panel_occ(query))
    qd=dihedral_variants(panel_occ(query))
    for key,val in pairs:
        if normalize(panel_occ(key)) in qd:
            return recolor_panel(val,8)
    return blank(*dims(pairs[0][1]),0)
```

## S19_H6 — Rotate the Panels by Header Codes, Then Take the Majority
**Skills:** header decoding, panel-wise transforms, voting after alignment

**Primitive note:** The header gives one rotation code per panel. Apply those rotations first, then do a majority vote on occupancy.

**Scaffold:**

- Read the three rotation codes from the header.
- Rotate each corresponding panel by the requested amount.
- Take a cellwise majority vote over the transformed panels and paint the result 8.

**Train 1 input**

```text
1210
9999
2000
2000
2200
0000
9999
0030
3330
0000
0000
9999
0400
4440
0000
0000
```
**Train 1 output**

```text
8000
8000
8800
0000
```
**Train 2 input**

```text
3140
9999
2200
0220
0000
0000
9999
3300
0330
0000
0000
9999
0400
4400
4000
0000
```
**Train 2 output**

```text
8800
0880
0000
0000
```
**Test input**

```text
2410
9999
0200
2220
0000
0000
9999
3000
3300
3000
0000
9999
4000
4000
4400
0000
```
**Expected test output**

```text
8000
8800
8000
0000
```
**Written solution**

Use the top header row as three rotation instructions, one for each panel below. Rotate each panel’s occupied shape accordingly, keeping the panels aligned in their own coordinate system. Then compute the majority occupancy across the transformed panels and output the agreed cells in color 8.

**Reference program**

```python
def solve_S19_H6(grid):
    header,p1,p2,p3=extract_panels(grid, axis='row')
    codes=[header[0][i] for i in range(3)]
    pans=[p1,p2,p3]
    transformed=[]
    for p,code in zip(pans,codes):
        k={1:0,2:1,3:2,4:3}.get(code,0)
        transformed.append(render_same_size(set(rotate_times(list(panel_occ(p)),k)), *dims(p), 8))
    h,w=dims(p1)
    return render_same_size(majority_cells(transformed,2), h,w, 8)
```

## S19_H7 — Which Pair of Candidates Completes the Target with the Source?
**Skills:** pair search, inverse union reasoning, symbolic one-hot output

**Primitive note:** This is the pairwise version of the completion problem: two candidates together, not one, must complete the target.

**Scaffold:**

- Extract the source, target, and four candidate panels.
- Test every candidate pair by uniting both with the source.
- Output a 1×4 strip that marks the two candidates whose combined union exactly equals the target.

**Train 1 input**

```text
20009220090300900009000090000
00009020090000940009000090700
00009000090000900009006090000
00009000090000900009000090000
```
**Train 1 output**

```text
8008
```
**Train 2 input**

```text
22009222090000900009006090000
00009020093000904009000090000
00009000090000900009000090070
00009000090000900009000090000
```
**Train 2 output**

```text
0880
```
**Test input**

```text
00009020090300900009000090000
02009220090000940009000090070
00009000090000900009060090000
00009000090000900009000090000
```
**Expected test output**

```text
8800
```
**Written solution**

Treat the first panel as the source and the second as the target. Now search over all unordered pairs of candidate panels. For each pair, take the union of the source and both candidates. Exactly one pair reproduces the target, so mark those two candidate positions with 8 in a 1×4 output strip and leave the others as 0.

**Reference program**

```python
def solve_S19_H7(grid):
    pans=extract_panels(grid, axis='col')
    src,target,*cands=pans
    src_occ=panel_occ(src); target_occ=panel_occ(target)
    out=[[0]*len(cands)]
    for i in range(len(cands)):
        for j in range(i+1,len(cands)):
            if src_occ | panel_occ(cands[i]) | panel_occ(cands[j]) == target_occ:
                out[0][i]=8
                out[0][j]=8
                return out
    return out
```
