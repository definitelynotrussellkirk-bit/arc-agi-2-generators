# ARC-style Puzzle Bank — 21 more puzzles (set 17)

This seventeenth bank leans into **stencil growth, halos, contact surfaces, and object selection under hypothetical expansion**. The same basic move — expand source cells by a local offset stencil — gets repurposed in a lot of ways here: direct plus and X blooming, square halos, overlap extraction, second-layer shells, border-touching selection, mini-legend transfer, hole-sealing, and symbolic contact matrices.

The core primitive introduced here is:

```text
expand_with_stencil(cells, offsets, bounds)
Translate one small offset stencil around every source cell, union the translated
copies, and clip the result to the grid bounds. This makes plus growth, X growth,
square halos, contact tests, layer differences, and library-based stamping explicit.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set17_reference.py`.

## Index

### Easy

- **S17_E1** — Plus Bloom

- **S17_E2** — Diagonal Bloom

- **S17_E3** — 3x3 Stamp Around Each Seed

- **S17_E4** — Halo Without the Center

- **S17_E5** — Overlap of Two 3x3 Growths

- **S17_E6** — Corner Marker Chooses Plus or X

- **S17_E7** — Total Plus-Growth Size as a Bar


### Medium

- **S17_M1** — Color-Dependent Stencils

- **S17_M2** — Exact Manhattan-Radius-2 Ring

- **S17_M3** — Crop the Largest Grown Object

- **S17_M4** — Object Halo Only

- **S17_M5** — Legend Chooses Which Color Grows

- **S17_M6** — First Contact of Two Plus Growths

- **S17_M7** — Border-Touching Growth Wins


### Hard

- **S17_H1** — Arbitrary Stencil from a Mini-Legend

- **S17_H2** — Odd Panel by Plus-Grown Signature

- **S17_H3** — First Meeting Frontier Under Repeated Plus Growth

- **S17_H4** — Pick the Object Whose Halo Seals the Hole

- **S17_H5** — Color-Labeled Stencil Library

- **S17_H6** — Mask-Selected by Hypothetical Growth

- **S17_H7** — Growth Contact Matrix


# Easy


## S17_E1 — Plus Bloom
**Skills:** local stencil application, multi-seed union, same-size blank output

**Primitive note:** This is the simplest use of expand_with_stencil: apply one fixed offset set to every seed and union the results.

**Scaffold:**

- Treat every nonzero cell as a seed.
- Use the plus stencil: center plus the 4 cardinal neighbors.
- Union those marks on a blank grid and recolor them to 8.

**Train 1 input**

```text
00000000
02000000
00000000
00000000
00000000
00000200
00000000
00000000
```
**Train 1 output**

```text
08000000
88800000
08000000
00000000
00000800
00008880
00000800
00000000
```
**Train 2 input**

```text
000000000
000000000
000000200
000000000
000020000
000000000
002000000
000000000
000000000
```
**Train 2 output**

```text
000000000
000000800
000008880
000080800
000888000
008080000
088800000
008000000
000000000
```
**Test input**

```text
000000000
000000200
000000000
000000000
000000000
002000000
000000000
000000000
```
**Expected test output**

```text
000000800
000008880
000000800
000000000
008000000
088800000
008000000
000000000
```
**Written solution**

Each nonzero cell is just a center point. Around every seed, draw the 5-cell plus made of the center and its four orthogonal neighbors. Put the union of all those pluses onto a blank output grid and color the result 8.

**Reference program**

```python
def solve_S17_E1(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, PLUS, (h,w)), 8)
    return out
```


## S17_E2 — Diagonal Bloom
**Skills:** diagonal neighborhood reasoning, multi-seed stamping, same-size output

**Primitive note:** The primitive is the same as in E1, but the offset stencil is the X shape instead of the plus shape.

**Scaffold:**

- Find all nonzero seed cells.
- Use the center plus the 4 diagonal neighbors, not the cardinals.
- Write the union of those X-shaped stamps in color 8 on a blank grid.

**Train 1 input**

```text
00000000
00000000
00300000
00000000
00000000
00000300
00000000
00000000
```
**Train 1 output**

```text
00000000
08080000
00800000
08080000
00008080
00000800
00008080
00000000
```
**Train 2 input**

```text
000000000
000000000
000000300
000000000
000000000
000000000
003000000
000000000
000000000
```
**Train 2 output**

```text
000000000
000008080
000000800
000008080
000000000
080800000
008000000
080800000
000000000
```
**Test input**

```text
00000000
00000300
00000000
00000000
00000000
03000000
00000000
00000000
```
**Expected test output**

```text
00008080
00000800
00008080
00000000
80800000
08000000
80800000
00000000
```
**Written solution**

Ignore the original seed color. Every nonzero cell becomes the center of a 5-cell X: the center and the four diagonal neighbors. Overlay all of those X stamps on a blank grid and recolor the kept cells to 8.

**Reference program**

```python
def solve_S17_E2(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, XST, (h,w)), 8)
    return out
```


## S17_E3 — 3x3 Stamp Around Each Seed
**Skills:** square neighborhood growth, union of local windows, blank reconstruction

**Primitive note:** Here the stencil is the full radius-1 square, so expand_with_stencil acts like a 3×3 stamp around each seed.

**Scaffold:**

- Read every nonzero cell as a seed.
- Around each seed, fill the full 3×3 neighborhood centered there.
- Take the union and color the result 8.

**Train 1 input**

```text
0000000
0400000
0000000
0000000
0000000
0000040
0000000
```
**Train 1 output**

```text
8880000
8880000
8880000
0000000
0000888
0000888
0000888
```
**Train 2 input**

```text
000000000
000000000
000000400
000000000
000000000
004000000
000000000
000000000
```
**Train 2 output**

```text
000000000
000008880
000008880
000008880
088800000
088800000
088800000
000000000
```
**Test input**

```text
00000000
00000040
00000000
00004000
00000000
00000000
00000000
```
**Expected test output**

```text
00000888
00000888
00088888
00088800
00088800
00000000
00000000
```
**Written solution**

For every nonzero cell, fill all nine positions in the 3×3 block centered on that cell. Combine all of those little squares on a blank output grid. Any covered cell becomes 8.

**Reference program**

```python
def solve_S17_E3(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, SQ1, (h,w)), 8)
    return out
```


## S17_E4 — Halo Without the Center
**Skills:** difference between growth and source, cardinal halos, local exclusion

**Primitive note:** This uses a plus expansion, but then subtracts the original seed cells so only the outer halo remains.

**Scaffold:**

- Start from the same plus growth as in E1.
- Remove the original seed positions from that grown set.
- Color only the remaining halo cells as 8.

**Train 1 input**

```text
00000000
00000000
00500000
00000000
00000000
00000500
00000000
00000000
```
**Train 1 output**

```text
00000000
00800000
08080000
00800000
00000800
00008080
00000800
00000000
```
**Train 2 input**

```text
000000000
000000000
000000000
000000000
000050000
000000000
000000000
000000000
000000000
```
**Train 2 output**

```text
000000000
000000000
000000000
000080000
000808000
000080000
000000000
000000000
000000000
```
**Test input**

```text
00000000
00000000
00000500
00000000
00000000
00500000
00000000
00000000
```
**Expected test output**

```text
00000000
00000800
00008080
00000800
00800000
08080000
00800000
00000000
```
**Written solution**

First imagine drawing the usual 5-cell plus around every seed. Then delete the center seed cell from each plus, keeping only the four orthogonal neighbors. The output is the union of those halos, written in 8 on a blank grid.

**Reference program**

```python
def solve_S17_E4(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(seeds, PLUS, (h,w))
    halo=grown - set(seeds)
    out=blank(h,w,0)
    place(out, halo, 8)
    return out
```


## S17_E5 — Overlap of Two 3x3 Growths
**Skills:** set intersection, color-specific selection, square expansion

**Primitive note:** Two different seed sets are expanded with the same square stencil, and the answer keeps only their overlap.

**Scaffold:**

- Separate the color-2 seed from the color-3 seed.
- Expand each one to its own 3×3 square.
- Keep only the cells covered by both expansions and recolor them 8.

**Train 1 input**

```text
0000000
0000000
0000000
0020300
0000000
0000000
0000000
```
**Train 1 output**

```text
0000000
0000000
0008000
0008000
0008000
0000000
0000000
```
**Train 2 input**

```text
00000000
00000000
00200000
00000000
00003000
00000000
00000000
00000000
```
**Train 2 output**

```text
00000000
00000000
00000000
00080000
00000000
00000000
00000000
00000000
```
**Test input**

```text
00000000
00000000
00002000
00000000
00003000
00000000
00000000
00000000
```
**Expected test output**

```text
00000000
00000000
00000000
00088800
00000000
00000000
00000000
00000000
```
**Written solution**

Treat the 2-cell and the 3-cell as two different centers. Around each one, make the full 3×3 square. The output does not keep either whole square; it keeps only the intersection, i.e. the cells that lie in both grown regions. Those overlap cells become 8.

**Reference program**

```python
def solve_S17_E5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=expand_with_stencil(by[2], SQ1, (h,w))
    b=expand_with_stencil(by[3], SQ1, (h,w))
    out=blank(h,w,0)
    place(out, a & b, 8)
    return out
```


## S17_E6 — Corner Marker Chooses Plus or X
**Skills:** legend-controlled branching, stencil selection, seed stamping

**Primitive note:** The same seed layout can be grown with one of two offset sets; the top-left legend chooses which one.

**Scaffold:**

- Read the top-left cell as the mode selector.
- If the legend is 1, use the plus stencil; if it is 2, use the X stencil.
- Apply that stencil to every other nonzero seed and write the result in 8.

**Train 1 input**

```text
10000000
00000000
00000400
00000000
00000000
00400000
00000000
00000000
```
**Train 1 output**

```text
00000000
00000800
00008880
00000800
00800000
08880000
00800000
00000000
```
**Train 2 input**

```text
20000000
00000000
00400000
00000000
00000000
00000400
00000000
00000000
```
**Train 2 output**

```text
00000000
08080000
00800000
08080000
00008080
00000800
00008080
00000000
```
**Test input**

```text
100000000
000000000
000000400
000000000
000000000
000400000
000000000
000000000
```
**Expected test output**

```text
000000000
000000800
000008880
000000800
000800000
008880000
000800000
000000000
```
**Written solution**

The top-left marker is not a seed to grow; it tells you which stencil to use. A 1 means use the 5-cell plus, while a 2 means use the 5-cell diagonal X. Apply the chosen stencil to the actual seeds elsewhere in the grid and output the union in color 8.

**Reference program**

```python
def solve_S17_E6(grid):
    h,w=dims(grid)
    legend=grid[0][0]
    seeds=[(r,c) for r,c,v in nonzero(grid) if (r,c)!=(0,0)]
    offsets=PLUS if legend==1 else XST
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, offsets, (h,w)), 8)
    return out
```


## S17_E7 — Total Plus-Growth Size as a Bar
**Skills:** counting derived cells, symbolic output, growth without overlap

**Primitive note:** Instead of drawing the grown region itself, this task asks for its size as a 1-row bar.

**Scaffold:**

- Grow each seed with the plus stencil.
- Count how many cells are in the union of all grown pluses.
- Output a single horizontal bar of that length, filled with 8.

**Train 1 input**

```text
0000000
0000000
0000000
0002000
0000000
0000000
0000000
```
**Train 1 output**

```text
88888
```
**Train 2 input**

```text
00000000
00000000
00200000
00000000
00000000
00000200
00000000
00000000
```
**Train 2 output**

```text
8888888888
```
**Test input**

```text
000000000
000000000
002000000
000000000
000000200
000000000
000200000
000000000
000000000
```
**Expected test output**

```text
888888888888888
```
**Written solution**

Do the same plus growth as in E1, but do not draw that result back onto the original board. Count how many cells are in the full grown union, then make a 1-row output whose length matches that count. Fill the whole bar with 8.

**Reference program**

```python
def solve_S17_E7(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(seeds, PLUS, (h,w))
    out=blank(1,len(grown),8)
    return out
```

# Medium


## S17_M1 — Color-Dependent Stencils
**Skills:** multi-rule composition, color-conditioned behavior, overlay of distinct growth rules

**Primitive note:** expand_with_stencil stays the same, but the offset set now depends on the color of the seed.

**Scaffold:**

- Partition the seeds by color.
- Grow color 2 with a plus, color 3 with an X, and color 4 with a full 3×3 square.
- Overlay the results, keeping each growth in its own color.

**Train 1 input**

```text
000000000
000000000
002000300
000000000
000000000
000000000
000040000
000000000
000000000
```
**Train 1 output**

```text
000000000
002003030
022200300
002003030
000000000
000444000
000444000
000444000
000000000
```
**Train 2 input**

```text
0000000000
0000000000
0020000000
0000000300
0000000000
0000000000
0000000000
0020000400
0000000000
0000000000
```
**Train 2 output**

```text
0000000000
0020000000
0222003030
0020000300
0000003030
0000000000
0020004440
0222004440
0020004440
0000000000
```
**Test input**

```text
0000000000
0000000000
0002000000
0000000000
0000000000
0000000300
0040000000
0000000000
0000000000
```
**Expected test output**

```text
0000000000
0002000000
0022200000
0002000000
0000003030
0444000300
0444003030
0444000000
0000000000
```
**Written solution**

This puzzle has three growth rules at once. Every 2-seed grows into a plus of 2s, every 3-seed grows into a diagonal X of 3s, and every 4-seed grows into a filled 3×3 square of 4s. Combine all of those color-specific growths on one blank grid.

**Reference program**

```python
def solve_S17_M1(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    out=blank(h,w,0)
    mapping={2:PLUS,3:XST,4:SQ1}
    for color,seeds in by.items():
        if color in mapping:
            place(out, expand_with_stencil(seeds, mapping[color], (h,w)), color)
    return out
```


## S17_M2 — Exact Manhattan-Radius-2 Ring
**Skills:** iterated growth, layer subtraction, distance-shell reasoning

**Primitive note:** Run the plus growth twice and keep only the cells added on the second step.

**Scaffold:**

- Start from the seeds and do one plus expansion.
- Expand that result once more with the same plus stencil.
- Subtract the first-step growth so only the distance-2 ring remains.

**Train 1 input**

```text
000000000
000000000
000000000
000000000
000020000
000000000
000000000
000000000
000000000
```
**Train 1 output**

```text
000000000
000000000
000080000
000808000
008000800
000808000
000080000
000000000
000000000
```
**Train 2 input**

```text
0000000000
0000000000
0000000000
0002000000
0000000000
0000000000
0000002000
0000000000
0000000000
0000000000
```
**Train 2 output**

```text
0000000000
0008000000
0080800000
0800080000
0080808000
0008080800
0000800080
0000080800
0000008000
0000000000
```
**Test input**

```text
0000000000
0000000000
0000002000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Expected test output**

```text
0000008000
0000080800
0000800080
0000080800
0000008000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**

Think of plus growth as one step of Manhattan-distance expansion. After one step you have distance 0 and 1 from the seed; after two steps you reach distance 2 as well. The puzzle asks for the new cells that appear only on the second step, so keep the step-2 region minus the step-1 region and color it 8.

**Reference program**

```python
def solve_S17_M2(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    step1=expand_with_stencil(seeds, PLUS, (h,w))
    step2=expand_with_stencil(step1, PLUS, (h,w))
    ring=step2 - step1
    out=blank(h,w,0)
    place(out, ring, 8)
    return out
```


## S17_M3 — Crop the Largest Grown Object
**Skills:** component extraction, hypothetical growth for ranking, cropped output

**Primitive note:** The stencil is a 3×3 square, but the task scores entire components by the size of their grown region.

**Scaffold:**

- Split the nonzero cells into separate connected objects.
- Square-grow each object by one step and compare the grown sizes.
- Take the largest grown object, crop to its bounding box, and recolor it 8.

**Train 1 input**

```text
000000000000
000000000000
002000000000
000000000000
000000000000
000000022000
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
8888
8888
8888
```
**Train 2 input**

```text
000000000000
000000000000
002200000000
000000000000
000000000000
000000000000
000000020000
000000022000
000000000000
000000000000
```
**Train 2 output**

```text
8880
8888
8888
8888
```
**Test input**

```text
0000000000000
0000000000000
0020000000000
0000000000000
0000000000000
0000002200000
0000000000000
0000000000000
0000000002000
0000000002200
0000000000000
```
**Expected test output**

```text
8880
8888
8888
8888
```
**Written solution**

The objects compete after, not before, growth. For each separate object, expand all of its cells with the 3×3 square stencil and measure the size of that grown union. Choose the object whose grown footprint is largest, then output that grown footprint cropped tightly and recolored to 8.

**Reference program**

```python
def solve_S17_M3(grid):
    h,w=dims(grid)
    comps=[comp for comp in components(grid) if comp["color"]!=0]
    best=None
    best_grown=None
    for comp in comps:
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        key=(len(grown), -len(comp["cells"]))  # area first
        if best is None or key>best:
            best=key; best_grown=grown
    return crop_cells(best_grown, 8)
```


## S17_M4 — Object Halo Only
**Skills:** whole-object dilation, difference mask, same-size halo extraction

**Primitive note:** This is the object-level analogue of E4: grow with a square stencil, then subtract the original object cells.

**Scaffold:**

- Treat all nonzero cells as object pixels, not isolated seeds.
- Grow the whole foreground by one square-expansion step.
- Remove the original foreground, leaving only the outside halo in 8.

**Train 1 input**

```text
0000000000
0000000000
0033000000
0030000000
0000000000
0000000000
0000003300
0000003300
0000000000
```
**Train 1 output**

```text
0000000000
0888800000
0800800000
0808800000
0888000000
0000088880
0000080080
0000080080
0000088880
```
**Train 2 input**

```text
00000000000
00000000000
00000003000
00000003000
00000003000
00000000000
00330000000
00030000000
00000000000
00000000000
```
**Train 2 output**

```text
00000000000
00000088800
00000080800
00000080800
00000080800
08888088800
08008000000
08808000000
00888000000
00000000000
```
**Test input**

```text
0000000000
0000000000
0033000000
0003000000
0000000000
0000000000
0000003000
0000003330
0000000000
0000000000
```
**Expected test output**

```text
0000000000
0888800000
0800800000
0880800000
0088800000
0000088800
0000080888
0000080008
0000088888
0000000000
```
**Written solution**

Square-expand the entire foreground by one cell in every direction. That gives a thickened version of the original objects. Then erase the original object cells from that thickened region. The remaining outside band is the halo, and that is what the output shows in 8.

**Reference program**

```python
def solve_S17_M4(grid):
    h,w=dims(grid)
    occ=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(occ, SQ1, (h,w))
    halo=grown - set(occ)
    out=blank(h,w,0)
    place(out, halo, 8)
    return out
```


## S17_M5 — Legend Chooses Which Color Grows
**Skills:** selector legends, color filtering, single-branch expansion

**Primitive note:** The top-left legend now picks the target seed color rather than the stencil itself.

**Scaffold:**

- Read the top-left cell as the target color.
- Ignore nonzero cells of every other color.
- Square-grow only the matching seeds and output that grown set in 8.

**Train 1 input**

```text
200000000
000000000
002000300
000000000
000000000
000000000
002000400
000000000
000000000
```
**Train 1 output**

```text
000000000
088800000
088800000
088800000
000000000
088800000
088800000
088800000
000000000
```
**Train 2 input**

```text
400000000
000000000
002000400
000000000
000000000
000000000
003000400
000000000
000000000
```
**Train 2 output**

```text
000000000
000008880
000008880
000008880
000000000
000008880
000008880
000008880
000000000
```
**Test input**

```text
3000000000
0000000000
0020000300
0000000000
0000000000
0000000000
0003000400
0000000000
0000000000
```
**Expected test output**

```text
0000000000
0000008880
0000008880
0000008880
0000000000
0088800000
0088800000
0088800000
0000000000
```
**Written solution**

The corner value tells you which seed color matters on this puzzle. Find only the seeds whose color matches the legend, expand those seeds with the full 3×3 square stencil, and discard everything else. The union of the chosen growth becomes 8.

**Reference program**

```python
def solve_S17_M5(grid):
    h,w=dims(grid)
    target=grid[0][0]
    seeds=[(r,c) for r,c,v in nonzero(grid) if (r,c)!=(0,0) and v==target]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, SQ1, (h,w)), 8)
    return out
```


## S17_M6 — First Contact of Two Plus Growths
**Skills:** set intersection after growth, multi-cell seed groups, one-step contact reasoning

**Primitive note:** Two different foreground groups use the same plus growth, and the answer is where those one-step growths touch.

**Scaffold:**

- Collect the color-2 cells and the color-3 cells separately.
- Apply one plus expansion to each group.
- Keep only the cells that appear in both expanded sets.

**Train 1 input**

```text
00000000
00000000
00000000
00203000
00000000
00000000
00000000
00000000
```
**Train 1 output**

```text
00000000
00000000
00000000
00080000
00000000
00000000
00000000
00000000
```
**Train 2 input**

```text
000000000
000000000
002030000
002030000
000000000
000000000
000000000
000000000
000000000
```
**Train 2 output**

```text
000000000
000000000
000800000
000800000
000000000
000000000
000000000
000000000
000000000
```
**Test input**

```text
0000000000
0000000000
0000002000
0000302000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Expected test output**

```text
0000000000
0000000000
0000000000
0000080000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**

Grow the 2-group and the 3-group outward by one plus step. You do not keep either full growth. Instead, keep the cells where the two one-step expansions overlap. Those shared contact cells are written as 8.

**Reference program**

```python
def solve_S17_M6(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=expand_with_stencil(by[2], PLUS, (h,w))
    b=expand_with_stencil(by[3], PLUS, (h,w))
    out=blank(h,w,0)
    place(out, a & b, 8)
    return out
```


## S17_M7 — Border-Touching Growth Wins
**Skills:** hypothetical clipping, selection by border interaction, cropped output

**Primitive note:** Square growth is clipped by the grid boundary, and the chosen seed is the one whose grown region actually hits that boundary.

**Scaffold:**

- Imagine the 3×3 square around each seed.
- Check which grown square touches the outer border of the grid.
- Crop that winning grown square and recolor it 8.

**Train 1 input**

```text
00020000
00000000
00000000
00000000
00000200
00000000
00000000
```
**Train 1 output**

```text
888
888
```
**Train 2 input**

```text
00000000
00000000
00000000
00000200
00000000
00000000
20000000
00000000
```
**Train 2 output**

```text
88
88
88
```
**Test input**

```text
000000000
000000000
000000000
002000000
000000000
000000000
000000000
000020000
```
**Expected test output**

```text
888
888
```
**Written solution**

Grow each seed into its 3×3 square, clipped by the edges of the board. Only one of those grown squares reaches the border. Select that border-touching grown region, crop it tightly, and output it in 8.

**Reference program**

```python
def solve_S17_M7(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    candidates=[]
    for s in seeds:
        grown=expand_with_stencil([s], SQ1, (h,w))
        touch=any(r in {0,h-1} or c in {0,w-1} for r,c in grown)
        candidates.append((touch,len(grown),s,grown))
    chosen=max(candidates)  # touch first True>False, then more cells (clipped border maybe smaller? but touch dominates)
    return crop_cells(chosen[3],8)
```

# Hard


## S17_H1 — Arbitrary Stencil from a Mini-Legend
**Skills:** pattern extraction from an in-grid legend, anchor-relative offsets, arbitrary stamping

**Primitive note:** The offset stencil is no longer fixed in code; it must be read from the mini-legend around the anchor cell.

**Scaffold:**

- In the top-left 5×5 legend, use the 9-cell as the anchor.
- Record the offsets from that anchor to every 1-cell in the legend.
- Apply that extracted offset set to every color-2 seed elsewhere and output the union in 8.

**Train 1 input**

```text
00000000000
00100000000
00900000000
00110000000
00000000000
00000000000
00002000000
00000002000
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00008000000
00000008000
00008800000
00000008800
00000000000
```
**Train 2 input**

```text
000000000000
011000000000
009100000000
000100000000
000000000000
000000000000
000000000000
000000200000
000000000200
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000008800000
000000088800
000000080080
000000000080
000000000000
```
**Test input**

```text
00000000000
00100000000
00910000000
01100000000
00000000000
00000000000
00000000000
00000002000
00002000000
00000000000
00000000000
```
**Expected test output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000008000
00008000800
00000888000
00088000000
00000000000
```
**Written solution**

The small legend in the corner literally tells you which relative offsets belong to the stencil. Use the 9 as the origin, note where the 1-cells sit relative to it, and treat that set of offsets as the shape to stamp. Then place that same offset pattern around every 2-seed elsewhere in the grid and color the result 8.

**Reference program**

```python
def solve_S17_H1(grid):
    h,w=dims(grid)
    # legend occupies rows 0:5 cols0:5 ; anchor color 9 indicates center
    legend_cells=[(r,c,v) for r,c,v in nonzero([row[:5] for row in grid[:5]])]
    anchor=[(r,c) for r,c,v in legend_cells if v==9][0]
    offsets=[(r-anchor[0], c-anchor[1]) for r,c,v in legend_cells if v!=9]
    seeds=[(r,c) for r,c,v in nonzero(grid) if not (r<5 and c<5) and v==2]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, offsets, (h,w)), 8)
    return out
```


## S17_H2 — Odd Panel by Plus-Grown Signature
**Skills:** panel splitting, dihedral normalization, comparison after transformation

**Primitive note:** The comparison is not on the raw objects; it is on their one-step plus-grown silhouettes, up to rotation and reflection.

**Scaffold:**

- Split the board into panels at the separator columns.
- Plus-grow each panel object and normalize its grown shape up to dihedral symmetry.
- Find the unique signature and output that panel’s original object, cropped and recolored to 8.

**Train 1 input**

```text
00000900000900000900000
00000900200900000900200
02200900200900220900220
00000900000900000900000
00000900000900000900000
```
**Train 1 output**

```text
80
88
```
**Train 2 input**

```text
00000900000900000900000
02000900000900000902200
02000902200900200902000
00000900000900200900000
00000900000900000900000
```
**Train 2 output**

```text
88
80
```
**Test input**

```text
00000900000900000900000
00000900200900000902000
02200900200900220902200
00000900000900000900000
00000900000900000900000
```
**Expected test output**

```text
80
88
```
**Written solution**

Each panel contains one small object. Expand each object by one plus step, then compare the grown silhouettes after allowing rotation and reflection. Three panels agree and one panel differs. Output the original object from the odd panel, cropped tightly and shown in 8.

**Reference program**

```python
def solve_S17_H2(grid):
    # panels separated by col 9s; choose odd panel by plus-grown dihedral signature; output original odd object cropped
    panels=panel_split_vertical(grid, sep=9)
    sigs=[]
    originals=[]
    for a,b,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        grown=expand_with_stencil(cells, PLUS, dims(p))
        sig=norm_dihedral(grown)
        sigs.append(sig)
        originals.append(cells)
    cnt=Counter(sigs)
    odd_idx=[i for i,s in enumerate(sigs) if cnt[s]==1][0]
    return crop_cells(originals[odd_idx],8)
```


## S17_H3 — First Meeting Frontier Under Repeated Plus Growth
**Skills:** simultaneous expansion, earliest-contact reasoning, iterative set updates

**Primitive note:** This extends one-step contact into a repeated process: keep expanding both sides until they first intersect.

**Scaffold:**

- Start from the color-2 cells and color-3 cells as two fronts.
- Expand both fronts by the plus stencil in lockstep.
- Stop at the first step where the fronts overlap, and output only that first overlap set in 8.

**Train 1 input**

```text
00000000
00000000
00000000
02000300
00000000
00000000
00000000
00000000
```
**Train 1 output**

```text
00000000
00000000
00000000
00080000
00000000
00000000
00000000
00000000
```
**Train 2 input**

```text
000000000
000020000
000000000
000000000
000000000
000000000
000030000
000000000
000000000
```
**Train 2 output**

```text
000000000
000000000
000000000
000080000
000080000
000000000
000000000
000000000
000000000
```
**Test input**

```text
0000000000
0000000000
0000000000
0000000000
0200000300
0000000000
0000000000
0000000000
0000000000
```
**Expected test output**

```text
0000000000
0000000000
0000000000
0000000000
0000800000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**

Imagine both colored seed groups growing outward by plus steps at the same speed. Do not wait until they heavily overlap; stop the very first time the two grown regions intersect. The answer is that first meeting frontier, written in 8.

**Reference program**

```python
def solve_S17_H3(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    A=set(by[2]); B=set(by[3])
    # simultaneous growth with plus, find first intersection
    for step in range(10):
        inter=A & B
        if inter:
            out=blank(h,w,0); place(out, inter, 8); return out
        A=expand_with_stencil(A, PLUS, (h,w))
        B=expand_with_stencil(B, PLUS, (h,w))
    raise ValueError("no meet")
```


## S17_H4 — Pick the Object Whose Halo Seals the Hole
**Skills:** hole counting, topological effect of dilation, selection by after-minus-before behavior

**Primitive note:** Square growth can change topology by shrinking or eliminating holes; this puzzle selects the object whose hole count drops.

**Scaffold:**

- Separate the objects and count their holes before growth.
- Square-grow each object by one step and count holes again.
- Choose the object whose hole count decreases and output its original shape, cropped in 8.

**Train 1 input**

```text
000000000000000
022200002222200
020200002000200
022200002000200
000000002000200
000000002222200
000000000000000
000000000000000
000000000000000
```
**Train 1 output**

```text
888
808
888
```
**Train 2 input**

```text
0000000000000000
0000000002220000
0222220002020000
0200020002220000
0200020000000000
0200020000000000
0222220000000000
0000000000000000
0000000000000000
0000000000000000
```
**Train 2 output**

```text
888
808
888
```
**Test input**

```text
000000000000000000
000000000222220000
002220000200020000
002020000200020000
002220000200020000
000000000222220000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Expected test output**

```text
888
808
888
```
**Written solution**

Some hollow shapes stay hollow after one square-expansion step, while a smaller hole can be sealed completely. Compare each object before and after growth. The correct choice is the object whose number of holes goes down; output the original chosen object, cropped and recolored to 8.

**Reference program**

```python
def solve_S17_H4(grid):
    h,w=dims(grid)
    comps=[comp for comp in components(grid) if comp["color"]!=0]
    chosen=None
    for comp in comps:
        before=hole_count_shape(comp["cells"])
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        after=hole_count_shape(list(grown))
        if after < before:
            # choose max drop, then smaller area
            key=(before-after, -len(comp["cells"]))
            if chosen is None or key > chosen[0]:
                chosen=(key, comp["cells"])
    assert chosen is not None
    return crop_cells(chosen[1],8)
```


## S17_H5 — Color-Labeled Stencil Library
**Skills:** library extraction, color-keyed rule lookup, multiple arbitrary stencils in one grid

**Primitive note:** This is a generalization of H1: several stencil patterns are stored in the top band, keyed by color, and must be applied to matching seeds below.

**Scaffold:**

- Read each library panel in the top band: the 9 marks the anchor and the colored cells define that color’s offsets.
- Build a separate stencil for each color key.
- For every lower seed of color 2, 3, or 4, stamp the matching stencil in that same color.

**Train 1 input**

```text
00000900000900000
00200903000900400
00920900900904900
00000900030900400
00000900000900000
00000000000000000
00000000000000000
00200000300000000
00000000000000400
00002000000000000
00000000000000000
00000000000000000
```
**Train 1 output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00200003000000000
00020000000000400
00002000030004000
00000200000000400
00000000000000000
00000000000000000
```
**Train 2 input**

```text
00000900000900000
02000900300904400
02900900930904900
02000900000900400
00000900000900000
00000000000000000
00000000000000000
00000000003000000
00020000000000040
00000000000030000
00000000000000000
00000000000000000
```
**Train 2 output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000003000000
00200000000300440
00200000000030400
00200000000003040
00000000000000000
00000000000000000
```
**Test input**

```text
00000900000900000
00200903000900400
02900900930900940
00000903000900400
00000900000900000
00000000000000000
00000000000000000
00020000000000004
00000000003000000
00000000000000040
00000000000000000
00000000000000000
00000000000000000
```
**Expected test output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00020000000000004
00200000030000000
00000000000300044
00000000030000004
00000000000000040
00000000000000000
00000000000000000
```
**Written solution**

The top band is a dictionary of stencils. In each small library panel, the 9 is the anchor and the surrounding colored cells show the offsets that belong to that color’s pattern. Below the library, every seed of that color should receive the corresponding stamp. The output is the union of all those color-specific stamps.

**Reference program**

```python
def solve_S17_H5(grid):
    h,w=dims(grid)
    band=[row[:] for row in grid[:5]]
    panels=panel_split_vertical(band, sep=9)
    stencil_by_color={}
    for a,b,p in panels:
        nz=[(r,c,v) for r,c,v in nonzero(p)]
        anchor=[(r,c) for r,c,v in nz if v==9][0]
        colors=sorted({v for r,c,v in nz if v not in {0,9}})
        assert len(colors)==1
        color=colors[0]
        offsets=[(r-anchor[0], c-anchor[1]) for r,c,v in nz if v==color]
        stencil_by_color[color]=offsets
    out=blank(h,w,0)
    for r,c,v in nonzero(grid):
        if r<5: # library band
            continue
        if v in stencil_by_color:
            place(out, expand_with_stencil([(r,c)], stencil_by_color[v], (h,w)), v)
    return out
```


## S17_H6 — Mask-Selected by Hypothetical Growth
**Skills:** counterfactual overlap scoring, object selection, mask interaction

**Primitive note:** Objects are ranked by how much their one-step square growth would overlap a fixed mask region.

**Scaffold:**

- Keep the color-1 cells as the fixed mask.
- Separate the color-2 objects and square-grow each one.
- Choose the object whose grown region overlaps the mask the most, then output the original object cropped in 8.

**Train 1 input**

```text
000000000000
000000000000
002000001100
000000000100
000000000000
000000000000
000000022000
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
88
```
**Train 2 input**

```text
0000000000000
0000000000000
0000000020000
0000000000000
0000000000000
0011000200000
0010000220000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**

```text
80
88
```
**Test input**

```text
0000000000000
0000000000000
0020000000000
0000000000200
0000000002200
0000000000000
0000002200000
0000000011000
0000000011000
0000000000000
0000000000000
```
**Expected test output**

```text
88
```
**Written solution**

The mask is not something to copy directly. Instead, use it to score the candidate objects. For each color-2 object, imagine its one-step 3×3 growth and count how many cells of that hypothetical grown region would fall on the color-1 mask. Pick the best-scoring object and output the original object, cropped and recolored to 8.

**Reference program**

```python
def solve_S17_H6(grid):
    h,w=dims(grid)
    mask={(r,c) for r,c,v in nonzero(grid) if v==1}
    comps=[comp for comp in components([[2 if v==2 else 0 for v in row] for row in grid]) if comp["color"]==2]
    best=None
    best_comp=None
    for comp in comps:
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        overlap=len(grown & mask)
        key=(overlap, len(grown), -len(comp["cells"]))
        if best is None or key>best:
            best=key; best_comp=comp["cells"]
    return crop_cells(best_comp,8)
```


## S17_H7 — Growth Contact Matrix
**Skills:** symbolic matrix construction, pairwise growth comparison, multi-group reasoning

**Primitive note:** Square growth becomes a relation: for each pair of colored groups, ask whether their grown regions touch.

**Scaffold:**

- Group the seeds by color in sorted color order.
- Square-grow each color group by one step.
- Build a small matrix: put 5 on the diagonal, and put 8 wherever two different grown groups overlap.

**Train 1 input**

```text
000000000
000000000
002030000
000000000
000000000
000000000
000000400
000000000
000000000
```
**Train 1 output**

```text
580
850
005
```
**Train 2 input**

```text
000000000
000000000
002000400
000000000
000000000
000003000
000000000
000000000
000000000
```
**Train 2 output**

```text
500
050
005
```
**Test input**

```text
0000000000
0000000000
0020400000
0000000000
0000000000
0000000000
0000003000
0000000000
0000000000
0000000000
```
**Expected test output**

```text
508
050
805
```
**Written solution**

There are three colored groups. Expand each group by one square-growth step, then compare them pairwise. The output is a small contact matrix ordered by color: every group relates to itself on the diagonal with 5, and any off-diagonal pair gets an 8 exactly when the two grown regions overlap.

**Reference program**

```python
def solve_S17_H7(grid):
    h,w=dims(grid)
    groups=defaultdict(list)
    for r,c,v in nonzero(grid):
        groups[v].append((r,c))
    colors=sorted(groups)
    cell_groups=[groups[c] for c in colors]
    return matrix_of_contacts(cell_groups, SQ1, (h,w))
```
