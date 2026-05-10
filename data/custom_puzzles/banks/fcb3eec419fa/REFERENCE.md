# ARC-style Puzzle Bank — 21 more puzzles (set 23)
This twenty-third bank leans into **regular tile lattices, tile voting, library lookup, and tile algebra**. The common move is to stop treating the board as one undifferentiated canvas and instead parse it as a macro-grid of equal-sized local boards separated by divider lines. Once the tile lattice is known, you can count, compare, rotate, reorder, vote over, match, and assemble whole tiles.
The core primitive introduced here is:
```text
tile_lattice(grid, divider_color=9)
Parse a regular lattice of equal-sized tiles separated by full divider rows and columns.
Use the resulting macro-grid of local boards as the main object of reasoning.
```
The reference programs assume the shared helpers in `arc_puzzle_bank_21_set23_reference.py`.
## Index
### Easy
- **S23_E1** — Count Nonzeros Per Tile
- **S23_E2** — Mark Centers for Main-Diagonal Corner Tiles
- **S23_E3** — Recolor the Densest Tile
- **S23_E4** — Copy the Source Motif to the Target Tile
- **S23_E5** — Majority Color Macro Grid
- **S23_E6** — Mirror Every Tile Horizontally
- **S23_E7** — Vertical-Symmetry Flag Strip
### Medium
- **S23_M1** — Rotate Only the Marked Tiles
- **S23_M2** — Cellwise Union of the Tile Row
- **S23_M3** — Copy Prototypes by Key Color
- **S23_M4** — Odd Tile Under Rotation
- **S23_M5** — Fill Each Tile's Bounding Box
- **S23_M6** — Sort Tiles by Occupancy Count
- **S23_M7** — Canonical Rotation per Tile
### Hard
- **S23_H1** — A:B::C:? Rotation Candidate
- **S23_H2** — Rotation-Congruence Matrix
- **S23_H3** — Majority-Repair Tile from Noisy Copies
- **S23_H4** — Prototype Label Lookup Under Rotation
- **S23_H5** — Missing Tile by Cellwise XOR
- **S23_H6** — Continue the Rotation Sequence
- **S23_H7** — Assemble the Mosaic by Edge Matching
## S23_E1 — Count Nonzeros Per Tile
**Skills:** tile extraction, per-tile counting, reduced macro output

**Primitive note:** Each tile becomes one macro cell. The divider lattice tells you which local cells belong together before you count anything.

**Scaffold:**

- Parse the divider lines into a regular tile grid.
- Count the nonzero cells inside each tile.
- Write those counts into a smaller grid with the same tile-row and tile-column layout.

**Train 1 input**
```text
10911900
01910900
99999999
10911911
00901911
```
**Train 1 output**
```text
230
134
```
**Train 2 input**
```text
01911910
00900910
99999999
11900911
10901901
```
**Train 2 output**
```text
122
313
```
**Test input**
```text
10900911
11900911
99999999
01910911
01900910
```
**Test output**
```text
304
213
```
**Written solution**

Split the board into its regular tiles. For each tile, count how many cells are nonzero, and place that number into the corresponding position of a reduced macro grid.

**Reference program**
```python
def solve_S23_E1(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[]
    for row in tiles:
        out.append([nonzero_count(t) for t in row])
    return out
```
## S23_E2 — Mark Centers for Main-Diagonal Corner Tiles
**Skills:** tile-local condition checks, same-size output, corner reasoning

**Primitive note:** The rule is purely local to each tile: only tiles whose top-left and bottom-right corners are occupied get changed.

**Scaffold:**

- Inspect each tile on its own.
- Check whether the top-left and bottom-right corners are nonzero.
- If they are, color that tile's center cell 8 and leave everything else alone.

**Train 1 input**
```text
2029002
0009200
0029200
9999999
2009020
0009002
2029000
```
**Train 1 output**
```text
2029002
0809200
0029200
9999999
2009020
0809002
2029000
```
**Train 2 input**
```text
2009002
0029000
0029200
9999999
2209000
0009020
0029200
```
**Train 2 output**
```text
2009002
0829000
0029200
9999999
2209000
0809020
0029200
```
**Test input**
```text
2009002
0009002
0029200
9999999
2209020
0009000
0029020
```
**Test output**
```text
2009002
0809002
0029200
9999999
2209020
0809000
0029020
```
**Written solution**

Look at each tile separately. Whenever a tile has nonzero cells in its top-left and bottom-right corners, mark the center of that tile with 8; otherwise keep the tile unchanged.

**Reference program**
```python
def solve_S23_E2(grid):
    tiles, _, _ = tile_lattice(grid)
    out_tiles=[]
    for row in tiles:
        out_row=[]
        for t in row:
            x=copy_grid(t)
            if t[0][0]!=0 and t[2][2]!=0:
                x[1][1]=8
            out_row.append(x)
        out_tiles.append(out_row)
    return assemble_tiles(out_tiles)
```
## S23_E3 — Recolor the Densest Tile
**Skills:** cross-tile comparison, counting, same-size selective recoloring

**Primitive note:** After the tiles are parsed, the only global step is to compare how many nonzero cells each tile contains and find the unique maximum.

**Scaffold:**

- Split the board into tiles.
- Count how many nonzero cells are in each tile.
- Find the unique densest tile and recolor all of its nonzero cells to 8.

**Train 1 input**
```text
2009200
0009200
0029220
9999999
0209220
2229200
0209000
```
**Train 1 output**
```text
2009200
0009200
0029220
9999999
0809220
8889200
0809000
```
**Train 2 input**
```text
0209222
0209020
0009020
9999999
2009220
2009002
2009002
```
**Train 2 output**
```text
0209888
0209080
0009080
9999999
2009220
2009002
2009002
```
**Test input**
```text
2009020
0009020
2029000
9999999
0209200
2229220
0209020
```
**Test output**
```text
2009020
0009020
2029000
9999999
0809200
8889220
0809020
```
**Written solution**

Count the nonzero cells in every tile, identify the tile with the largest count, and recolor only the nonzero cells of that tile to 8. Leave the other tiles unchanged.

**Reference program**
```python
def solve_S23_E3(grid):
    tiles, _, _ = tile_lattice(grid)
    counts=[nonzero_count(t) for row in tiles for t in row]
    idx=max(range(len(counts)), key=lambda i: counts[i])
    flat=[copy_grid(t) for row in tiles for t in row]
    best=flat[idx]
    flat2=[]
    for i,t in enumerate(flat):
        if i==idx:
            flat2.append([[8 if v!=0 else 0 for v in row] for row in t])
        else:
            flat2.append(copy_grid(t))
    rows=len(tiles); cols=len(tiles[0])
    return assemble_from_flat(flat2, rows, cols)
```
## S23_E4 — Copy the Source Motif to the Target Tile
**Skills:** source-target transfer, tile selection, motif copying

**Primitive note:** The tile lattice makes it easy to separate source, target, and distractor tiles before any copying happens.

**Scaffold:**

- Find the tile that contains the actual motif in color 2.
- Find the target tile marked by color 3.
- Copy the source occupancy pattern into the target tile using color 8.

**Train 1 input**
```text
22090009100
20090309010
00090009001
```
**Train 1 output**
```text
22098809100
20098009010
00090009001
```
**Train 2 input**
```text
00090019200
03090109200
00091009220
```
**Train 2 output**
```text
80090019200
80090109200
88091009220
```
**Test input**
```text
01092209000
01090229030
01090009000
```
**Test output**
```text
01092209880
01090229088
01090009000
```
**Written solution**

Identify the source tile by its color-2 motif and the target tile by its color-3 marker. Then copy the source shape into the target tile, recoloring the copied cells to 8.

**Reference program**
```python
def solve_S23_E4(grid):
    flat, rows, cols = flat_tiles(grid)
    # source tile: most color-2 cells
    src_idx=max(range(len(flat)), key=lambda i: sum(v==2 for row in flat[i] for v in row))
    tgt_idx=[i for i,t in enumerate(flat) if any(v==3 for row in t for v in row)][0]
    src=flat[src_idx]
    out=[copy_grid(t) for t in flat]
    newt=blank(*dims(src),0)
    for r,row in enumerate(src):
        for c,v in enumerate(row):
            if v==2:
                newt[r][c]=8
    out[tgt_idx]=newt
    return assemble_from_flat(out, rows, cols)
```
## S23_E5 — Majority Color Macro Grid
**Skills:** tile summarization, color counting, reduced output

**Primitive note:** Each tile collapses to one macro color: whichever nonzero color appears most often inside that tile.

**Scaffold:**

- Parse the tiles.
- Count the frequency of each nonzero color inside each tile.
- Output a reduced grid whose cell is the tile's majority nonzero color.

**Train 1 input**
```text
11922
20921
99999
12921
11922
```
**Train 1 output**
```text
12
12
```
**Train 2 input**
```text
21911
22921
99999
22912
10911
```
**Train 2 output**
```text
21
21
```
**Test input**
```text
12922
11912
99999
21911
22912
```
**Test output**
```text
12
21
```
**Written solution**

Treat each tile as one summary cell. For each tile, count its nonzero colors and output the most frequent one in the corresponding macro position.

**Reference program**
```python
def solve_S23_E5(grid):
    tiles, _, _ = tile_lattice(grid)
    return [[majority_nonzero_color(t) for t in row] for row in tiles]
```
## S23_E6 — Mirror Every Tile Horizontally
**Skills:** within-tile transforms, regular tiling, same-size output

**Primitive note:** The macro layout stays fixed; only the contents of each tile are reflected left-to-right inside their own local coordinates.

**Scaffold:**

- Keep the divider structure exactly as it is.
- Reflect each tile across its own vertical axis.
- Reassemble the mirrored tiles in the original macro positions.

**Train 1 input**
```text
40094409440
40094009044
44090009000
```
**Train 1 output**
```text
00490449044
00490049440
04490009000
```
**Train 2 input**
```text
44094449400
00490409040
00490409004
```
**Train 2 output**
```text
04494449004
40090409040
40090409400
```
**Test input**
```text
00490049000
04090049444
40090449000
```
**Test output**
```text
40094009000
04094009444
00494409000
```
**Written solution**

Mirror each tile left-to-right within its own local 3×3 frame and put the reflected tile back in the same place.

**Reference program**
```python
def solve_S23_E6(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[[flip_h(t) for t in row] for row in tiles]
    return assemble_tiles(out)
```
## S23_E7 — Vertical-Symmetry Flag Strip
**Skills:** symmetry detection, tile classification, symbolic output

**Primitive note:** Each tile is tested independently for left-right symmetry, then the results are summarized in a small strip.

**Scaffold:**

- Inspect each tile separately.
- Check whether the tile is unchanged by horizontal mirroring.
- Output 8 for symmetric tiles and 0 for the others.

**Train 1 input**
```text
020920090209220
222920090209200
020922090209000
```
**Train 1 output**
```text
8080
```
**Train 2 input**
```text
222922092029002
020902290209002
020900090009022
```
**Train 2 output**
```text
8080
```
**Test input**
```text
202900290209220
202902090209002
020920090209002
```
**Test output**
```text
8080
```
**Written solution**

For each tile, test whether it is vertically symmetric. Produce a one-row strip whose entries are 8 exactly at the positions of the symmetric tiles.

**Reference program**
```python
def solve_S23_E7(grid):
    flat, rows, cols = flat_tiles(grid)
    out=blank(rows, cols, 0)
    idx=0
    for r in range(rows):
        for c in range(cols):
            if vertical_symmetry(flat[idx]):
                out[r][c]=8
            idx+=1
    return out
```
## S23_M1 — Rotate Only the Marked Tiles
**Skills:** conditional tile transforms, rotation, marker-controlled rules

**Primitive note:** Markers act at tile level: the motif is always the color-2 pattern, but only marked tiles get rotated.

**Scaffold:**

- Within each tile, separate the color-2 motif from any color-3 marker.
- If a tile contains a marker, rotate the motif 90° clockwise.
- Output only the resulting motif, recolored to 8.

**Train 1 input**
```text
20092209220
23092009032
22090009000
```
**Train 1 output**
```text
88898809008
80098009008
00090009080
```
**Train 2 input**
```text
22090029222
00290309020
00292009020
```
**Train 2 output**
```text
88098009888
00890009080
00890089080
```
**Test input**
```text
22092009002
23090209032
00090029022
```
**Test output**
```text
08898009000
00890809800
00090089888
```
**Written solution**

Read the color-2 cells as the motif in each tile. Tiles containing a color-3 marker should have that motif rotated 90° clockwise; unmarked tiles keep the motif as-is. The output uses color 8 for the resulting motif and removes the markers.

**Reference program**
```python
def solve_S23_M1(grid):
    flat, rows, cols = flat_tiles(grid)
    out=[]
    for t in flat:
        motif=[[1 if v==2 else 0 for v in row] for row in t]
        tile=colorize_occ(motif,8)
        if any(v==3 for row in t for v in row):
            tile=rot90(tile)
        out.append(tile)
    return assemble_from_flat(out, rows, cols)
```
## S23_M2 — Cellwise Union of the Tile Row
**Skills:** cross-tile aggregation, superposition, reduced output

**Primitive note:** The tile grid is just the container; the output is a single tile built by combining all tile occupancies cellwise.

**Scaffold:**

- Extract every tile in the row.
- Take the union of their occupied cells, position by position.
- Output a single tile with 8 wherever any input tile was occupied.

**Train 1 input**
```text
22090209002
20090209020
00090209200
```
**Train 1 output**
```text
888
880
880
```
**Train 2 input**
```text
20092009222
20090209020
22090029020
```
**Train 2 output**
```text
888
880
888
```
**Test input**
```text
22092209202
02290029020
00090029000
```
**Test output**
```text
888
088
008
```
**Written solution**

Overlay all tiles cell by cell. Any location occupied in at least one input tile becomes 8 in the single output tile.

**Reference program**
```python
def solve_S23_M2(grid):
    flat, rows, cols = flat_tiles(grid)
    h,w=dims(flat[0])
    out=blank(h,w,0)
    for t in flat:
        for r in range(h):
            for c in range(w):
                if t[r][c]!=0:
                    out[r][c]=8
    return out
```
## S23_M3 — Copy Prototypes by Key Color
**Skills:** tile library lookup, key-value matching, source-to-query transfer

**Primitive note:** The top tile row behaves like a little dictionary: key colors identify prototype motifs that must be copied into the query tiles below.

**Scaffold:**

- Read the top row as key→prototype pairs.
- For each bottom-row query tile, find its key color.
- Copy the matching prototype motif into that query position using color 8.

**Train 1 input**
```text
12094209620
20090209022
00090209000
99999999999
00090009000
06090109040
00090009000
```
**Train 1 output**
```text
12094209620
20090209022
00090209000
99999999999
08090809080
08898009080
00090009080
```
**Train 2 input**
```text
20095029722
20090209020
22092009020
99999999999
00090009000
05090709020
00090009000
```
**Train 2 output**
```text
20095029722
20090209020
22092009020
99999999999
00890889800
08090809800
80090809880
```
**Test input**
```text
32094009802
00290209020
00290029000
99999999999
00090009000
08090309040
00090009000
```
**Test output**
```text
32094009802
00290209020
00290029000
99999999999
00890809000
08090089080
00090089008
```
**Written solution**

Use the top row as a lookup library. Each prototype tile is labeled by its key color, and each bottom query tile names one key. Replace each query tile with the corresponding prototype motif, recolored to 8.

**Reference program**
```python
def solve_S23_M3(grid):
    tiles, _, _ = tile_lattice(grid)
    top=tiles[0]
    bottom=tiles[1]
    lib={}
    for t in top:
        key=t[0][0]
        lib[key]=[[1 if (v==2 or (v!=0 and (r,c)!=(0,0) and v!=key)) else 0 for c,v in enumerate(row)] for r,row in enumerate(t)]
        # but keep only motif nonzero excluding key
        lib[key]=[[1 if (v==2) else 0 for v in row] for row in t]
    out=[ [copy_grid(t) for t in top], [] ]
    for q in bottom:
        key=max(v for row in q for v in row)
        motif=lib[key]
        out[1].append(colorize_occ(motif,8))
    return assemble_tiles(out)
```
## S23_M4 — Odd Tile Under Rotation
**Skills:** equivalence classes, rotation invariance, symbolic output

**Primitive note:** The important comparison is not exact equality but equality up to rotation.

**Scaffold:**

- Canonicalize each tile up to 90° rotations.
- Find the equivalence class that appears only once.
- Output a one-hot strip marking that odd tile.

**Train 1 input**
```text
200922292229022
200920090209002
220900090209002
```
**Train 1 output**
```text
0080
```
**Train 2 input**
```text
200922090029200
020902290209020
002900092009002
```
**Train 2 output**
```text
0800
```
**Test input**
```text
220900292009002
002900292009020
002922090229200
```
**Test output**
```text
0008
```
**Written solution**

Group the tiles by shape up to rotation. Three tiles belong to the same rotation class and one does not, so output a strip with 8 at the odd tile's position.

**Reference program**
```python
def solve_S23_M4(grid):
    flat, rows, cols = flat_tiles(grid)
    # find class by canonical rotation
    reps=[flatten(canonical_rotation([[1 if v!=0 else 0 for v in row] for row in t])) for t in flat]
    freq=Counter(reps)
    odd_idx=[i for i,r in enumerate(reps) if freq[r]==1][0]
    return one_hot(len(flat), odd_idx)
```
## S23_M5 — Fill Each Tile's Bounding Box
**Skills:** object enclosure, local geometry, same-size output

**Primitive note:** The bounding-box computation happens independently inside each tile rather than across the whole board.

**Scaffold:**

- Within each tile, locate all nonzero cells.
- Compute the smallest axis-aligned box containing them.
- Fill that box with 8 and do it independently for every tile.

**Train 1 input**
```text
2009002
0209000
0009002
9999999
0209000
0009002
2009020
```
**Train 1 output**
```text
8809008
8809008
0009008
9999999
8809000
8809088
8809088
```
**Train 2 input**
```text
2009000
0009202
0209000
9999999
0029020
0009000
2009020
```
**Train 2 output**
```text
8809000
8809888
8809000
9999999
8889080
8889080
8889080
```
**Test input**
```text
0209200
0029000
0009002
9999999
0009002
2009020
0209000
```
**Test output**
```text
0889888
0889888
0009888
9999999
0009088
8809088
8809000
```
**Written solution**

For each tile, find the bounding box of its occupied cells and replace the tile by that filled rectangle in color 8.

**Reference program**
```python
def solve_S23_M5(grid):
    tiles, _, _ = tile_lattice(grid)
    out=[[bbox_fill(t,8) for t in row] for row in tiles]
    return assemble_tiles(out)
```
## S23_M6 — Sort Tiles by Occupancy Count
**Skills:** cross-tile ordering, stable comparison, macro rearrangement

**Primitive note:** The tile lattice gives a row of comparable objects that must be reordered rather than transformed internally.

**Scaffold:**

- Count the nonzero cells in each tile.
- Sort the tiles from smallest count to largest count.
- Output the same tiles in that new left-to-right order.

**Train 1 input**
```text
20092009200
02090009000
20290009002
```
**Train 1 output**
```text
20092009200
00090009020
00090029202
```
**Train 2 input**
```text
02090009220
02090009000
02090029000
```
**Train 2 output**
```text
00092209020
00090009020
00290009020
```
**Test input**
```text
20090029020
20090209000
00092029000
```
**Test output**
```text
02092009002
00092009020
00090009202
```
**Written solution**

Ignore the original left-to-right order, count how many cells are occupied in each tile, and reorder the whole row from sparsest tile to densest tile.

**Reference program**
```python
def solve_S23_M6(grid):
    flat, rows, cols = flat_tiles(grid)
    assert rows==1
    ordered=sorted(flat, key=lambda t:(nonzero_count(t), flatten(t)))
    return assemble_from_flat(ordered, 1, cols)
```
## S23_M7 — Canonical Rotation per Tile
**Skills:** normalization, rotation search, same-size output

**Primitive note:** Each tile is independently rotated into a canonical representative, so equivalent tiles end up aligned the same way.

**Scaffold:**

- Consider the four 90° rotations of each tile.
- Pick the canonical one, for example the lexicographically smallest flattened pattern.
- Replace the tile by that canonical rotation.

**Train 1 input**
```text
22292009002
20092009020
00090229200
```
**Train 1 output**
```text
00090029002
00290029020
22292209200
```
**Train 2 input**
```text
20090009020
02090029220
00290229200
```
**Train 2 output**
```text
00290009000
02090029220
20090229022
```
**Test input**
```text
00090209200
20090209020
22292229200
```
**Test output**
```text
00090029000
20092229020
22290029202
```
**Written solution**

Normalize each tile under rotation by trying all four 90° rotations and choosing a single canonical orientation. Output every tile in that canonical pose.

**Reference program**
```python
def solve_S23_M7(grid):
    flat, rows, cols = flat_tiles(grid)
    out=[canonical_rotation(t) for t in flat]
    return assemble_from_flat(out, rows, cols)
```
## S23_H1 — A:B::C:? Rotation Candidate
**Skills:** analogy, relational reasoning, candidate selection

**Primitive note:** The top row shows the relation explicitly: B is the 90° clockwise rotation of A. The same relation must be applied to C to choose the right candidate.

**Scaffold:**

- Infer the top-row relation from A to B.
- Apply that same relation to tile C.
- Choose the candidate tile that matches and output a one-hot strip.

**Train 1 input**
```text
20092229220
20092009200
22090009000
99999999999
02290009222
00290029020
00090229020
```
**Train 1 output**
```text
800
```
**Train 2 input**
```text
22090029222
02290229020
00090209020
99999999999
20090029220
02092229200
00290029000
```
**Train 2 output**
```text
080
```
**Test input**
```text
22090029000
00290029002
00292209022
99999999999
22092009000
20090209200
00090029220
```
**Test output**
```text
008
```
**Written solution**

Read the top row as an analogy: B is A rotated 90° clockwise. Therefore the correct candidate is the one that equals C rotated 90° clockwise. Mark that candidate with 8 in a one-hot strip.

**Reference program**
```python
def solve_S23_H1(grid):
    tiles, _, _ = tile_lattice(grid)
    A,B,C = tiles[0]
    cands = tiles[1]
    target=rot90([[1 if v!=0 else 0 for v in row] for row in C])
    idx=[i for i,t in enumerate(cands) if [[1 if v!=0 else 0 for v in row] for row in t]==target][0]
    return one_hot(len(cands), idx)
```
## S23_H2 — Rotation-Congruence Matrix
**Skills:** symbolic outputs, pairwise comparison, rotation classes

**Primitive note:** The output is a relation matrix over tiles: each entry says whether two tiles belong to the same rotation class.

**Scaffold:**

- Canonicalize every tile up to rotation.
- Compare every pair of canonical forms.
- Write 8 in the matrix exactly where the two tiles are rotation-congruent.

**Train 1 input**
```text
20090229200
20090029020
22090029002
```
**Train 1 output**
```text
880
880
008
```
**Train 2 input**
```text
22092229000
02290209220
00090209022
```
**Train 2 output**
```text
808
080
808
```
**Test input**
```text
02290029000
00290209200
00092009220
```
**Test output**
```text
808
080
808
```
**Written solution**

Compare each tile to every other tile up to 90° rotation. The output matrix has 8 where two tiles are equivalent under rotation and 0 elsewhere.

**Reference program**
```python
def solve_S23_H2(grid):
    flat, rows, cols = flat_tiles(grid)
    n=len(flat)
    reps=[canonical_rotation([[1 if v!=0 else 0 for v in row] for row in t]) for t in flat]
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if reps[i]==reps[j]:
                out[i][j]=8
    return out
```
## S23_H3 — Majority-Repair Tile from Noisy Copies
**Skills:** consensus reasoning, denoising, cross-tile voting

**Primitive note:** No single tile has to be trusted completely; the intended shape is recovered by voting cellwise across several noisy versions.

**Scaffold:**

- Overlay the noisy copies in tile coordinates.
- For each cell, ask whether a clear majority of copies occupy it.
- Build one repaired tile from those majority decisions using color 8.

**Train 1 input**
```text
2009200
2009200
2209200
9999999
2009202
2009200
2209220
```
**Train 1 output**
```text
800
800
880
```
**Train 2 input**
```text
2229222
0209000
0209020
9999999
2229222
0209020
0229020
```
**Train 2 output**
```text
888
080
080
```
**Test input**
```text
2209220
0229022
0009200
9999999
2209220
0209022
0009000
```
**Test output**
```text
880
088
000
```
**Written solution**

Treat the input tiles as noisy copies of one intended motif. Recover the motif by cellwise majority vote and output that repaired tile in color 8.

**Reference program**
```python
def solve_S23_H3(grid):
    flat, rows, cols = flat_tiles(grid)
    h,w=dims(flat[0])
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for t in flat if t[r][c]!=0)
            if cnt>=3:
                out[r][c]=8
    return out
```
## S23_H4 — Prototype Label Lookup Under Rotation
**Skills:** library lookup, rotation invariance, symbolic labeling

**Primitive note:** Prototype tiles are labeled, but queries are unlabeled rotated copies. So matching has to happen after canonicalizing the shapes.

**Scaffold:**

- Read the top row as labeled prototype tiles.
- Normalize both prototypes and queries up to rotation.
- For each query, output the label color of the matching prototype.

**Train 1 input**
```text
120930295029722
020902090229002
020920090209000
999999999999999
000902092209200
220902092009020
022902090009002
```
**Train 1 output**
```text
5173
```
**Train 2 input**
```text
220942296029802
020900292229020
020900090029200
999999999999999
200900090209200
020900290209222
002902290209200
```
**Train 2 output**
```text
8426
```
**Test input**
```text
102922094229622
022902092009002
020902090229000
999999999999999
000922090209000
200902292029222
220900092029000
```
**Test output**
```text
6142
```
**Written solution**

Use the top row as a labeled library of shapes. Each bottom query is a rotated copy of one prototype, so canonicalize by rotation, match it to the library, and output the matching prototype's label color in a strip.

**Reference program**
```python
def solve_S23_H4(grid):
    tiles, _, _ = tile_lattice(grid)
    top=tiles[0]
    bottom=tiles[1]
    proto=[]
    for t in top:
        label=t[0][0]
        motif=[[1 if (v!=0 and not (r==0 and c==0)) else 0 for c,v in enumerate(row)] for r,row in enumerate(t)]
        proto.append((label, canonical_rotation(motif)))
    out=[]
    for q in bottom:
        qcan=canonical_rotation([[1 if v!=0 else 0 for v in row] for row in q])
        label=[lab for lab,can in proto if can==qcan][0]
        out.append(label)
    return [out]
```
## S23_H5 — Missing Tile by Cellwise XOR
**Skills:** matrix reasoning, boolean composition, reduced output

**Primitive note:** The three visible tiles combine cellwise with XOR to define the missing fourth tile.

**Scaffold:**

- Align the three visible tiles cell by cell.
- For each location, take odd parity of occupancy across the three tiles.
- Output that parity pattern as the missing tile in color 8.

**Train 1 input**
```text
2209020
2009020
0009020
9999999
0029000
0209030
2009000
```
**Train 1 output**
```text
808
800
880
```
**Train 2 input**
```text
2229200
2009020
0009002
9999999
0029000
2229030
0029000
```
**Train 2 output**
```text
080
008
000
```
**Test input**
```text
2209002
0229002
0009220
9999999
0229000
0029030
0009000
```
**Test output**
```text
800
088
880
```
**Written solution**

Compute the missing tile by taking the cellwise XOR of the three visible tiles: a cell is present exactly when an odd number of the visible tiles occupy that position.

**Reference program**
```python
def solve_S23_H5(grid):
    tiles, _, _ = tile_lattice(grid)
    A=tiles[0][0]; B=tiles[0][1]; C=tiles[1][0]
    h,w=dims(A)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            bit=((A[r][c]!=0) ^ (B[r][c]!=0) ^ (C[r][c]!=0))
            if bit:
                out[r][c]=8
    return out
```
## S23_H6 — Continue the Rotation Sequence
**Skills:** sequence extrapolation, repeated transforms, missing-tile completion

**Primitive note:** This is a local sequence over tiles: each tile is the 90° clockwise rotation of the previous one.

**Scaffold:**

- Observe the rotation step from one tile to the next.
- Apply that same 90° clockwise step once more to the third tile.
- Output the missing fourth tile in color 8.

**Train 1 input**
```text
200922290229000
200920090029030
220900090029000
```
**Train 1 output**
```text
000
008
888
```
**Train 2 input**
```text
022900090009000
002900292009030
000902292209000
```
**Train 2 output**
```text
880
800
000
```
**Test input**
```text
220900292009000
002900292009030
002922090229000
```
**Test output**
```text
088
800
800
```
**Written solution**

The tiles form a rotation sequence, each one rotating 90° clockwise from the previous tile. Rotate the third tile once more to get the missing fourth tile, then output it in color 8.

**Reference program**
```python
def solve_S23_H6(grid):
    flat, rows, cols = flat_tiles(grid)
    # first three are sequence, last is blank
    return colorize_occ([[1 if v!=0 else 0 for v in row] for row in rot90(flat[2])],8)
```
## S23_H7 — Assemble the Mosaic by Edge Matching
**Skills:** search, global arrangement, rotations, combinatorial assembly

**Primitive note:** Every tile carries edge-center connector colors. The correct 2×2 mosaic is the arrangement and rotation where all touching edge-center colors agree.

**Scaffold:**

- For each tile, consider all four rotations.
- Search for a 2×2 arrangement where adjacent edge-center colors match.
- Output the assembled mosaic in that consistent orientation.

**Train 1 input**
```text
070906090709050
458957296329813
020901090409040
```
**Train 1 output**
```text
0109030
2759514
0609080
9999999
0609080
4379752
0209040
```
**Train 2 input**
```text
070905090509030
528936192149142
060904090809060
```
**Train 2 output**
```text
0209050
3469627
0109080
9999999
0109080
5649412
0309050
```
**Test input**
```text
080902090409050
263978495129641
070901090209030
```
**Test output**
```text
0209080
4129263
0509070
9999999
0509070
6419182
0309040
```
**Written solution**

Rotate and permute the tiles until the touching edge-center colors match across both internal boundaries of a 2×2 mosaic. Output that assembled mosaic.

**Reference program**
```python
def solve_S23_H7(grid):
    flat, rows, cols = flat_tiles(grid)
    # search arrangement 2x2 with rotations
    indices=range(len(flat))
    rots=[lambda x:x, rot90, rot180, rot270]
    best=None
    for perm in itertools.permutations(indices,4):
        for ks in itertools.product(range(4), repeat=4):
            arr=[rotk(flat[perm[i]], ks[i]) for i in range(4)]
            t0,t1,t2,t3=arr
            # match right/left and bottom/top edge-center colors
            if t0[1][2]!=t1[1][0]: 
                continue
            if t2[1][2]!=t3[1][0]:
                continue
            if t0[2][1]!=t2[0][1]:
                continue
            if t1[2][1]!=t3[0][1]:
                continue
            cand=assemble_tiles([[t0,t1],[t2,t3]])
            key=flatten(cand)
            if best is None or key<best[0]:
                best=(key,cand)
    if best is None:
        raise ValueError("no arrangement")
    return best[1]
```
