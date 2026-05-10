# ARC-style Puzzle Bank — 21 more puzzles (set 24)
This twenty-fourth bank leans into **onion-peeling depth maps, inner cores, thickness profiles, and layer-based analogy**. The common move is to stop reading a component only as a blob of color and instead convert it into an explicit depth image: which cells belong to the first peel layer, which belong to the second, which cells survive to the inner core, and how those depth profiles compare across panels, objects, and candidates.
The core primitive introduced here is:
```text
onion_layers(grid, colors=None, connectivity=4)
Repeatedly peel each connected nonzero component from the boundary inward and label each occupied cell by its peel depth.
```
The reference programs assume the shared helpers in `arc_puzzle_bank_21_set24_reference.py`.
## Index
### Easy
- **S24_E1** — Recolor the Outermost Layer
- **S24_E2** — Keep Only Each Component’s Deepest Cells
- **S24_E3** — Max-Depth Strip
- **S24_E4** — Odd–Even Layer Recolor
- **S24_E5** — Second-Layer Mask
- **S24_E6** — Keep the Thickest Component
- **S24_E7** — Crop to the Depth Map
### Medium
- **S24_M1** — Header Palette by Depth
- **S24_M2** — Match the Candidate by Layer Histogram
- **S24_M3** — Layer Histogram Strip
- **S24_M4** — Transfer the Layer Palette
- **S24_M5** — Count Components by Thickness Class
- **S24_M6** — Left-vs-Right Depth Report
- **S24_M7** — Sort Colors by Thickness
### Hard
- **S24_H1** — Plain : Layer-Colored :: Plain : ?
- **S24_H2** — Majority Repair, then Depth Map
- **S24_H3** — Thickness Congruence Matrix
- **S24_H4** — Prototype Key Lookup by Layer Signature
- **S24_H5** — Grow One More Onion Layer
- **S24_H6** — Match by Full Depth Map Under Rotation
- **S24_H7** — Common Core via Minimum Depth Map
## S24_E1 — Recolor the Outermost Layer
**Skills:** boundary peeling, same-size recolor, component-wise depth

**Primitive note:** The first peel layer is the boundary of each component. Once the onion depth map exists, “outermost cells” become the cells whose depth is 1.

**Scaffold:**

- Treat every nonzero component as a solid object.
- Peel each object from the outside inward to assign layer numbers.
- Recolor exactly the cells in layer 1 to 8 and leave deeper cells alone.

**Train 1 input**
```text
000000000000000
022222000000000
022222000003000
022222000033300
022222000333330
022222000033300
000000000003000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
088888000000000
082228000008000
082228000083800
082228000833380
088888000083800
000000000008000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
000000000000
004440000000
044444000000
044444000000
044444000000
004440000000
000000000000
000000006660
000000006660
000000006660
000000000000
000000000000
```
**Train 2 output**
```text
000000000000
008880000000
084448000000
084448000000
084448000000
008880000000
000000000000
000000008880
000000008680
000000008880
000000000000
000000000000
```
**Test input**
```text
000000000000000
000555000000000
000555000000000
055555550000000
055555550000200
055555550002220
000555000022222
000555000002220
000000000000200
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test output**
```text
000000000000000
000888000000000
000858000000000
088555880000000
085555580000800
088555880008280
000858000082228
000888000008280
000000000000800
000000000000000
000000000000000
000000000000000
000000000000000
```
**Written solution**

Compute onion layers for every nonzero component. Recolor all cells in depth 1, the outermost peel layer, to 8 while leaving deeper occupied cells unchanged.

**Reference program**
```python
def solve_S24_E1(grid):
    layers = onion_layers(grid)
    out = copy_grid(grid)
    for r, row in enumerate(layers):
        for c, d in enumerate(row):
            if d == 1:
                out[r][c] = 8
    return out
```
## S24_E2 — Keep Only Each Component’s Deepest Cells
**Skills:** inner-core detection, per-component maxima, same-size masking

**Primitive note:** The onion map tells you how far each occupied cell is from the boundary. The deepest cells are exactly the cells that realize the maximum depth inside a component.

**Scaffold:**

- Compute onion depth separately for each connected component.
- Find the maximum depth reached inside each component.
- Blank everything except the cells at that maximum depth, and color those surviving cells 8.

**Train 1 input**
```text
000000000000000
022222000000000
022222000003000
022222000033300
022222000333330
022222000033300
000000000003000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
000000000000000
000000000000000
000800000000000
000000000008000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
00000000000000000
00044400006666600
00044400066666660
04444444066666660
04444444066666660
04444444066666660
00044400066666660
00044400006666600
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Train 2 output**
```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00008000000080000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Test input**
```text
00000000000000000
02222222000000000
02222222000000000
02222222000050000
02222222000555000
02222222005555500
00000000055555550
00000000005555500
00000000000555000
00000000000050000
00000000000000000
00000000000000000
00000000000000000
```
**Test output**
```text
00000000000000000
00000000000000000
00000000000000000
00088800000000000
00000000000000000
00000000000000000
00000000000080000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Written solution**

For each component, find its deepest onion layer and keep only those cells. Output 8 on every cell that belongs to a component’s maximum depth, and 0 elsewhere.

**Reference program**
```python
def solve_S24_E2(grid):
    h, w = dims(grid)
    out = blank(h, w, 0)
    for comp in component_masks(grid):
        layers = onion_layers(comp)
        md = max((v for row in layers for v in row), default=0)
        for r in range(h):
            for c in range(w):
                if layers[r][c] == md and md > 0:
                    out[r][c] = 8
    return out
```
## S24_E3 — Max-Depth Strip
**Skills:** component ordering, reduced symbolic output, thickness measurement

**Primitive note:** The primitive collapses each object to one number: its maximum peel depth.

**Scaffold:**

- Read the components from left to right.
- For each component, compute its maximum onion depth.
- Write those depths into a one-row strip in the same left-to-right order.

**Train 1 input**
```text
0000000000000000000000000
0000000000000000000044400
0000000000003000000044400
0222000000033300004444444
0222000000333330004444444
0222000000033300004444444
0000000000003000000044400
0000000000000000000044400
0000000000000000000000000
```
**Train 1 output**
```text
234
```
**Train 2 input**
```text
000000000000000000000000000
000000000000000000000000000
000000000000000000000400000
000200000033333300004440000
002220000033333300044444000
022222000033333300444444400
002220000033333300044444000
000200000000000000004440000
000000000000000000000400000
000000000000000000000000000
000000000000000000000000000
```
**Train 2 output**
```text
324
```
**Test input**
```text
0000000000000000000000000
0000000000000000000000000
0222220000000000000444000
0222220000000000000444000
0222220000033300044444440
0022200000033300044444440
0022200000033300044444440
0000000000000000000444000
0000000000000000000444000
0000000000000000000000000
0000000000000000000000000
```
**Test output**
```text
324
```
**Written solution**

Order the nonzero components from left to right and compute each component’s maximum onion depth. Output those depths as a single horizontal row.

**Reference program**
```python
def solve_S24_E3(grid):
    vals = [max_depth(comp) for comp in component_masks(grid)]
    return [vals]
```
## S24_E4 — Odd–Even Layer Recolor
**Skills:** layer parity, same-size transform, depth labeling

**Primitive note:** Once every occupied cell has a peel depth, parity becomes a simple local label on top of that symbolic map.

**Scaffold:**

- Compute the onion depth of every occupied cell.
- Cells in odd-numbered layers become color 2.
- Cells in even-numbered layers become color 3; background stays 0.

**Train 1 input**
```text
000000000000000
055555000000000
055555000004000
055555000044400
055555000444440
055555000044400
000000000004000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
022222000000000
023332000002000
023232000023200
023332000232320
022222000023200
000000000002000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
000000000000000
000666000000000
000666000000000
066666660000000
066666660000000
066666660000000
000666000000000
000666000000000
000000000002220
000000000002220
000000000002220
000000000000000
000000000000000
```
**Train 2 output**
```text
000000000000000
000222000000000
000232000000000
022323220000000
023232320000000
022323220000000
000232000000000
000222000000000
000000000002220
000000000002320
000000000002220
000000000000000
000000000000000
```
**Test input**
```text
00000000000
00000000000
00077777000
00777777700
00777777700
00777777700
00777777700
00777777700
00077777000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000000000
00022222000
00233333200
00232223200
00232323200
00232223200
00233333200
00022222000
00000000000
00000000000
```
**Written solution**

Replace every occupied cell by its depth parity: odd onion layers become 2 and even onion layers become 3.

**Reference program**
```python
def solve_S24_E4(grid):
    layers = onion_layers(grid)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            d = layers[r][c]
            if d:
                out[r][c] = 2 if d % 2 == 1 else 3
    return out
```
## S24_E5 — Second-Layer Mask
**Skills:** selective masking, depth thresholding, same-size extraction

**Primitive note:** This uses the depth map as a selector: keep exactly depth 2 and ignore all other layers.

**Scaffold:**

- Peel each component inward and label the layers.
- Look only for cells with depth exactly 2.
- Output 8 on those cells and 0 everywhere else.

**Train 1 input**
```text
000000000000000
022222000000000
022222000003000
022222000033300
022222000333330
022222000033300
000000000003000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
000000000000000
008880000000000
008080000008000
008880000080800
000000000008000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
00000000000000000
00044400000000000
00044400000000000
04444444000000000
04444444000000000
04444444000000000
00044400000000000
00044400000000000
00000000000000000
00000000000666600
00000000000666600
00000000000000000
00000000000000000
```
**Train 2 output**
```text
00000000000000000
00000000000000000
00008000000000000
00080800000000000
00800080000000000
00080800000000000
00008000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Test input**
```text
00000000000000000
00005000000000000
00055500000000000
00555550000000000
05555555000000000
00555550000000000
00055500000222000
00005000002222200
00000000002222200
00000000002222200
00000000000222000
00000000000000000
00000000000000000
```
**Test output**
```text
00000000000000000
00000000000000000
00008000000000000
00080800000000000
00800080000000000
00080800000000000
00008000000000000
00000000000888000
00000000000808000
00000000000888000
00000000000000000
00000000000000000
00000000000000000
```
**Written solution**

Compute onion layers and keep only the cells in depth 2. The output is a blank board except for 8s exactly on the second peel layer.

**Reference program**
```python
def solve_S24_E5(grid):
    layers = onion_layers(grid)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            if layers[r][c] == 2:
                out[r][c] = 8
    return out
```
## S24_E6 — Keep the Thickest Component
**Skills:** cross-component comparison, inner-depth ranking, selective preservation

**Primitive note:** Thickness is represented by maximum onion depth. The thickest object is the one with the largest maximum depth.

**Scaffold:**

- Compute the maximum onion depth of every connected component.
- Find the unique component with the largest maximum depth.
- Erase everything else and recolor that winning component to 8.

**Train 1 input**
```text
000000000000000000000
000000000000000000000
000000000000000004000
000000000000000044400
022220003330000444440
022220003330000044400
000000003330000004000
000000000000000000000
000000000000000000000
000000000000000000000
000000000000000000000
```
**Train 1 output**
```text
000000000000000000000
000000000000000000000
000000000000000008000
000000000000000088800
000000000000000888880
000000000000000088800
000000000000000008000
000000000000000000000
000000000000000000000
000000000000000000000
000000000000000000000
```
**Train 2 input**
```text
000000000000000000000000000
000000000000000000000666000
000000000000000000000666000
000000000444440000066666660
022200000444440000066666660
022200000444440000066666660
022200000444440000000666000
000000000444440000000666000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
```
**Train 2 output**
```text
000000000000000000000000000
000000000000000000000888000
000000000000000000000888000
000000000000000000088888880
000000000000000000088888880
000000000000000000088888880
000000000000000000000888000
000000000000000000000888000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
```
**Test input**
```text
000000000000000000000000000
000000000000000000000000000
000020000000000000000000000
000222000003333333000000000
002222200003333333000000000
022222220003333333000000000
002222200003333333000000000
000222000003333333000000000
000020000000000000000000000
000000000000000000000055550
000000000000000000000055550
000000000000000000000000000
000000000000000000000000000
```
**Test output**
```text
000000000000000000000000000
000000000000000000000000000
000080000000000000000000000
000888000000000000000000000
008888800000000000000000000
088888880000000000000000000
008888800000000000000000000
000888000000000000000000000
000080000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
000000000000000000000000000
```
**Written solution**

Compare components by their maximum onion depth, keep only the unique deepest-thickness component, and recolor its occupied cells to 8.

**Reference program**
```python
def solve_S24_E6(grid):
    comps = component_masks(grid)
    best = max(comps, key=max_depth)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            if best[r][c]:
                out[r][c] = 8
    return out
```
## S24_E7 — Crop to the Depth Map
**Skills:** reduced output, numeric depth encoding, bounding-box cropping

**Primitive note:** Here the primitive becomes the whole answer: instead of raw colors, the output is the cropped onion-depth image itself.

**Scaffold:**

- Ignore the original color and compute the onion depth labels.
- Take the bounding box of the occupied shape.
- Return the cropped depth map inside that box.

**Train 1 input**
```text
000000000
000000000
002222200
002222200
002222200
002222200
002222200
000000000
000000000
```
**Train 1 output**
```text
11111
12221
12321
12221
11111
```
**Train 2 input**
```text
00000000000
00000000000
00003330000
00003330000
00333333300
00333333300
00333333300
00003330000
00003330000
00000000000
00000000000
```
**Train 2 output**
```text
0011100
0012100
1123211
1234321
1123211
0012100
0011100
```
**Test input**
```text
00000000000
00000000000
00000400000
00004440000
00044444000
00444444400
00044444000
00004440000
00000400000
00000000000
00000000000
```
**Test output**
```text
0001000
0012100
0123210
1234321
0123210
0012100
0001000
```
**Written solution**

Replace the shape by its onion-depth labeling and crop the result to the shape’s nonzero bounding box.

**Reference program**
```python
def solve_S24_E7(grid):
    return crop_nonzero(onion_layers(grid))
```
## S24_M1 — Header Palette by Depth
**Skills:** legend parsing, layer recolor, same-size conditioned transform

**Primitive note:** The top row acts as a palette indexed by onion depth: the first palette cell is for layer 1, the second for layer 2, and so on.

**Scaffold:**

- Read the nonzero colors in the header row as an ordered palette.
- Compute the onion depth of the body shape below the header.
- Recolor each occupied body cell using the palette entry for its depth.

**Train 1 input**
```text
23400000
00000000
01111100
01111100
01111100
01111100
01111100
00000000
```
**Train 1 output**
```text
23400000
00000000
02222200
02333200
02343200
02333200
02222200
00000000
```
**Train 2 input**
```text
567800000
000000000
000010000
000111000
001111100
011111110
001111100
000111000
000010000
000000000
```
**Train 2 output**
```text
567800000
000000000
000050000
000565000
005676500
056787650
005676500
000565000
000050000
000000000
```
**Test input**
```text
246800000
000000000
000111000
000111000
011111110
011111110
011111110
000111000
000111000
000000000
```
**Test output**
```text
246800000
000000000
000222000
000242000
022464220
024686420
022464220
000242000
000222000
000000000
```
**Written solution**

Use the nonzero header colors as a depth palette. Then recolor the body so that depth 1 gets the first header color, depth 2 the second, and so on.

**Reference program**
```python
def solve_S24_M1(grid):
    palette = [v for v in grid[0] if v != 0]
    out = copy_grid(grid)
    body = grid[1:]
    layers = onion_layers(body)
    for r in range(len(body)):
        for c in range(len(body[0])):
            d = layers[r][c]
            if d:
                out[r + 1][c] = palette[min(d - 1, len(palette) - 1)]
    return out
```
## S24_M2 — Match the Candidate by Layer Histogram
**Skills:** panel parsing, histogram comparison, candidate selection

**Primitive note:** Instead of using the full depth map, this puzzle only compares how many cells occur in each depth layer.

**Scaffold:**

- Split the board into panels using the 9-colored divider columns.
- For the prototype panel, count how many occupied cells lie in depth 1, depth 2, and so on.
- Choose the candidate whose layer-count histogram matches the prototype exactly.

**Train 1 input**
```text
0000000900000009000000090000000
0001000900000009000100091111110
0011100900111009001110091111110
0111110900111009011111091111110
0011100900111009001110091111110
0001000900000009000100090000000
0000000900000009000000090000000
```
**Train 1 output**
```text
080
```
**Train 2 input**
```text
0000000900000009000000090000000
0111110900111009011111090111110
0111110901111109011111090111110
0111110901111109011111090111110
0111110901111109001110090111110
0111110900111009001110090111110
0000000900000009000000090000000
```
**Train 2 output**
```text
008
```
**Test input**
```text
000000000900000000090000000009000000000
000111000900001000090001110009001111100
000111000900011100090001110009011111110
011111110900111110090111111109011111110
011111110901111111090111111109011111110
011111110900111110090111111109011111110
000111000900011100090001110009011111110
000111000900001000090001110009001111100
000000000900000000090000000009000000000
```
**Test output**
```text
080
```
**Written solution**

Parse the panels, compute the onion-layer histogram of the prototype, and mark the unique candidate whose histogram is identical.

**Reference program**
```python
def solve_S24_M2(grid):
    panels = extract_panels(grid, 9, 'col')
    proto = depth_hist(panels[0])
    ans = [8 if depth_hist(p) == proto else 0 for p in panels[1:]]
    return [ans]
```
## S24_M3 — Layer Histogram Strip
**Skills:** reduced counting output, symbolic layer profile, histogram encoding

**Primitive note:** The primitive turns one shape into a compact layer profile: how many cells live in each peel depth.

**Scaffold:**

- Compute the onion depth map of the shape.
- Count how many cells have depth 1, depth 2, and so on.
- Output those counts in a single horizontal strip.

**Train 1 input**
```text
000000000
000000000
000020000
000222000
002222200
000222000
000020000
000000000
000000000
```
**Train 1 output**
```text
841
```
**Train 2 input**
```text
0000000
0000000
0033300
0033300
0033300
0000000
0000000
```
**Train 2 output**
```text
81
```
**Test input**
```text
0000000
0000000
0004000
0044400
0004000
0000000
0000000
```
**Test output**
```text
41
```
**Written solution**

Compute the onion-layer histogram of the shape and write the counts, in increasing depth order, into a one-row strip.

**Reference program**
```python
def solve_S24_M3(grid):
    return [depth_hist(grid)]
```
## S24_M4 — Transfer the Layer Palette
**Skills:** palette inference, example-to-target transfer, component pairing

**Primitive note:** The left object already encodes a color for each depth layer; the right object must reuse that same depth-to-color mapping.

**Scaffold:**

- Take the left component and compute its onion layers.
- For each depth, read which color the left example uses on that depth.
- Apply the same depth-to-color mapping to the right plain component.

**Train 1 input**
```text
00000000000000000
00000000000000000
02222200000001000
02333200000011100
02343200000111110
02333200000011100
02222200000001000
00000000000000000
00000000000000000
```
**Train 1 output**
```text
00000000000000000
00000000000000000
02222200000002000
02333200000023200
02343200000234320
02333200000023200
02222200000002000
00000000000000000
00000000000000000
```
**Train 2 input**
```text
000000000000000000000
000000000000000000000
000080000000000000000
000878000000011111000
008767800000011111000
087656780000011111000
008767800000011111000
000878000000011111000
000080000000000000000
000000000000000000000
000000000000000000000
```
**Train 2 output**
```text
000000000000000000000
000000000000000000000
000080000000000000000
000878000000088888000
008767800000087778000
087656780000087678000
008767800000087778000
000878000000088888000
000080000000000000000
000000000000000000000
000000000000000000000
```
**Test input**
```text
000000000000000000000
000000000000000000000
000222000000000000000
000242000000011111000
022464220000011111000
024686420000011111000
022464220000011111000
000242000000011111000
000222000000000000000
000000000000000000000
000000000000000000000
```
**Test output**
```text
000000000000000000000
000000000000000000000
000222000000000000000
000242000000022222000
022464220000024442000
024686420000024642000
022464220000024442000
000242000000022222000
000222000000000000000
000000000000000000000
000000000000000000000
```
**Written solution**

Infer the palette from the layer-colored example on the left, then recolor the plain target on the right by matching each of its depths to the corresponding example color.

**Reference program**
```python
def solve_S24_M4(grid):
    comps = component_masks(grid)
    ex, target = comps[0], comps[1]
    ex_layers = onion_layers(ex)
    ex_md = max((v for row in ex_layers for v in row), default=0)
    palette = []
    for d in range(1, ex_md + 1):
        vals = [grid[r][c] for r, row in enumerate(ex_layers) for c, v in enumerate(row) if v == d]
        palette.append(majority_color(vals))
    t_layers = onion_layers(target)
    h, w = dims(grid)
    out = copy_grid(grid)
    for r in range(h):
        for c in range(w):
            d = t_layers[r][c]
            if d:
                out[r][c] = palette[min(d - 1, len(palette) - 1)]
    return out
```
## S24_M5 — Count Components by Thickness Class
**Skills:** categorization, component statistics, symbolic summary

**Primitive note:** Each component is classified only by its maximum onion depth, turning geometry into a small discrete thickness class.

**Scaffold:**

- Find every connected component.
- Assign each component to class 1, 2, 3, or 4 according to its maximum onion depth.
- Count how many components fall into each class and output those four counts.

**Train 1 input**
```text
0000000000000000000000000000000
0000000000000000000000000555000
0000000000000000000000000555000
0000000000000000040000055555550
0222200033300000444000055555550
0222200033300004444400055555550
0000000033300000444000000555000
0000000000000000040000000555000
0000000000000000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
```
**Train 1 output**
```text
1111
```
**Train 2 input**
```text
0000000000000000000000000000000
0000000000000000000000000050000
0222200000000000000000000555000
0222200000000044444000005555500
0000000000000044444000055555550
0000000000000044444000005555500
0000000000000044444000000555000
0000000000000044444000000050000
0000000000000000000000000000000
0000000033330000000000000000000
0000000033330000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
```
**Train 2 output**
```text
2011
```
**Test input**
```text
0000000000000000000000000000000
0000000000000000000000005555500
0000000000000000000000055555550
0000000000000000040000055555550
0222000000600000444000055555550
0222000000600004444400055555550
0222000066666000444000055555550
0000000000600000040000005555500
0000000000600000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
0000000000000000000000000000000
```
**Test output**
```text
0211
```
**Written solution**

Compute the maximum onion depth of each component, bucket the components by depths 1 through 4, and output the class counts as a four-cell row.

**Reference program**
```python
def solve_S24_M5(grid):
    counts = [0, 0, 0, 0]
    for comp in component_masks(grid):
        md = max_depth(comp)
        if 1 <= md <= 4:
            counts[md - 1] += 1
    return [counts]
```
## S24_M6 — Left-vs-Right Depth Report
**Skills:** panel parsing, pairwise measurement, reduced symbolic output

**Primitive note:** The divider splits the input into two separate objects whose maximum onion depths can be reported directly.

**Scaffold:**

- Split the board into left and right panels.
- Compute the maximum onion depth in each panel.
- Output a two-cell row with the left depth first and the right depth second.

**Train 1 input**
```text
00000009000000000
00000009000010000
01111109000111000
01111109001111100
01111109011111110
01111109001111100
01111109000111000
00000009000010000
00000009000000000
```
**Train 1 output**
```text
34
```
**Train 2 input**
```text
000000090000000
000000090001000
011110090011100
011110090111110
000000090011100
000000090001000
000000090000000
```
**Train 2 output**
```text
13
```
**Test input**
```text
0000000009000000000
0011111009000000000
0111111109011111100
0111111109011111100
0111111109011111100
0111111109011111100
0111111109000000000
0011111009000000000
0000000009000000000
```
**Test output**
```text
42
```
**Written solution**

Measure the maximum onion depth of the left panel and the right panel, then report those two depths as a length-two row.

**Reference program**
```python
def solve_S24_M6(grid):
    panels = extract_panels(grid, 9, 'col')
    return [[max_depth(panels[0]), max_depth(panels[1])]]
```
## S24_M7 — Sort Colors by Thickness
**Skills:** component ranking, color extraction, symbolic ordering

**Primitive note:** The geometry decides the order, but the output remembers the original component colors.

**Scaffold:**

- For each monochrome component, compute its maximum onion depth.
- Sort the components by increasing maximum depth.
- Output the components’ original colors in that sorted order.

**Train 1 input**
```text
000000000000000000000000000000000
000000000000000000000000088800000
000000000000000000000000088800000
000000000000000006000008888888000
022220004440000066600008888888000
022220004440000666660008888888000
000000004440000066600000088800000
000000000000000006000000088800000
000000000000000000000000000000000
000000000000000000000000000000000
000000000000000000000000000000000
000000000000000000000000000000000
000000000000000000000000000000000
```
**Train 1 output**
```text
2468
```
**Train 2 input**
```text
000000000000000000000000000000000
000000000000000000022200000000000
000000000000000000022200000000000
033333000000000002222222000000000
033333000000000002222222000555000
033333000000000002222222000555000
033333000000000000022200000555000
033333000000000000022200000000000
000000000000000000000000000000000
000000000077770000000000000000000
000000000077770000000000000000000
000000000000000000000000000000000
000000000000000000000000000000000
```
**Train 2 output**
```text
7532
```
**Test input**
```text
000000000000000000000000000000000
000040000000000000000000000000000
000444000000000000000000000000000
004444400006666660000000000008000
044444440006666660000000000088800
004444400006666660000000000888880
000444000006666660000000000088800
000040000000000000000000000008000
000000000000000000000000000000000
000000000000000000000222200000000
000000000000000000000222200000000
000000000000000000000000000000000
000000000000000000000000000000000
```
**Test output**
```text
2684
```
**Written solution**

Rank the components by maximum onion depth from thinnest to thickest and output their original colors in that order.

**Reference program**
```python
def solve_S24_M7(grid):
    comps = component_masks(grid)
    info = []
    for comp in comps:
        info.append((max_depth(comp), color_of_component(grid, comp)))
    info.sort()
    return [[color for _, color in info]]
```
## S24_H1 — Plain : Layer-Colored :: Plain : ?
**Skills:** analogy, palette inference, candidate selection, panel reasoning

**Primitive note:** The first two panels define a depth-color transform. The third panel must undergo the analogous transform, and only one candidate matches that result.

**Scaffold:**

- Use the first plain panel and the second colored panel to infer a palette indexed by onion depth.
- Apply that inferred palette to the third plain panel.
- Choose the candidate panel that exactly matches the transformed third panel.

**Train 1 input**
```text
00000009000000090000000900000009000000090000000
01111109022222090001000900020009000400090222220
01111109023332090011100900232009004340090233320
01111109023432090111110902343209043234090234320
01111109023332090011100900232009004340090233320
01111109022222090001000900020009000400090222220
00000009000000090000000900000009000000090000000
```
**Train 1 output**
```text
800
```
**Train 2 input**
```text
00000000090000000009000000000900000000090000000009000000000
00011100090005550009000000000900000000090000000009000000000
00011100090005650009000000000900000000090000000009000050000
01111111090556765509000111000900088800090005550009000565000
01111111090567876509000111000900087800090005650009005676500
01111111090556765509000111000900088800090005550009000565000
00011100090005650009000000000900000000090000000009000050000
00011100090005550009000000000900000000090000000009000000000
00000000090000000009000000000900000000090000000009000000000
```
**Train 2 output**
```text
080
```
**Test input**
```text
00000000090000000009000000000900000000090000000009000000000
00001000090000200009000000000900000000090000000009000000000
00011100090002420009001111100900222220090066666009002222200
00111110090024642009001111100900244420090064446009002444200
01111111090246864209001111100900246420090064246009002464200
00111110090024642009000111000900024200090006460009002444200
00011100090002420009000111000900022200090006660009002222200
00001000090000200009000000000900000000090000000009000000000
00000000090000000009000000000900000000090000000009000000000
```
**Test output**
```text
800
```
**Written solution**

Infer the depth-to-color mapping from the first two panels, apply that same mapping to the third panel, and mark the candidate that matches the resulting layer-colored shape.

**Reference program**
```python
def solve_S24_H1(grid):
    panels = extract_panels(grid, 9, 'col')
    a, b, c = panels[:3]
    cands = panels[3:]
    palette = depth_palette_from_pair(a, b)
    expected = apply_palette_to_panel(c, palette)
    return [[8 if exact_match(expected, cand) else 0 for cand in cands]]
```
## S24_H2 — Majority Repair, then Depth Map
**Skills:** panel aggregation, denoising, numeric depth output

**Primitive note:** The object is seen through several corrupted copies; majority voting reconstructs the solid mask before onion peeling turns it into a depth image.

**Scaffold:**

- Split the noisy copies into panels.
- Reconstruct the underlying object by majority vote at each cell position.
- Compute the onion-depth map of that repaired object and crop it to the object’s bounding box.

**Train 1 input**
```text
00000009000000090000000
00111109011110090111110
01111109010111090111110
01101109011111090111110
01111109011111090111010
01111109011111090011110
00000009000000090000000
```
**Train 1 output**
```text
11111
12221
12321
12221
11111
```
**Train 2 input**
```text
00000000090000000009000000000
00000000090000100009000010000
00011100090001110009000101000
00111110090011111009001111100
00111111090111111009011111010
00111110090011111009001111100
00011100090001110009000111000
00001000090000000009000010000
00000000090000000009000000000
```
**Train 2 output**
```text
0001000
0012100
0123210
1234321
0123210
0012100
0001000
```
**Test input**
```text
00000000090000000009000000000
00000000090000000009000000000
01110111090111110109011111110
01111111090111111109011011110
01110111090111111109011111110
00011100090001110009000111000
00011100090001110009000111000
00000000090000000009000000000
00000000090000000009000000000
```
**Test output**
```text
1111111
1222221
1123211
0012100
0011100
```
**Written solution**

Repair the object by taking the majority occupancy across the three noisy panels, then output the cropped onion-depth map of the repaired shape.

**Reference program**
```python
def solve_S24_H2(grid):
    panels = extract_panels(grid, 9, 'col')
    repaired = majority_grid(panels)
    return crop_nonzero(onion_layers(repaired))
```
## S24_H3 — Thickness Congruence Matrix
**Skills:** relational output, pairwise comparison, matrix construction

**Primitive note:** Each panel contributes one thickness number, and the output compares every pair of those numbers.

**Scaffold:**

- Compute the maximum onion depth of every panel.
- For each pair of panels, check whether those maximum depths are equal.
- Write an 8 where the two depths match and 0 where they do not.

**Train 1 input**
```text
00000009000000090000000
00000009000100091111110
00111009001110091111110
00111009011111091111110
00111009001110091111110
00000009000100090000000
00000009000000090000000
```
**Train 1 output**
```text
808
080
808
```
**Train 2 input**
```text
00000000090000000009000000000
00111110090001110009000000000
01111111090001110009001111100
01111111090111111109001111100
01111111090111111109001111100
01111111090111111109001111100
01111111090001110009001111100
00111110090001110009000000000
00000000090000000009000000000
```
**Train 2 output**
```text
880
880
008
```
**Test input**
```text
00000000090000000009000000000
00001000090000000009000000000
00011100090011111009000111000
00111110090011111009001111100
01111111090011111009001111100
00111110090011111009001111100
00011100090011111009000111000
00001000090000000009000000000
00000000090000000009000000000
```
**Test output**
```text
800
088
088
```
**Written solution**

Turn each panel into its maximum onion depth, then build a square matrix whose entries are 8 exactly when the corresponding two panels have equal thickness.

**Reference program**
```python
def solve_S24_H3(grid):
    panels = extract_panels(grid, 9, 'col')
    ds = [max_depth(p) for p in panels]
    return [[8 if ds[i] == ds[j] else 0 for j in range(len(ds))] for i in range(len(ds))]
```
## S24_H4 — Prototype Key Lookup by Layer Signature
**Skills:** library lookup, keyed prototypes, histogram matching

**Primitive note:** Each prototype is tagged by a key color. The query must inherit the key of the prototype with the same onion-layer signature.

**Scaffold:**

- Read the first cell of each prototype panel as its key color.
- Ignore that key cell and compute the prototype shape’s layer histogram.
- Find the prototype whose histogram matches the query and output its key color.

**Train 1 input**
```text
200000000940000000096000000009000000000
000000000900000000090001110009000000000
000000000900001000090001110009000010000
000111000900011100090111111109000111000
000111000900111110090111111109001111100
000111000900011100090111111109000111000
000000000900001000090001110009000010000
000000000900000000090001110009000000000
000000000900000000090000000009000000000
```
**Train 1 output**
```text
4
```
**Train 2 input**
```text
300000000950000000097000000009000000000
000000000900000000090000000009000000000
001111100900011100090111111009011111100
001111100900111110090111111009011111100
001111100900111110090111111009011111100
001111100900111110090111111009011111100
001111100900011100090000000009000000000
000000000900000000090000000009000000000
000000000900000000090000000009000000000
```
**Train 2 output**
```text
7
```
**Test input**
```text
200000000980000000096000000009000000000
000010000900111110090000000009001111100
000111000901111111090111111109011111110
001111100901111111090111111109011111110
011111110901111111090111111109011111110
001111100901111111090001110009011111110
000111000901111111090001110009011111110
000010000900111110090000000009001111100
000000000900000000090000000009000000000
```
**Test output**
```text
8
```
**Written solution**

Compare the query’s onion-layer histogram with the histograms of the keyed prototypes. Output the key color attached to the matching prototype.

**Reference program**
```python
def solve_S24_H4(grid):
    panels = extract_panels(grid, 9, 'col')
    query = panels[-1]
    q_hist = depth_hist(query)
    for proto in panels[:-1]:
        key = proto[0][0]
        shape = copy_grid(proto)
        shape[0][0] = 0
        if depth_hist(shape) == q_hist:
            return [[key]]
    return [[0]]
```
## S24_H5 — Grow One More Onion Layer
**Skills:** analogy, inverse peeling, one-step dilation, reduced output

**Primitive note:** If onion peeling removes one boundary layer, this task asks for the inverse move: add one more outer layer around the query shape.

**Scaffold:**

- Use the first two panels to see that the shape gains exactly one four-neighbor outer layer.
- Take the third panel as the query shape.
- Grow it by one such layer and output the cropped grown result.

**Train 1 input**
```text
00000009000000090000000
00000009000000090000000
00111009001110090001000
00111009001110090011100
00111009001110090001000
00000009000000090000000
00000009000000090000000
```
**Train 1 output**
```text
00100
01110
11111
01110
00100
```
**Train 2 input**
```text
00000000090000000009000000000
00000000090000000009000000000
00001000090001110009000000000
00011100090011111009000111000
00111110090011111009000111000
00011100090011111009000111000
00001000090001110009000000000
00000000090000000009000000000
00000000090000000009000000000
```
**Train 2 output**
```text
01110
11111
11111
11111
01110
```
**Test input**
```text
00000000090000000009000000000
00000000090000000009000000000
00111110090011111009000010000
00111110090011111009000111000
00111110090011111009001111100
00011100090011111009000111000
00011100090011111009000010000
00000000090000000009000000000
00000000090000000009000000000
```
**Test output**
```text
0001000
0011100
0111110
1111111
0111110
0011100
0001000
```
**Written solution**

Add one new four-neighbor boundary layer around the query shape, then crop the grown mask to its occupied bounding box.

**Reference program**
```python
def solve_S24_H5(grid):
    panels = extract_panels(grid, 9, 'col')
    c = panels[2]
    grown = grow_one_layer(c)
    return crop_nonzero(grown)
```
## S24_H6 — Match by Full Depth Map Under Rotation
**Skills:** normalized comparison, rotation reasoning, candidate selection

**Primitive note:** The comparison is stricter than a histogram: the full cropped onion-depth image must match, up to rotation.

**Scaffold:**

- Compute the cropped onion-depth map of the prototype panel.
- Compute the cropped onion-depth map of each candidate.
- Choose the candidate whose depth map matches the prototype after some rotation.

**Train 1 input**
```text
000000000900000000090000000009000000000
000000000900000000090011110009000010000
011111100900111110090011110009000111000
011111100900111110090011110009001111100
011111100900111110090011110009011111110
011111100900111110090011110009001111100
000000000900111110090011110009000111000
000000000900000000090000000009000010000
000000000900000000090000000009000000000
```
**Train 1 output**
```text
080
```
**Train 2 input**
```text
000000000900000000090000000009000000000
000000000900001110090011111009000000000
011111110900001110090111111109011111110
011111110900111110090111111109011111110
011111110900111110090111111109011111110
000111000900111110090111111109011111110
000111000900001110090111111109011111110
000000000900001110090011111009000000000
000000000900000000090000000009000000000
```
**Train 2 output**
```text
800
```
**Test input**
```text
000000000900000000090000000009000000000
000000000900001000090011111009000000000
011111110900011100090011111009001111100
011111110900111110090011111009001111100
011111110901111111090011111009001111100
011111110900111110090011111009001111100
011111110900011100090011111009001111100
000000000900001000090011111009000000000
000000000900000000090000000009000000000
```
**Test output**
```text
080
```
**Written solution**

Normalize the prototype and each candidate to cropped onion-depth maps, allow rotations, and mark the unique candidate with the same full depth map.

**Reference program**
```python
def solve_S24_H6(grid):
    panels = extract_panels(grid, 9, 'col')
    proto = normalized_depth_map(panels[0])
    ans = []
    for cand in panels[1:]:
        dm = normalized_depth_map(cand)
        ok = any(rotk(dm, k) == proto for k in range(4))
        ans.append(8 if ok else 0)
    return [ans]
```
## S24_H7 — Common Core via Minimum Depth Map
**Skills:** panel alignment, depth-map composition, numeric reduced output

**Primitive note:** After both panels are converted into depth maps, the answer is the cellwise minimum of those normalized depth images.

**Scaffold:**

- Crop each panel to its onion-depth map.
- Align the two cropped depth maps by their top-left corners.
- At each position, keep the smaller of the two depth values.

**Train 1 input**
```text
000000090000000
011111090001000
011111090011100
011111090111110
011111090011100
011111090001000
000000090000000
```
**Train 1 output**
```text
00100
01210
12321
01210
00100
```
**Train 2 input**
```text
000000090000000
001110090111110
011111090111110
011111090111110
011111090011100
001110090011100
000000090000000
```
**Train 2 output**
```text
01110
12221
12321
01210
01110
```
**Test input**
```text
0000000009000000000
0001110009001111100
0001110009011111110
0111111109011111110
0111111109011111110
0111111109011111110
0001110009011111110
0001110009001111100
0000000009000000000
```
**Test output**
```text
0011100
0012100
1123211
1234321
1123211
0012100
0011100
```
**Written solution**

Convert both panels to cropped onion-depth maps, align them, and output the cellwise minimum depth at every position.

**Reference program**
```python
def solve_S24_H7(grid):
    panels = extract_panels(grid, 9, 'col')
    a = normalized_depth_map(panels[0])
    b = normalized_depth_map(panels[1])
    h = max(len(a), len(b))
    w = max(len(a[0]), len(b[0]))
    aa = pad_to(a, h, w, 0)
    bb = pad_to(b, h, w, 0)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            out[r][c] = min(aa[r][c], bb[r][c])
    return out
```