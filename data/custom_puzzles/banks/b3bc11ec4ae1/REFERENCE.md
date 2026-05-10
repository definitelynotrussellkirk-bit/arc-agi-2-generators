# ARC-style Puzzle Bank — 21 more puzzles (set 18)

This eighteenth bank leans into **interval completion, orthogonal hulls, blocked closure, and symbolic relations**. The recurring move is not local stamping or path tracing but *closing intervals*: take sparse endpoint markers, infer the span they determine along rows or columns, and then reuse that idea in stricter or richer ways. In the easier tier that means direct horizontal or vertical gap-filling. In the middle tier it becomes component-wise closure, blocker-aware closure, ranking, intersections, and panel odd-one-out tasks. In the hard tier it scales into legend-routed transform libraries, majority merges, counterfactual target matching, and symbolic matrices built from completed shapes.

The core primitive introduced here is:

```text
axis_closure(cells, axis='row')
For each occupied row or column, fill every cell between that line's extreme occupied coordinates. This turns sparse endpoints into solid spans, supports row/column gap-bridging, and — when composed across axes or under blockers — builds rectangles, blocked room completions, overlap tests, and relation matrices.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set18_reference.py`.

## Index

### Easy

- **S18_E1** — Horizontal Gap Fill

- **S18_E2** — Vertical Gap Fill

- **S18_E3** — Corner Marker Chooses Axis

- **S18_E4** — Bridge Only, Not the Endpoints

- **S18_E5** — Color-Split Axis Closure

- **S18_E6** — Rectangle Completion from Four Corners

- **S18_E7** — Longest Closed Row Wins

### Medium

- **S18_M1** — Component-Wise Horizontal Closure

- **S18_M2** — Pick the Color-Coded Object that Gains the Most

- **S18_M3** — Orientation Chooses the Axis

- **S18_M4** — Close Only the Rows with Exactly Two Markers

- **S18_M5** — Intersection of Row and Column Closures

- **S18_M6** — Odd Panel by Completed Rectangle

- **S18_M7** — Horizontal Closure Inside Wall-Separated Rooms

### Hard

- **S18_H1** — Mini-Legend Maps Each Color to a Closure Mode

- **S18_H2** — Pairwise Overlap Matrix of Completed Closures

- **S18_H3** — Pick the Object Whose Double Closure Is a True Rectangle

- **S18_H4** — Majority Merge of Three Completed Panels

- **S18_H5** — Target Mask Selects the Best Closure Match

- **S18_H6** — Blocked Double Closure Inside Walled Rooms

- **S18_H7** — Congruence Matrix of Completed Shapes


# Easy


## S18_E1 — Horizontal Gap Fill
**Skills:** row-wise span completion, same-size blank output, extreme detection

**Primitive note:** This is the simplest use of axis_closure: close each occupied row by filling between its extreme occupied columns.

**Scaffold:**

- Ignore the exact source color; every nonzero cell is just a marker.
- Within each occupied row, look at the leftmost and rightmost marker.
- Fill the whole interval between them on a blank grid.

**Train 1 input**

```text
0000000000
0200200000
0000000000
0000000000
0020002020
0000000000
0000000200
0000000000
```
**Train 1 output**

```text
0000000000
0888800000
0000000000
0000000000
0088888880
0000000000
0000000800
0000000000
```
**Train 2 input**

```text
000000000
000000000
020002000
000000000
000000000
000220020
000000000
202000000
000000000
```
**Train 2 output**

```text
000000000
000000000
088888000
000000000
000000000
000888880
000000000
888000000
000000000
```
**Test input**

```text
00000000000
00200002000
00000000000
00000200200
00000000000
00000000000
02002000000
00000000000
```
**Expected test output**

```text
00000000000
00888888000
00000000000
00000888800
00000000000
00000000000
08888000000
00000000000
```
**Written solution**

Treat every nonzero cell as a marker. For each row that contains markers, find the leftmost and rightmost marked columns and fill the whole horizontal span between them. Do that independently for each row, and write the union of those spans onto a blank output grid in color 8.

**Reference program**

```python
def solve_S18_E1(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(axis_closure(cells,'row'), h,w, 8)
```


## S18_E2 — Vertical Gap Fill
**Skills:** column-wise span completion, same-size blank output, extreme detection

**Primitive note:** The same primitive works on the other axis: axis_closure with axis='col' fills between extreme occupied rows inside each occupied column.

**Scaffold:**

- Treat each nonzero cell as a marker.
- Within each occupied column, find the topmost and bottommost marker.
- Fill the whole vertical interval between them.

**Train 1 input**

```text
00000000
02000000
00000200
00000000
02000000
00000000
00020000
00000200
00020000
00000000
```
**Train 1 output**

```text
00000000
08000000
08000800
08000800
08000800
00000800
00080800
00080800
00080000
00000000
```
**Train 2 input**

```text
002000000
000000000
000000020
002000000
000000020
000000200
000000000
000000000
000000200
```
**Train 2 output**

```text
008000000
008000000
008000080
008000080
000000080
000000800
000000800
000000800
000000800
```
**Test input**

```text
0000000000
0000200000
0000000000
0000000020
0000000000
0200000000
0000200000
0200000000
0000000020
0000000000
```
**Expected test output**

```text
0000000000
0000800000
0000800000
0000800080
0000800080
0800800080
0800800080
0800000080
0000000080
0000000000
```
**Written solution**

Each occupied column defines a vertical span. In every column that contains nonzero cells, fill all rows from the topmost marked cell down to the bottommost marked cell. Put those column spans onto a blank output grid in color 8.

**Reference program**

```python
def solve_S18_E2(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(axis_closure(cells,'col'), h,w, 8)
```


## S18_E3 — Corner Marker Chooses Axis
**Skills:** mode selection, row vs column closure, ignore control cell

**Primitive note:** A single control cell can route the same primitive to either row-closure or column-closure mode.

**Scaffold:**

- Read the top-left marker first.
- If it is 2, close rows; if it is 3, close columns.
- Then ignore that control cell and apply the chosen closure to the remaining markers.

**Train 1 input**

```text
200000000
000000000
020002000
000000000
000000000
000200200
000000000
000000000
```
**Train 1 output**

```text
000000000
000000000
088888000
000000000
000000000
000888800
000000000
000000000
```
**Train 2 input**

```text
30000000
00000300
00300000
00000000
00000300
00000000
00300000
00000000
00000000
```
**Train 2 output**

```text
00000000
00000800
00800800
00800800
00800800
00800000
00800000
00000000
00000000
```
**Test input**

```text
3000000000
0003000000
0000000300
0000000000
0000000000
0003000000
0000000300
0000000000
```
**Expected test output**

```text
0000000000
0008000000
0008000800
0008000800
0008000800
0008000800
0000000800
0000000000
```
**Written solution**

The top-left cell is not part of the pattern itself; it is a mode switch. A 2 means fill horizontal spans inside occupied rows, while a 3 means fill vertical spans inside occupied columns. Ignore the marker after reading it, and draw the chosen closure in color 8.

**Reference program**

```python
def solve_S18_E3(grid):
    h,w=dims(grid)
    marker=grid[0][0]
    axis='row' if marker==2 else 'col'
    cells=[(r,c) for r,c,v in nonzero(grid) if not (r==0 and c==0)]
    return render_same_size(axis_closure(cells,axis), h,w, 8)
```


## S18_E4 — Bridge Only, Not the Endpoints
**Skills:** difference of sets, row-wise closure, same-size blank output

**Primitive note:** axis_closure gives the full closed span; subtracting the original cells isolates the pure gap-bridging part.

**Scaffold:**

- First imagine the full horizontal closure.
- Then remove the original markers from it.
- Only the newly bridged cells survive in the output.

**Train 1 input**

```text
0000000000
0200020000
0000000000
0020200000
0000000000
0000002002
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0088800000
0000000000
0008000000
0000000000
0000000880
0000000000
0000000000
```
**Train 2 input**

```text
000000000
000000000
200200000
000000000
000020002
000000000
000000000
022000000
000000000
```
**Train 2 output**

```text
000000000
000000000
088000000
000000000
000008880
000000000
000000000
000000000
000000000
```
**Test input**

```text
00000000000
00200000200
00000000000
00000000000
00000202000
00000000000
02002000000
00000000000
```
**Expected test output**

```text
00000000000
00088888000
00000000000
00000000000
00000080000
00000000000
00880000000
00000000000
```
**Written solution**

Compute the horizontal closure exactly as in a row-filling task, but do not copy the original marked cells. Only keep the cells that had to be inserted to bridge the gaps between endpoints, and color those inserted cells 8.

**Reference program**

```python
def solve_S18_E4(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(bridge_only(cells,'row'), h,w, 8)
```


## S18_E5 — Color-Split Axis Closure
**Skills:** per-color routing, different output colors, independent transforms

**Primitive note:** One primitive can be routed by color: one color family uses row closure, another uses column closure.

**Scaffold:**

- Treat the two source colors separately.
- Color 2 becomes horizontal spans and is recolored to 8.
- Color 3 becomes vertical spans and is recolored to 6.

**Train 1 input**

```text
0000000000
0203020000
0000000030
0000000000
0020002000
0003000000
0000000030
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0886880000
0006000060
0006000060
0086888060
0006000060
0000000060
0000000000
0000000000
```
**Train 2 input**

```text
00000000000
00000000300
02002000000
00300000000
00000000300
00000020020
00000000000
00300000000
```
**Train 2 output**

```text
00000000000
00000000600
08888000600
00600000600
00600000600
00600088880
00600000000
00600000000
```
**Test input**

```text
0000000000
0020000200
0000000003
0000030000
0000000000
0000030000
0200200000
0000000003
0000000000
```
**Expected test output**

```text
0000000000
0088888800
0000000006
0000060006
0000060006
0000060006
0888800006
0000000006
0000000000
```
**Written solution**

Split the input into the color-2 markers and the color-3 markers. Close the color-2 markers along rows and paint those spans 8. Close the color-3 markers along columns and paint those spans 6. Combine both results on a blank grid.

**Reference program**

```python
def solve_S18_E5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    out=blank(h,w,0)
    place(out, axis_closure(by[2],'row'), 8)
    place(out, axis_closure(by[3],'col'), 6)
    return out
```


## S18_E6 — Rectangle Completion from Four Corners
**Skills:** two-pass closure, from sparse corners to filled rectangle, same-size blank output

**Primitive note:** Applying axis_closure twice on perpendicular axes turns a corner skeleton into its orthogonally convex completion.

**Scaffold:**

- The four markers are the corners of one rectangle.
- A row closure connects the two corners on each occupied row.
- A column closure of that result fills the whole rectangle.

**Train 1 input**

```text
000000000
002000200
000000000
000000000
000000000
002000200
000000000
000000000
```
**Train 1 output**

```text
000000000
008888800
008888800
008888800
008888800
008888800
000000000
000000000
```
**Train 2 input**

```text
0000000000
0000000000
0200000020
0000000000
0000000000
0000000000
0000000000
0200000020
0000000000
```
**Train 2 output**

```text
0000000000
0000000000
0888888880
0888888880
0888888880
0888888880
0888888880
0888888880
0000000000
```
**Test input**

```text
00000000000
00020000020
00000000000
00000000000
00000000000
00000000000
00020000020
00000000000
```
**Expected test output**

```text
00000000000
00088888880
00088888880
00088888880
00088888880
00088888880
00088888880
00000000000
```
**Written solution**

The input gives only the four corners of an axis-aligned rectangle. First close across rows so that the top edge and bottom edge become solid spans. Then close down columns; that turns those two edges into a fully filled rectangle. Draw the finished rectangle in color 8.

**Reference program**

```python
def solve_S18_E6(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(double_closure(cells,'row','col'), h,w, 8)
```


## S18_E7 — Longest Closed Row Wins
**Skills:** ranking by closure length, row-wise closure, same-size blank output

**Primitive note:** axis_closure produces candidate spans; their lengths then become the ranking feature.

**Scaffold:**

- Close every occupied row horizontally.
- Measure the resulting span length in each row.
- Keep only the longest one.

**Train 1 input**

```text
0000000000
0202000000
0000000000
0020000200
0000000000
0000200002
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0000000000
0000000000
0088888800
0000000000
0000000000
0000000000
0000000000
```
**Train 2 input**

```text
00000000000
00000000000
20002000000
00000000000
00020000020
00000000000
00000000000
00000220000
00000000000
```
**Train 2 output**

```text
00000000000
00000000000
00000000000
00000000000
00088888880
00000000000
00000000000
00000000000
00000000000
```
**Test input**

```text
000000000000
002000200000
000000000000
020000000200
000000000000
000000000000
000002020000
000000000000
```
**Expected test output**

```text
000000000000
000000000000
000000000000
088888888800
000000000000
000000000000
000000000000
000000000000
```
**Written solution**

For each occupied row, build the full horizontal span between its extreme markers. Compare those span lengths, choose the longest, and output only that winning span in color 8 on an otherwise blank grid.

**Reference program**

```python
def solve_S18_E7(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    by=defaultdict(list)
    for r,c in cells:
        by[r].append(c)
    best=None
    bestlen=-1
    for r, cols in by.items():
        L=max(cols)-min(cols)+1
        if L>bestlen or (L==bestlen and r<best[0] if best is not None else False):
            bestlen=L
            best=(r, min(cols), max(cols))
    out=blank(h,w,0)
    if best:
        r,a,b=best
        for c in range(a,b+1):
            out[r][c]=8
    return out
```


# Medium


## S18_M1 — Component-Wise Horizontal Closure
**Skills:** object decomposition, avoid cross-object bridging, row-wise closure per component

**Primitive note:** The primitive still fills intervals, but now the scope is not 'whole color class' — it is one connected component at a time.

**Scaffold:**

- Do not close across every marker of the same color at once.
- First split the markers into connected components.
- Apply horizontal closure inside each component separately, then union the results.

**Train 1 input**

```text
00000000000000
02220000222000
02020000202000
02020000202000
00000222200000
00000200200000
00000200200000
00000000000000
```
**Train 1 output**

```text
00000000000000
08880000888000
08880000888000
08880000888000
00000888800000
00000888800000
00000888800000
00000000000000
```
**Train 2 input**

```text
000000000000000
022200000000000
020200022220000
020200020020000
020200020020000
000000000002220
000000000002020
000000000002020
000000000000000
```
**Train 2 output**

```text
000000000000000
088800000000000
088800088880000
088800088880000
088800088880000
000000000008880
000000000008880
000000000008880
000000000000000
```
**Test input**

```text
000000000000000
002222000022200
002002000020200
002002000020200
000000000020200
000000222000000
000000202000000
000000202000000
000000000000000
```
**Expected test output**

```text
000000000000000
008888000088800
008888000088800
008888000088800
000000000088800
000000888000000
000000888000000
000000888000000
000000000000000
```
**Written solution**

All markers share one color, but they do not belong to one object. First separate the input into connected components. Within each component, close rows between that component's own leftmost and rightmost cells. Union those component-wise row closures on a blank output grid in color 8.

**Reference program**

```python
def solve_S18_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        closed=axis_closure(comp['cells'],'row')
        place(out, closed, 8)
    return out
```


## S18_M2 — Pick the Color-Coded Object that Gains the Most
**Skills:** counterfactual closure, ranking by added cells, cropped output

**Primitive note:** axis_closure is used as a hypothetical completion; the ranking feature is the amount of growth each color-coded object would get from that completion.

**Scaffold:**

- Treat each nonzero color as a separate candidate object.
- For each color, ask how many cells horizontal closure would add.
- Choose the object with the biggest gain and output its closed version, cropped tightly.

**Train 1 input**

```text
0000000000000
0200002004400
0200002000000
0000000004400
0030300000000
0030300000000
0000000000000
0000000000000
```
**Train 1 output**

```text
888888
888888
```
**Train 2 input**

```text
00000000000000
02000002000000
00000000004400
02000002000000
00000000004400
00300300000000
00300300000000
00000000000000
00000000000000
```
**Train 2 output**

```text
8888888
0000000
8888888
```
**Test input**

```text
0000000000000
0200002004400
0200002000000
0000000004400
0000000030300
0000000030300
0000000000000
0000000000000
```
**Expected test output**

```text
888888
888888
```
**Written solution**

Each candidate object is identified by its color. Compute the horizontal closure of each color's markers and measure how many cells that closure adds beyond the original markers of that color. Pick the color with the largest gain, then output its closed shape as a tightly cropped color-8 grid.

**Reference program**

```python
def solve_S18_M2(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    best_color=None
    best_gain=-1
    best_closed=None
    for color,cells in sorted(by.items()):
        closed=axis_closure(cells,'row')
        gain=len(closed)-len(cells)
        if gain>best_gain:
            best_gain=gain; best_color=color; best_closed=closed
    return crop_cells(best_closed, 8)
```


## S18_M3 — Orientation Chooses the Axis
**Skills:** object descriptors, per-object routing, row vs column closure

**Primitive note:** The interval-closing primitive is still doing the geometric work, but the axis is chosen from a descriptor of each color-coded object.

**Scaffold:**

- Treat each color as one separate object.
- For each color, compare how many rows it occupies to how many columns it occupies.
- Wider objects close along rows; taller objects close along columns.

**Train 1 input**

```text
000000000000
020002003300
020002000000
000000000000
000000003300
000000000000
004000400000
004000400000
000000000000
```
**Train 1 output**

```text
000000000000
088888008800
088888000000
000000000000
000000008800
000000000000
008888800000
008888800000
000000000000
```
**Train 2 input**

```text
0000000000000
0200002000000
0200002000000
0000000003300
0000000000000
0000000000000
0004040000000
0000000003300
0004040000000
0000000000000
```
**Train 2 output**

```text
0000000000000
0888888000000
0888888000000
0000000008800
0000000000000
0000000000000
0008880000000
0000000008800
0008880000000
0000000000000
```
**Test input**

```text
000000000000
002000020000
002000020330
000000000000
000000000000
000000000000
044000000330
000000000000
044000000000
```
**Expected test output**

```text
000000000000
008888880000
008888880880
000000000000
000000000000
000000000000
088000000880
000000000000
088000000000
```
**Written solution**

Each color denotes a separate object. For each one, compare its row span to its column span. If it occupies at least as many columns as rows, fill horizontal intervals inside that color's footprint. If it occupies more rows than columns, fill vertical intervals instead. Union the transformed objects and paint them 8.

**Reference program**

```python
def solve_S18_M3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    for color,cells in by.items():
        rs,cs=count_rows_cols(cells)
        axis='row' if cs>=rs else 'col'
        place(out, axis_closure(cells,axis), 8)
    return out
```


## S18_M4 — Close Only the Rows with Exactly Two Markers
**Skills:** counting within rows, conditional closure, same-size blank output

**Primitive note:** axis_closure still does the filling, but only after a row-count filter decides which rows are eligible.

**Scaffold:**

- Count how many markers each occupied row contains.
- Ignore rows with one marker or three-plus markers.
- Only rows with exactly two markers turn into full horizontal spans.

**Train 1 input**

```text
00000000000
02000200000
00000000000
00200200200
00000000000
20002000000
00000000020
00000000000
```
**Train 1 output**

```text
00000000000
08888800000
00000000000
00000000000
00000000000
88888000000
00000000000
00000000000
```
**Train 2 input**

```text
0000000000
0000000000
0200002000
0000000000
0020200200
0000000000
0000000000
0000020020
0000000000
```
**Train 2 output**

```text
0000000000
0000000000
0888888000
0000000000
0000000000
0000000000
0000000000
0000088880
0000000000
```
**Test input**

```text
000000000000
200200000000
000002002020
000000000000
000000000000
000020000200
000000020000
000000000000
```
**Expected test output**

```text
000000000000
888800000000
000000000000
000000000000
000000000000
000088888800
000000000000
000000000000
```
**Written solution**

Examine the rows independently. When a row contains exactly two nonzero cells, fill the whole interval between them. Rows with any other number of markers contribute nothing. Output the union of the qualifying row spans in color 8.

**Reference program**

```python
def solve_S18_M4(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    by=defaultdict(list)
    for r,c in cells:
        by[r].append(c)
    out=blank(h,w,0)
    for r, cols in by.items():
        if len(cols)==2:
            for c in range(min(cols), max(cols)+1):
                out[r][c]=8
    return out
```


## S18_M5 — Intersection of Row and Column Closures
**Skills:** set intersection, crossing spans, two-color reasoning

**Primitive note:** The primitive creates candidate spans on two different axes; their overlap becomes the actual answer.

**Scaffold:**

- Build the row closure of color 2.
- Build the column closure of color 3.
- Keep only the cells that belong to both completed structures.

**Train 1 input**

```text
0000030000
0003000000
0200002000
0000000000
0000000000
0020000200
0003000000
0000030000
```
**Train 1 output**

```text
0000000000
0000000000
0008080000
0000000000
0000000000
0008080000
0000000000
0000000000
```
**Train 2 input**

```text
00003000000
00200000200
00000003000
00000000000
00000000000
00000000000
02000020000
00003000000
00000003000
```
**Train 2 output**

```text
00000000000
00008000000
00000000000
00000000000
00000000000
00000000000
00008000000
00000000000
00000000000
```
**Test input**

```text
000030000000
000000030000
020000000200
000000000000
000000000000
000200000020
000030000000
000000030000
```
**Expected test output**

```text
000000000000
000000000000
000080080000
000000000000
000000000000
000080080000
000000000000
000000000000
```
**Written solution**

Use the color-2 markers to create horizontal spans and the color-3 markers to create vertical spans. Then intersect those two completed sets of cells. The output is just that intersection, drawn in color 8 on a blank grid.

**Reference program**

```python
def solve_S18_M5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=axis_closure(by[2],'row')
    b=axis_closure(by[3],'col')
    return render_same_size(a & b, h,w, 8)
```


## S18_M6 — Odd Panel by Completed Rectangle
**Skills:** panel parsing, double closure, odd-one-out by normalized shape

**Primitive note:** The closure primitive becomes a shape-normalization tool here: sparse corners are turned into solid comparable rectangles.

**Scaffold:**

- Split the input into panels at the separator columns.
- In each panel, complete the sparse corner pattern into its filled rectangle.
- Two completed rectangles match; one does not. Output the odd one, cropped.

**Train 1 input**

```text
00000090200209000000
02002090000009000000
00000090200209200020
02002090000009200020
00000090000009000000
00000090000009000000
```
**Train 1 output**

```text
88888
88888
```
**Train 2 input**

```text
00000090020209000000
20200090000009000000
00000090000009020002
00000090020209000000
20200090000009020002
00000090000009000000
```
**Train 2 output**

```text
88888
88888
88888
```
**Test input**

```text
00000090202009000000
02020090000009202000
00000090202009000000
02020090000009000000
00000090000009202000
00000090000009000000
```
**Expected test output**

```text
888
888
888
888
```
**Written solution**

Each panel contains only the corners of one rectangle. Complete each panel separately by applying row closure and then column closure. Compare the resulting filled rectangles up to translation: two panels match and one is different. Output the completed rectangle from the odd panel as a tight color-8 crop.

**Reference program**

```python
def solve_S18_M6(grid):
    panels=panel_split_vertical(grid, 9)
    norms=[]
    closures=[]
    for _,_,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        closed=double_closure(cells,'row','col')
        closures.append(closed)
        norms.append(norm_cells(closed))
    cnt=Counter(norms)
    idx=next(i for i,n in enumerate(norms) if cnt[n]==1)
    return crop_cells(closures[idx], 8)
```


## S18_M7 — Horizontal Closure Inside Wall-Separated Rooms
**Skills:** blockers, segment-wise closure, preserve walls

**Primitive note:** This is a blocked version of axis_closure: the extremes are computed inside each unbroken segment, not across the whole row.

**Scaffold:**

- Treat wall cells as hard separators.
- Within each row segment between walls, close only between the markers that lie inside that same segment.
- Do not bridge across a wall; preserve the wall cells in the output.

**Train 1 input**

```text
0000500005000
0202500005000
0000502025000
0000500005000
0000500005000
0000500005202
0000502025000
0000500005000
```
**Train 1 output**

```text
0000500005000
0888500005000
0000508885000
0000500005000
0000500005000
0000500005888
0000508885000
0000500005000
```
**Train 2 input**

```text
00000500005000
02002500005000
00000500005000
00000502025000
00000500005000
00000500005000
00000500005202
00000520205000
00000500005000
```
**Train 2 output**

```text
00000500005000
08888500005000
00000500005000
00000508885000
00000500005000
00000500005000
00000500005888
00000588805000
00000500005000
```
**Test input**

```text
00005000050000
20025000050000
00005020250000
00005000050000
00005000050000
00005000052002
00005202050000
00005000050000
```
**Expected test output**

```text
00005000050000
88885000050000
00005088850000
00005000050000
00005000050000
00005000058888
00005888050000
00005000050000
```
**Written solution**

The row-filling rule still applies, but only inside wall-delimited row segments. Walls break a row into separate rooms, and closure cannot cross them. Preserve the wall cells as 5 and fill each within-room horizontal span in color 8.

**Reference program**

```python
def solve_S18_M7(grid):
    h,w=dims(grid)
    walls={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==5}
    seeds=[(r,c) for r,c,v in nonzero(grid, ignore_colors={5})]
    closed=blocked_axis_closure(seeds, 'row', (h,w), walls)
    out=blank(h,w,0)
    place(out, walls, 5)
    place(out, closed, 8)
    return out
```


# Hard


## S18_H1 — Mini-Legend Maps Each Color to a Closure Mode
**Skills:** legend parsing, per-color transformation library, mixed outputs

**Primitive note:** axis_closure becomes one entry in a small transform library; the puzzle is about reading which library entry belongs to which color.

**Scaffold:**

- Read the top two legend rows before looking at the scene.
- A legend pair says: this scene color uses row closure, column closure, double closure, or bridge-only mode.
- Apply the mapped transform to each color's scene cells and keep the scene colors.

**Train 1 input**

```text
20030040000
10020030000
99999999999
00000000300
02002040040
00000000000
00000000300
00000040040
00000000000
```
**Train 1 output**

```text
20030040000
10020030000
99999999999
00000000300
02222044440
00000044440
00000044440
00000044440
00000000000
```
**Train 2 input**

```text
02003004000
03001002000
99999999999
00000000400
02020000000
00000030030
02020000400
00000000000
00000000000
```
**Train 2 output**

```text
02003004000
03001002000
99999999999
00000000400
02220000400
02220033330
02220000400
00000000000
00000000000
```
**Test input**

```text
20030040000
20030010000
99999999999
00000000000
00200030030
00000000404
00000030030
00200000000
00000000000
```
**Expected test output**

```text
20030040000
20030010000
99999999999
00000000000
00200033330
00200033444
00200033330
00200000000
00000000000
```
**Written solution**

The top two rows form a legend: a nonzero color token in row 0 is paired with a mode code directly beneath it in row 1. After the separator row of 9s comes the actual scene. For each scene color, look up its mode and apply the corresponding transform: 1=row closure, 2=column closure, 3=row-then-column double closure, 4=bridge-only row fill. Keep the legend and separator unchanged, and transform the scene in place using the original scene colors.

**Reference program**

```python
def solve_S18_H1(grid):
    # first two rows legend, third row separator 9s, rest scene
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        color=grid[0][c]
        mode=grid[1][c]
        if color!=0 and mode in (1,2,3,4):
            mapping[color]=mode
    out=copyg(grid)
    for r in range(3,h):
        for c in range(w):
            if out[r][c] not in (0,9):
                out[r][c]=0
    by=defaultdict(list)
    for r in range(3,h):
        for c,v in enumerate(grid[r]):
            if v!=0 and v!=9:
                by[v].append((r,c))
    for color,cells in by.items():
        mode=mapping.get(color,1)
        if mode==1:
            transformed=axis_closure(cells,'row')
        elif mode==2:
            transformed=axis_closure(cells,'col')
        elif mode==3:
            transformed=double_closure(cells,'row','col')
        else:
            transformed=bridge_only(cells,'row')
        place(out, transformed, color)
    return out
```


## S18_H2 — Pairwise Overlap Matrix of Completed Closures
**Skills:** symbolic relation output, object ordering, double-closure overlap

**Primitive note:** The primitive produces comparable completed regions for each color-coded object; the answer is a symbolic overlap matrix between those regions.

**Scaffold:**

- Complete each colored object into its filled rectangle.
- Order the objects by color.
- Write an n×n matrix with 5 on the diagonal and 8 whenever two completed shapes overlap.

**Train 1 input**

```text
000000000000
020200004040
000303004040
020200000000
000303000000
000000000000
000000000000
```
**Train 1 output**

```text
580
850
005
```
**Train 2 input**

```text
0000000000000
0200303000000
0200200000000
0000303000000
0000000040400
0000000005050
0000000040400
0000000005050
```
**Train 2 output**

```text
5800
8500
0058
0085
```
**Test input**

```text
0000000040400
0200200000000
0000303040400
0200200005050
0000000000000
0000303005050
0000000000000
0000000000000
```
**Expected test output**

```text
5800
8500
0050
0005
```
**Written solution**

Each color is one object. Complete each colored object with row-then-column closure. Sort the colors in ascending order, then build a square relation matrix: place 5 on the diagonal and 8 whenever the completed closures of two colors overlap. Leave all other entries 0.

**Reference program**

```python
def solve_S18_H2(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    objs=[(color, double_closure(cells,'row','col')) for color,cells in sorted(by.items())]
    n=len(objs)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif objs[i][1] & objs[j][1]:
                out[i][j]=8
    return out
```


## S18_H3 — Pick the Object Whose Double Closure Is a True Rectangle
**Skills:** counterfactual shape test, double closure, cropped output

**Primitive note:** double_closure is used as a diagnostic transform on each color-coded object: whether the result saturates its bounding box becomes the selection criterion.

**Scaffold:**

- Treat each color as one candidate object.
- Complete every candidate with row closure followed by column closure.
- Exactly one color becomes a true filled rectangle. Output that completed shape, cropped.

**Train 1 input**

```text
000000000000
020020003030
000000000000
020020003000
000000000000
004040000000
000400000000
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
000000003000
020002000000
000000003030
000000000000
020002000000
000000040400
000000004000
000000000000
```
**Train 2 output**

```text
88888
88888
88888
88888
```
**Test input**

```text
0000000000000
0200002000000
0000000003030
0000000000000
0200002003000
0000000404000
0000000040000
0000000000000
```
**Expected test output**

```text
888888
888888
888888
888888
```
**Written solution**

Each nonzero color is a separate candidate. Compute the double closure of every color's cells. Some results are still L-like or sparse, but one of them exactly equals its full bounding box and is therefore a real filled rectangle. Choose that color and output its completed rectangle as a tight color-8 crop.

**Reference program**

```python
def solve_S18_H3(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    best_color=None
    best_closed=None
    best_area=-1
    for color,cells in sorted(by.items()):
        closed=double_closure(cells,'row','col')
        r1,c1,r2,c2=bbox(closed)
        area=(r2-r1+1)*(c2-c1+1)
        if len(closed)==area and area>best_area:
            best_area=area
            best_color=color
            best_closed=closed
    return crop_cells(best_closed, 8)
```


## S18_H4 — Majority Merge of Three Completed Panels
**Skills:** panel parsing, double closure, cell-wise majority

**Primitive note:** The closure primitive lifts sparse panel data into solid comparable masks; then a majority operator combines those masks.

**Scaffold:**

- Split the grid into three panels.
- Complete the sparse shape in each panel into its filled rectangle.
- Keep the cells that belong to at least two of the three completed panels.

**Train 1 input**

```text
00000090000009000000
02002090000009002002
00000090200209000000
02002090000009002002
00000090200209000000
00000090000009000000
```
**Train 1 output**

```text
000000
008880
088880
088880
000000
000000
```
**Train 2 input**

```text
02020090000009000000
00000090200209200200
02020090000009000000
00000090200209200200
00000090000009000000
00000090000009000000
```
**Train 2 output**

```text
000000
088800
088800
088800
000000
000000
```
**Test input**

```text
00000090202009000000
02020090000009002020
00000090000009000000
00000090202009000000
02020090000009002020
00000090000009000000
```
**Expected test output**

```text
000000
088800
088800
088800
008800
000000
```
**Written solution**

Each panel contains the corners of one rectangle. Complete all three rectangles separately using row-then-column closure, but keep them in the same panel coordinate system. Then take a cell-wise majority vote: a cell appears in the output if it is covered by at least two of the three completed panels. Output that majority shape as a single panel-sized grid in color 8.

**Reference program**

```python
def solve_S18_H4(grid):
    panels=panel_split_vertical(grid, 9)
    panel_shapes=[dims(p) for _,_,p in panels]
    assert len(set(panel_shapes))==1
    ph,pw=panel_shapes[0]
    counts=Counter()
    for _,_,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        closed=double_closure(cells,'row','col')
        for cell in closed:
            counts[cell]+=1
    out=blank(ph,pw,0)
    for cell,k in counts.items():
        if k>=2:
            out[cell[0]][cell[1]]=8
    return out
```


## S18_H5 — Target Mask Selects the Best Closure Match
**Skills:** cross-reference with target region, counterfactual closure, cropped output

**Primitive note:** axis_closure is used counterfactually here: you do not output the target itself, but the candidate object whose completed span best explains the target mask.

**Scaffold:**

- Ignore the target mask color when building candidates.
- For each candidate color, imagine its horizontal closure.
- Choose the candidate whose closed span matches the target region best, then output that closure cropped.

**Train 1 input**

```text
000000000000
000000030300
027720030300
027720000000
000000400040
000000000000
000000000000
```
**Train 1 output**

```text
8888
8888
```
**Train 2 input**

```text
000000000000
020200000000
000000000000
000000003030
000000003030
004777400000
000000000000
000000000000
```
**Train 2 output**

```text
88888
```
**Test input**

```text
000000000000
000000003730
000000003730
000000000000
020020000000
000000400400
000000000000
000000000000
```
**Expected test output**

```text
888
888
```
**Written solution**

The color-7 cells form a target mask. For each other color, close its markers horizontally and compare that hypothetical closure to the target. The best candidate is the one with the greatest overlap and the fewest extra cells beyond the target. Output that winning closure as a tight color-8 crop.

**Reference program**

```python
def solve_S18_H5(grid):
    target={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7}
    by=defaultdict(list)
    for r,c,v in nonzero(grid, ignore_colors={7}):
        by[v].append((r,c))
    best_color=None
    best_closed=None
    best_score=(-1,-10**9,-10**9)
    for color,cells in sorted(by.items()):
        closed=axis_closure(cells,'row')
        overlap=len(closed & target)
        extra=-len(closed - target)
        total=-len(closed)
        score=(overlap, extra, total)
        if score > best_score:
            best_score=score; best_color=color; best_closed=closed
    return crop_cells(best_closed, 8)
```


## S18_H6 — Blocked Double Closure Inside Walled Rooms
**Skills:** two-stage closure, walls as hard blockers, room-wise completion

**Primitive note:** This is a blocked, two-pass version of axis_closure. The walls define where interval completion is allowed to propagate.

**Scaffold:**

- Preserve the walls and treat them as absolute barriers.
- First do blocked row closure, then blocked column closure, always respecting the walls.
- The result fills orthogonally convex room regions implied by the corner markers.

**Train 1 input**

```text
5555555555555
5000005000005
5020205020205
5000005000005
5000005000005
5020205000005
5000005020205
5000005000005
5555555555555
```
**Train 1 output**

```text
5555555555555
5000005000005
5088805088805
5088805088805
5088805088805
5088805088805
5000005088805
5000005000005
5555555555555
```
**Train 2 input**

```text
55555555555555
50000005000005
50200205000005
50000005000005
50200205000005
55555555555555
50000005020205
50000005000005
50000005020205
55555555555555
```
**Train 2 output**

```text
55555555555555
50000005000005
50888805000005
50888805000005
50888805000005
55555555555555
50000005088805
50000005088805
50000005088805
55555555555555
```
**Test input**

```text
5555555555555
5020025000005
5000005000005
5000005020205
5020025000005
5000005000005
5000005020205
5000005000005
5555555555555
```
**Expected test output**

```text
5555555555555
5088885000005
5088885000005
5088885088805
5088885088805
5000005088805
5000005088805
5000005000005
5555555555555
```
**Written solution**

The seeds lie inside wall-bounded rooms. Close them horizontally, but only within wall-delimited row segments. Then take that result and close it vertically, again stopping at walls. Keep the wall cells as 5 and paint the completed room interiors 8.

**Reference program**

```python
def solve_S18_H6(grid):
    h,w=dims(grid)
    walls={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==5}
    seeds=[(r,c) for r,c,v in nonzero(grid, ignore_colors={5})]
    step1=blocked_axis_closure(seeds, 'row', (h,w), walls)
    step2=blocked_axis_closure(step1, 'col', (h,w), walls)
    out=blank(h,w,0)
    place(out, walls, 5)
    place(out, step2, 8)
    return out
```


## S18_H7 — Congruence Matrix of Completed Shapes
**Skills:** symbolic relation output, shape normalization, double closure

**Primitive note:** double_closure turns each color-coded sparse object into a canonical filled shape; normalization then supports an explicit congruence relation.

**Scaffold:**

- Complete each colored object into its filled rectangle.
- Normalize those completed shapes up to translation.
- Build a relation matrix that marks which color pairs have the same completed shape.

**Train 1 input**

```text
000000000000
020020030030
000000000000
020020030030
000000000000
040400005050
000000000000
040400005050
000000000000
```
**Train 1 output**

```text
5800
8500
0058
0085
```
**Train 2 input**

```text
00000000000000
02000200300030
02000200300030
00000000000000
00000000000000
00404000505000
00000000000000
00000000505000
00404000000000
00000000000000
```
**Train 2 output**

```text
5800
8500
0050
0005
```
**Test input**

```text
00000000000000
02020003030000
00000000000000
00000000000000
02020003030000
00000000000000
04000400500050
04000400500050
00000000000000
00000000000000
```
**Expected test output**

```text
5800
8500
0058
0085
```
**Written solution**

Treat each color as one object and complete it into a solid rectangle by row-then-column closure. Normalize those completed shapes up to translation, sort the objects by color, and output an n×n matrix with 5 on the diagonal and 8 whenever two colors have congruent completed shapes. All other cells stay 0.

**Reference program**

```python
def solve_S18_H7(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    objs=[(color, norm_cells(double_closure(cells,'row','col'))) for color,cells in sorted(by.items())]
    n=len(objs)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif objs[i][1]==objs[j][1]:
                out[i][j]=8
    return out
```

