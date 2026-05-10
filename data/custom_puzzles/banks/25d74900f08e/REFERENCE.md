# ARC-style Puzzle Bank — 21 more puzzles (set 14)

This fourteenth bank leans into a profile-and-projection style of ARC design. The core move is to stop treating an object as only a raw bitmap and instead treat it as a pair of one-dimensional signatures: how many cells it occupies in each row of its bounding box, and how many cells it occupies in each column. From there you can do a surprising amount: close gaps by spans, match objects up to horizontal shifts, build canonical histograms, compare panels symbolically, and fuse two different anchors into one output.

This set introduces a new helper primitive:

```text
profile_signature(cells, trim=True)
  Return the row and column occupancy counts of a component inside its tight bounding box. This supports closure-by-span, profile matching, histogram construction, and profile-based symbolic outputs.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set14_reference.py`.

## Index

### Easy

- **S14_E1** — Horizontal Span Closure

- **S14_E2** — Vertical Span Closure

- **S14_E3** — Crop the Highest Row Peak

- **S14_E4** — Recolor the Flat Row Profiles

- **S14_E5** — Crop the Highest Column Peak

- **S14_E6** — Header Chooses the Row Count

- **S14_E7** — Build the Row Histogram


### Medium

- **S14_M1** — Match the Anchor's Row Profile

- **S14_M2** — Header Chooses the Closure Axis

- **S14_M3** — Odd Object by Row Profile

- **S14_M4** — Column Histogram of the Largest Object

- **S14_M5** — Canonical Profile Intersection

- **S14_M6** — Stamp the Anchor's Row Histogram

- **S14_M7** — Match the Anchor's Column Profile Across Panels


### Hard

- **S14_H1** — Pairwise Row-Profile Match Matrix

- **S14_H2** — Dual-Anchor Row/Column Match

- **S14_H3** — Learn the Closure from the Example Panels

- **S14_H4** — Match the Reversed Column Profile

- **S14_H5** — Row-Profile Difference Histogram

- **S14_H6** — Majority Row Profile Across Panels

- **S14_H7** — Intersect Blue Rows with Red Columns


# Easy

## S14_E1 — Horizontal Span Closure
**Skills:** row profiles, same-size fill, component-wise reasoning

**Primitive note:** Uses profile_signature implicitly: each occupied row of each component defines a left/right span that should be closed.

**Scaffold:**

- Split the colored cells into separate connected components.
- Inside one component, look at each occupied row and find its leftmost and rightmost cell.
- Fill every cell between those two endpoints, keeping the component's original color.

**Train 1 input**

```text
00000000000000
02220000303000
02020000333000
02220000303000
00000000000000
00000444000000
00000040000000
00000040000000
00000000000000
```
**Train 1 output**

```text
00000000000000
02220000333000
02220000333000
02220000333000
00000000000000
00000444000000
00000040000000
00000040000000
00000000000000
```

**Train 2 input**

```text
000000000000000
066660000777000
060060000707000
060060000777000
000000000000000
000000000000000
000000300000000
000000330000000
000000333000000
000000000000000
```
**Train 2 output**

```text
000000000000000
066660000777000
066660000777000
066660000777000
000000000000000
000000000000000
000000300000000
000000330000000
000000333000000
000000000000000
```

**Test input**

```text
000000000000000
002020000444400
002220000400400
002020000400400
000000000000000
000000070000000
000000777000000
000000070000000
000000000000000
```
**Test output**

```text
000000000000000
002220000444400
002220000444400
002220000444400
000000000000000
000000070000000
000000777000000
000000070000000
000000000000000
```

**Written solution:** Treat each object independently. For every occupied row in that object, take the segment from the row's first filled cell to its last filled cell and fill the whole segment. Rows that already have no gaps stay the same, while rows like 1-0-1 become solid bars. Put the filled rows back into the original grid with the original colors.

**Reference program**

```python
def solve_S14_E1(grid):
    return row_fill_same_size_excluding(grid)
```

## S14_E2 — Vertical Span Closure
**Skills:** column profiles, same-size fill, component-wise reasoning

**Primitive note:** This is the column-wise sibling of E1: use the component's column profile to close vertical gaps.

**Scaffold:**

- Again, reason one connected object at a time.
- For each occupied column, find the topmost and bottommost filled cell of that object.
- Fill the full vertical segment between them in the object's own color.

**Train 1 input**

```text
000000000000000
022200003330000
020200003000000
022200003000000
000000003330000
000000000000000
000004440000000
000000400000000
000000400000000
000000000000000
```
**Train 1 output**

```text
000000000000000
022200003330000
022200003330000
022200003330000
000000003330000
000000000000000
000004440000000
000000400000000
000000400000000
000000000000000
```

**Train 2 input**

```text
000000000000000
066600000777000
006000000707000
006000000777000
066600000000000
000000000000000
000000444000000
000000444000000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000000000
066600000777000
066600000777000
066600000777000
066600000000000
000000000000000
000000444000000
000000444000000
000000000000000
000000000000000
```

**Test input**

```text
0000000000000000
0022200000444000
0020000000404000
0020000000444000
0022200000000000
0000000000000000
0000006000000000
0000006600000000
0000006660000000
0000000000000000
```
**Test output**

```text
0000000000000000
0022200000444000
0022200000444000
0022200000444000
0022200000000000
0000000000000000
0000006000000000
0000006600000000
0000006660000000
0000000000000000
```

**Written solution:** The rule is the vertical version of span closure. For each object, inspect every column that contains object cells. If a column has two separated occupied cells, fill the gap between them. Apply that to all columns of all objects and keep the original colors.

**Reference program**

```python
def solve_S14_E2(grid):
    return col_fill_same_size_excluding(grid)
```

## S14_E3 — Crop the Highest Row Peak
**Skills:** row-profile peak, object selection, cropping

**Primitive note:** Directly uses profile_signature: select the component whose row profile has the largest entry.

**Scaffold:**

- Compute the row profile of every object inside its tight bounding box.
- Find the largest single row count achieved by each object.
- Choose the object with the highest such peak and crop it out.

**Train 1 input**

```text
000000000000000
022220003030000
022220003330000
000000003030000
000000000000400
000000000000400
000000000000400
000000000000400
000000000000000
```
**Train 1 output**

```text
8888
8888
```

**Train 2 input**

```text
0000000000000000
0006000000222200
0066600000200200
0666660000200200
0000000000000000
0000000000000000
0000000333000000
0000000030000000
0000000030000000
0000000000000000
```
**Train 2 output**

```text
00800
08880
88888
```

**Test input**

```text
0000000000000000
0444400022200000
0400400020000000
0400400020000000
0000000022200000
0000000000000700
0000000000007770
0000000000000700
0000000000000000
```
**Test output**

```text
8888
8008
8008
```

**Written solution:** For each component, count how many cells appear in each row of its bounding box. The winning object is the one whose most crowded row is the largest among all candidates. After selecting it, crop to its bounding box and recolor the cropped object to cyan(8).

**Reference program**

```python
def solve_S14_E3(grid):
    comps = components(grid)
    target = max(
        comps,
        key=lambda comp: (
            max_row_peak(comp),
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    return crop_component(target, 8)
```

## S14_E4 — Recolor the Flat Row Profiles
**Skills:** row-profile regularity, same-size recolor, component filtering

**Primitive note:** A component qualifies when all entries of its row profile are equal.

**Scaffold:**

- Measure the row profile of every object.
- Check whether every occupied row contains the same number of cells.
- Recolor only those regular-profile objects to cyan(8).

**Train 1 input**

```text
000000000000000
022200003000000
022200003300000
000000003330000
000000000000400
000000000000400
000000000000400
000000000000400
000000000000000
```
**Train 1 output**

```text
000000000000000
088800003000000
088800003300000
000000003330000
000000000000800
000000000000800
000000000000800
000000000000800
000000000000000
```

**Train 2 input**

```text
0000000000000000
0666600002020000
0666600002220000
0000000002020000
0000000000000000
0000000000000700
0000000000000700
0000000000000700
0000000000000000
0000000000000000
```
**Train 2 output**

```text
0000000000000000
0888800002020000
0888800002220000
0000000002020000
0000000000000000
0000000000000800
0000000000000800
0000000000000800
0000000000000000
0000000000000000
```

**Test input**

```text
000000000000000
004440000666000
004440000606000
000000000666000
000000000000030
000000000000030
000000000000030
000000000000030
000000000000000
```
**Test output**

```text
000000000000000
008880000666000
008880000606000
000000000666000
000000000000080
000000000000080
000000000000080
000000000000080
000000000000000
```

**Written solution:** Look at each object's row counts inside its bounding box. If every row count is the same, that object belongs to the target class; otherwise it does not. Keep the whole grid the same size and recolor exactly the qualifying objects to cyan(8).

**Reference program**

```python
def solve_S14_E4(grid):
    return recolor_same_size(grid, constant_row_profile, 8)
```

## S14_E5 — Crop the Highest Column Peak
**Skills:** column-profile peak, object selection, cropping

**Primitive note:** The column analogue of E3: use the biggest entry in the column profile.

**Scaffold:**

- Compute a column profile for each object.
- Record the largest value appearing in that profile.
- Pick the object with the biggest column peak, crop it, and recolor it.

**Train 1 input**

```text
000000000000000
022200003333000
020000003333000
020000000000000
022200000000000
000000000000040
000000000000444
000000000000040
000000000000000
```
**Train 1 output**

```text
888
800
800
888
```

**Train 2 input**

```text
000000000000000
060000022200000
060000022200000
060000000000000
060000000000000
000000000004000
000000000004400
000000000004440
000000000000000
000000000000000
```
**Train 2 output**

```text
8
8
8
8
```

**Test input**

```text
000000000000000
077700000303000
007000000333000
007000000303000
077700000000000
000000000000444
000000000000444
000000000000000
000000000000000
```
**Test output**

```text
888
080
080
888
```

**Written solution:** This time the deciding statistic is vertical rather than horizontal. For each object, count cells per column inside its bounding box and note the largest column count. The object with the highest column peak wins. Crop that object and recolor it to cyan(8).

**Reference program**

```python
def solve_S14_E5(grid):
    comps = components(grid)
    target = max(
        comps,
        key=lambda comp: (
            max_col_peak(comp),
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    return crop_component(target, 8)
```

## S14_E6 — Header Chooses the Row Count
**Skills:** header decoding, row-count selection, cropping

**Primitive note:** The top-row blue header encodes the target bounding-box height by the number of blue cells.

**Scaffold:**

- Read the number of blue header cells in the top row.
- For each object below the header, count how many rows its bounding box occupies.
- Choose the object whose row count matches the header and crop it out.

**Train 1 input**

```text
1110000000000000
0000000000000000
0020000033304440
0222000033304000
0020000000004000
0000000000004440
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Train 1 output**

```text
080
888
080
```

**Train 2 input**

```text
11110000000000000
00000000000000000
06666000020077700
06666000020007000
00000000020007000
00000000000077700
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Train 2 output**

```text
888
080
080
888
```

**Test input**

```text
110000000000000
000000000000000
044440003330060
044440003030060
000000003330060
000000000000060
000000000000000
000000000000000
000000000000000
```
**Test output**

```text
8888
8888
```

**Written solution:** The blue cells in the top row form a little numeric header: their count tells you how many rows the target object occupies. Ignore the header itself, compare that number to each object's bounding-box height, and select the unique match. Output the cropped matching object recolored to cyan(8).

**Reference program**

```python
def solve_S14_E6(grid):
    h, w = dims(grid)
    k = sum(1 for c in range(w) if grid[0][c] == 1)
    comps = components([row[:] for row in grid[1:]])
    target = next(
        comp
        for comp in sorted(comps, key=top_left_of_comp)
        if len(row_profile_cells(comp["cells"])) == k
    )
    return crop_component(target, 8)
```

## S14_E7 — Build the Row Histogram
**Skills:** profile extraction, constructive output, normalization

**Primitive note:** A direct use of profile_signature: convert the row profile into a left-justified histogram.

**Scaffold:**

- Take the single object and crop to its bounding box conceptually.
- Count how many cells appear in each row of that box.
- Create a new blank grid whose rows are left-justified cyan bars of those lengths.

**Train 1 input**

```text
0000000000
0000000000
0000200000
0000220000
0000222000
0000000000
0000000000
0000000000
```
**Train 1 output**

```text
800
880
888
```

**Train 2 input**

```text
000000000000
000000000000
000003030000
000003330000
000003030000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 output**

```text
880
888
880
```

**Test input**

```text
000000000000
000000000000
000066600000
000060000000
000060000000
000066600000
000000000000
000000000000
000000000000
```
**Test output**

```text
888
800
800
888
```

**Written solution:** Extract the object's row profile, then forget the original horizontal placement. Build a new canonical shape: row i contains exactly as many cyan cells as the original object had in row i, all packed flush to the left. The output is just that histogram, with no extra background around it.

**Reference program**

```python
def solve_S14_E7(grid):
    comp = single_largest_component(grid)
    return row_histogram_from_profile(row_profile_cells(comp["cells"]), 8)
```

# Medium

## S14_M1 — Match the Anchor's Row Profile
**Skills:** anchor matching, profile invariance, cropping

**Primitive note:** Compare candidates to the anchor using only row-profile equality, ignoring color and internal horizontal shifts.

**Scaffold:**

- The blue anchor object gives the target row profile.
- Compute the row profile of every non-anchor candidate.
- Choose the candidate with the exact same row-count list and crop it out.

**Train 1 input**

```text
00000000000000000
01000000004006060
01100000044006660
01110000444006060
00000000000000000
00000000000000000
00000000007770000
00000000000700000
00000000000700000
00000000000000000
```
**Train 1 output**

```text
008
088
888
```

**Train 2 input**

```text
000000000000000000
011100000444006666
010000000040006006
010000000040006006
011100000444000000
000000000000000000
000000000007770000
000000000000070000
000000000000070000
000000000000000000
000000000000000000
```
**Train 2 output**

```text
888
080
080
888
```

**Test input**

```text
00000000000000000
01110000044400606
01010000044000666
01110000044400606
00000000000000000
00000000000000000
00000000007777000
00000000007777000
00000000000000000
00000000000000000
```
**Test output**

```text
888
880
888
```

**Written solution:** Use the blue anchor as a template, but only in terms of row counts. A candidate matches even if its rows are shifted left or right inside its own box, as long as the sequence of row occupancies is identical. Find that candidate and output its cropped silhouette recolored to cyan(8).

**Reference program**

```python
def solve_S14_M1(grid):
    comps = components(grid)
    anchor = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] != 1], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == row_profile_cells(anchor["cells"])
    )
    return crop_component(target, 8)
```

## S14_M2 — Header Chooses the Closure Axis
**Skills:** header-controlled transform, row vs column reasoning, same-size fill

**Primitive note:** Header color 1 means horizontal span closure; header color 2 means vertical span closure.

**Scaffold:**

- First decode the header cell in the top-left corner.
- If it says row mode, close gaps across rows; if it says column mode, close gaps down columns.
- Apply the chosen closure to every non-header object in the grid.

**Train 1 input**

```text
1000000000000000
0000000000000000
0333000004440000
0303000004000000
0333000004000000
0000000004440000
0000000600000000
0000006660000000
0000000600000000
0000000000000000
```
**Train 1 output**

```text
1000000000000000
0000000000000000
0333000004440000
0333000004000000
0333000004000000
0000000004440000
0000000600000000
0000006660000000
0000000600000000
0000000000000000
```

**Train 2 input**

```text
2000000000000000
0000000000000000
0333000004440000
0303000004000000
0333000004000000
0000000004440000
0000000600000000
0000006660000000
0000000600000000
0000000000000000
```
**Train 2 output**

```text
2000000000000000
0000000000000000
0333000004440000
0333000004440000
0333000004440000
0000000004440000
0000000600000000
0000006660000000
0000000600000000
0000000000000000
```

**Test input**

```text
20000000000000000
00000000000000000
07777000006660000
07007000006060000
07007000006660000
00000000000000000
00000000000000000
00000004440000000
00000004440000000
00000000000000000
00000000000000000
```
**Test output**

```text
20000000000000000
00000000000000000
07777000006660000
07007000006660000
07007000006660000
00000000000000000
00000000000000000
00000004440000000
00000004440000000
00000000000000000
00000000000000000
```

**Written solution:** There are two possible transforms, and the header tells you which one to use. A blue-ish header cell with value 1 means horizontal span closure, while value 2 means vertical span closure. Ignore the header itself and apply the selected closure rule to all the other objects in place.

**Reference program**

```python
def solve_S14_M2(grid):
    mode = "row" if grid[0][0] == 1 else "col"
    if mode == "row":
        return row_fill_same_size_excluding(grid, banned_colors=(1, 2))
    return col_fill_same_size_excluding(grid, banned_colors=(1, 2))
```

## S14_M3 — Odd Object by Row Profile
**Skills:** classification, profile equivalence classes, cropping

**Primitive note:** Group components by row-profile signature; the target is the lone member of its class.

**Scaffold:**

- Compute the row profile of every object.
- Group objects that share the same row-profile signature.
- Find the one object whose profile class appears only once and crop it.

**Train 1 input**

```text
000000000000000000
020000000300004000
022000003300004400
022200033300044400
000000000000000000
000000000000000000
000000000606000000
000000000666000000
000000000606000000
000000000000000000
```
**Train 1 output**

```text
808
888
808
```

**Train 2 input**

```text
0000000000000000000
0222000333000444000
0020000003000040000
0020000003000040000
0000000000000000000
0000000000000000000
0000000000600000000
0000000006660000000
0000000000600000000
0000000000000000000
0000000000000000000
```
**Train 2 output**

```text
080
888
080
```

**Test input**

```text
000000000000000000
022200033300044400
020200033000004400
022200033300044400
000000000000000000
000000000000000000
000000000666000000
000000000666000000
000000000000000000
000000000000000000
```
**Test output**

```text
888
888
```

**Written solution:** Most of the objects belong to the same row-profile family, even though their exact shapes or colors may differ. The target is the outlier whose row-count sequence is unique. After finding that odd profile class, crop the outlier object and recolor it to cyan(8).

**Reference program**

```python
def solve_S14_M3(grid):
    comps = components(grid)
    profiles = [tuple(row_profile_cells(comp["cells"])) for comp in comps]
    counts = Counter(profiles)
    target = next(
        comp
        for comp in sorted(comps, key=top_left_of_comp)
        if counts[tuple(row_profile_cells(comp["cells"]))] == 1
    )
    return crop_component(target, 8)
```

## S14_M4 — Column Histogram of the Largest Object
**Skills:** size ranking, column profiles, constructive output

**Primitive note:** Select by component area first, then convert the winner's column profile into a top-justified histogram.

**Scaffold:**

- Find the largest object by number of cells.
- Compute how many cells it contains in each column of its bounding box.
- Build a new cyan histogram with those column counts stacked from the top.

**Train 1 input**

```text
00000000000000000
02220000303000000
02000000333000000
02000000303000000
02220000000000000
00000000000000000
00000000000004440
00000000000000400
00000000000000400
00000000000000000
```
**Train 1 output**

```text
888
888
800
800
```

**Train 2 input**

```text
000000000000000000
060000000022220000
066000000020020000
066600000020020000
066660000000000000
000000000000000000
000000000000000000
000000000000000400
000000000000004440
000000000000000400
000000000000000000
```
**Train 2 output**

```text
8888
8880
8800
8000
```

**Test input**

```text
000000000000000000
000700000033330000
007770000033330000
077777000000000000
000000000000000000
000000000000000040
000000000000000040
000000000000000040
000000000000000040
000000000000000000
```
**Test output**

```text
88888
08880
00800
```

**Written solution:** First identify the largest component in the scene. Then read off its column profile and turn that one-dimensional signature into a canonical output: each column becomes a top-justified cyan bar whose height equals the original count in that column. The result is a compact histogram of the winner's column profile.

**Reference program**

```python
def solve_S14_M4(grid):
    comp = single_largest_component(grid)
    return col_histogram_from_profile(col_profile_cells(comp["cells"]), 8)
```

## S14_M5 — Canonical Profile Intersection
**Skills:** row/column fusion, canonicalization, constructive output

**Primitive note:** Use profile_signature fully: build the left-justified row histogram and the top-justified column histogram, then keep their intersection.

**Scaffold:**

- Measure both the row profile and the column profile of the object.
- Imagine the canonical row histogram and the canonical column histogram for those profiles.
- Output the cells that belong to both canonical histograms at once.

**Train 1 input**

```text
0000000000
0000000000
0002020000
0002220000
0002020000
0000000000
0000000000
0000000000
```
**Train 1 output**

```text
880
808
800
```

**Train 2 input**

```text
0000000000
0000000000
0003000000
0003300000
0003330000
0000000000
0000000000
0000000000
```
**Train 2 output**

```text
800
880
800
```

**Test input**

```text
000000000000
000000000000
000066660000
000060060000
000060060000
000000000000
000000000000
000000000000
000000000000
```
**Test output**

```text
8888
8000
8000
```

**Written solution:** This puzzle asks for a canonical object built from both one-dimensional projections. Make the left-justified row histogram implied by the row profile, and independently make the top-justified column histogram implied by the column profile. The output is the intersection of those two canonical constructions, drawn in cyan(8).

**Reference program**

```python
def solve_S14_M5(grid):
    comp = single_largest_component(grid)
    sig = profile_signature(comp["cells"])
    return canonical_intersection_shape(sig["rows"], sig["cols"], 8)
```

## S14_M6 — Stamp the Anchor's Row Histogram
**Skills:** marker transport, profile extraction, constructive placement

**Primitive note:** Extract the anchor's row profile, turn it into a histogram, and stamp that histogram at the marker location.

**Scaffold:**

- Ignore the marker at first and compute the anchor object's row profile.
- Convert that profile into a left-justified histogram shape.
- Place that histogram with its top-left corner at the marker cell on an otherwise blank grid.

**Train 1 input**

```text
0000000000000000
0333000000000000
0300000000000000
0300000000000000
0333000000000000
0000000000000000
0000000000000000
0000000000100000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Train 1 output**

```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000888000
0000000000800000
0000000000800000
0000000000888000
0000000000000000
```

**Train 2 input**

```text
000000000000000
040000000000000
044000000000000
044400000000000
000000000000000
000000000000000
000000000100000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000800000
000000000880000
000000000888000
000000000000000
000000000000000
```

**Test input**

```text
00000000000000000
00666000000000000
00606000000000000
00666000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000100000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Test output**

```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000888000
00000000000880000
00000000000888000
00000000000000000
00000000000000000
```

**Written solution:** The original object is only a source of profile information. Read its row counts, convert them to the corresponding left-justified histogram, and then redraw that histogram somewhere else: the single blue marker cell gives the new top-left placement. The output contains only the stamped cyan histogram.

**Reference program**

```python
def solve_S14_M6(grid):
    comps = [comp for comp in components(grid) if comp["color"] != 1]
    anchor = max(
        comps,
        key=lambda comp: (
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    marker = detect_marker(grid, 1)
    profile = row_profile_cells(anchor["cells"])
    shape = row_histogram_from_profile(profile, 1)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                out[marker[0] + r][marker[1] + c] = 8
    return out
```

## S14_M7 — Match the Anchor's Column Profile Across Panels
**Skills:** panel parsing, cross-panel matching, column profiles

**Primitive note:** The separator splits the grid into panels. Use the first panel's object as the column-profile anchor and search in the second panel.

**Scaffold:**

- Split the input at the full-height separator column.
- Compute the anchor object's column profile in the left panel.
- In the right panel, select the candidate with the same column profile and crop it.

**Train 1 input**

```text
0000000500000000000
0000000500000000000
0020000504000000060
0022000504400000660
0022200504440006660
0000000500000000000
0000000500000000000
0000000500000000000
```
**Train 1 output**

```text
800
880
888
```

**Train 2 input**

```text
00000005000000000000
00000005000000000000
00222005044400066660
00200005040000060060
00200005040000060060
00222005044400000000
00000005000000000000
00000005000000000000
00000005000000000000
```
**Train 2 output**

```text
888
800
800
888
```

**Test input**

```text
00000005000000000000
00000005000000000000
00222005040400006660
00202005044400006060
00222005040400006660
00000005000000000000
00000005000000000000
00000005000000000000
```
**Test output**

```text
888
808
888
```

**Written solution:** The left panel provides the template, but only in terms of column counts. Compare the anchor's column profile to the candidates in the right panel and find the exact match, ignoring color. Crop that matched candidate and recolor it to cyan(8).

**Reference program**

```python
def solve_S14_M7(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    anchor = single_largest_component(panels[0])
    target = next(
        comp
        for comp in sorted(components(panels[1]), key=top_left_of_comp)
        if col_profile_cells(comp["cells"]) == col_profile_cells(anchor["cells"])
    )
    return crop_component(target, 8)
```

# Hard

## S14_H1 — Pairwise Row-Profile Match Matrix
**Skills:** symbolic output, pairwise comparison, matrix construction

**Primitive note:** Sort objects in reading order, then compare every pair by row-profile equality.

**Scaffold:**

- List the objects in reading order from top-left to bottom-right.
- For each ordered pair, ask whether the two objects have the same row profile.
- Write an output matrix with cyan(8) for matches and black(0) otherwise.

**Train 1 input**

```text
00000000000000000000
02000000003000040400
02200000033000044400
02220000333000040400
00000000000000000000
00000000000000000000
00000000006000000000
00000000066600000000
00000000006000000000
00000000000000000000
00000000000000000000
```
**Train 1 output**

```text
8800
8800
0080
0008
```

**Train 2 input**

```text
0000000000000000000000
0222000033300004440000
0020000000300004040000
0020000000300004440000
0000000000000000000000
0000000000000000000000
0000000000000000000000
0000000006660000000000
0000000006600000000000
0000000006660000000000
0000000000000000000000
0000000000000000000000
```
**Train 2 output**

```text
8800
8800
0088
0088
```

**Test input**

```text
00000000000000000000
02220000333000044400
02020000330000004400
02220000333000044400
00000000000000000000
00000000000000000000
00000000066600000000
00000000066600000000
00000000000000000000
00000000000000000000
00000000000000000000
```
**Test output**

```text
8880
8880
8880
0008
```

**Written solution:** This is no longer a selection task but a relational one. Order the objects by position, compute each row-profile signature, and compare every object to every other object. The output is a square matrix whose (i,j) cell is cyan(8) exactly when object i and object j share the same row profile.

**Reference program**

```python
def solve_S14_H1(grid):
    comps = sorted(components(grid), key=top_left_of_comp)
    profiles = [tuple(row_profile_cells(comp["cells"])) for comp in comps]
    n = len(comps)
    out = blank(n, n, 0)
    for i in range(n):
        for j in range(n):
            if profiles[i] == profiles[j]:
                out[i][j] = 8
    return out
```

## S14_H2 — Dual-Anchor Row/Column Match
**Skills:** multi-constraint matching, row profiles, column profiles

**Primitive note:** The blue anchor supplies the target row profile; the red anchor supplies the target column profile.

**Scaffold:**

- Compute the row profile of the blue anchor.
- Compute the column profile of the red anchor.
- Among the remaining candidates, find the one matching both constraints simultaneously.

**Train 1 input**

```text
00000000000000000000
01000000020000040000
01100000022000044000
01110000222000444000
00000000000000000000
00000000000000000000
00000000060000707000
00000000066000777000
00000000066600707000
00000000000000000000
00000000000000000000
```
**Train 1 output**

```text
080
088
888
```

**Train 2 input**

```text
0000000000000000000000
0111000022200004440000
0100000002000000400000
0100000002000000400000
0111000022200004440000
0000000000000000000000
0000000000000000000000
0000000066600007777000
0000000060000007007000
0000000060000007007000
0000000066600000000000
0000000000000000000000
```
**Train 2 output**

```text
888
080
080
888
```

**Test input**

```text
000000000000000000000
011100002220000444000
010100000220000044000
011100002220000444000
000000000000000000000
000000000000000000000
000000000666000707000
000000000606000777000
000000000666000707000
000000000000000000000
000000000000000000000
```
**Test output**

```text
888
088
888
```

**Written solution:** Each anchor contributes a different part of the target description. The blue anchor tells you what the candidate's row profile must be, and the red anchor tells you what its column profile must be. Only one candidate satisfies both signatures at the same time; crop that object and recolor it to cyan(8).

**Reference program**

```python
def solve_S14_H2(grid):
    comps = components(grid)
    blue = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    red = min([comp for comp in comps if comp["color"] == 2], key=top_left_of_comp)
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] not in (1, 2)], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == row_profile_cells(blue["cells"])
        and col_profile_cells(comp["cells"]) == col_profile_cells(red["cells"])
    )
    return crop_component(target, 8)
```

## S14_H3 — Learn the Closure from the Example Panels
**Skills:** analogy, meta-transform detection, panel reasoning

**Primitive note:** Infer whether the example pair uses horizontal or vertical closure, then apply that same closure to the third panel.

**Scaffold:**

- Compare panel 1 to panel 2 and determine which closure rule turned one into the other.
- Do not assume the axis in advance; it can differ from example to example.
- Apply the detected closure rule to the object in panel 3 and output the cropped result.

**Train 1 input**

```text
00000005000000050000000
00000005000000050000000
00222005002220050040400
00202005002220050044400
00222005002220050040400
00000005000000050000000
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Train 1 output**

```text
888
888
888
```

**Train 2 input**

```text
00000005000000050000000
00000005000000050000000
00222005002220050044400
00200005002220050040400
00200005002220050044400
00222005002220050000000
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Train 2 output**

```text
888
888
888
```

**Test input**

```text
00000005000000050000000
00000005000000050000000
02222005022220050044400
02002005022220050040400
02002005022220050044400
00000005000000050000000
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Test output**

```text
888
888
888
```

**Written solution:** The first two panels form a worked example. Detect whether panel 2 is the row-span closure or the column-span closure of panel 1. Once that example transform is identified, apply the same closure rule to the third panel's object and return the cropped transformed object in cyan(8).

**Reference program**

```python
def solve_S14_H3(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    if row_fill_same_size_excluding(panels[0]) == panels[1]:
        transformed = row_fill_same_size_excluding(panels[2])
    else:
        transformed = col_fill_same_size_excluding(panels[2])
    target = single_largest_component(transformed)
    return crop_component(target, 8)
```

## S14_H4 — Match the Reversed Column Profile
**Skills:** cross-axis comparison, reversal, object selection

**Primitive note:** Take the anchor's column profile, reverse its order, and use that reversed list as a row-profile target for the candidates.

**Scaffold:**

- Compute the anchor object's column profile.
- Reverse that list from top-to-bottom order into bottom-to-top order.
- Choose the candidate whose row profile equals the reversed list.

**Train 1 input**

```text
00000000000000000000
00010000444000600000
00110000440000660000
01110000400000666000
00000000000000000000
00000000000000000000
00000000007070000000
00000000007770000000
00000000007070000000
00000000000000000000
00000000000000000000
```
**Train 1 output**

```text
888
880
800
```

**Train 2 input**

```text
0000000000000000000000
0111000000440000066000
0100000000440000666600
0100000004444000066000
0111000000000000000000
0000000000000000000000
0000000000000000000000
0000000000777000000000
0000000000070000000000
0000000000070000000000
0000000000000000000000
0000000000000000000000
```
**Train 2 output**

```text
0880
0880
8888
```

**Test input**

```text
00000000000000000000
01111000044400066600
01001000040000006000
01001000040000066600
00000000044400000000
00000000000000000000
00000000007770000000
00000000000700000000
00000000000700000000
00000000000000000000
00000000000000000000
```
**Test output**

```text
888
800
800
888
```

**Written solution:** This puzzle mixes axes and order. Start from the anchor's column counts, reverse the sequence, and then treat that reversed sequence as the desired row profile. Search the candidates for the unique object with exactly that row-count list, then crop and recolor it to cyan(8).

**Reference program**

```python
def solve_S14_H4(grid):
    comps = components(grid)
    anchor = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    target_profile = list(reversed(col_profile_cells(anchor["cells"])))
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] != 1], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == target_profile
    )
    return crop_component(target, 8)
```

## S14_H5 — Row-Profile Difference Histogram
**Skills:** panel comparison, numeric profile reasoning, constructive output

**Primitive note:** Take absolute row-profile differences between the two panels, padding the shorter profile with zeros if needed.

**Scaffold:**

- Read the row profile of the left-panel object and the right-panel object.
- Pad the shorter list with zeros so the profiles have the same length.
- Take absolute differences row by row and draw the resulting cyan histogram.

**Train 1 input**

```text
000000050000000
000000050000000
002000050044400
002200050004000
002220050004000
000000050000000
000000050000000
000000050000000
```
**Train 1 output**

```text
88
80
88
```

**Train 2 input**

```text
000000050000000
000000050000000
002220050044400
002000050040400
002000050044400
002220050000000
000000050000000
000000050000000
000000050000000
```
**Train 2 output**

```text
000
800
880
888
```

**Test input**

```text
00000000500000000
00000000500000000
00222200500040000
00200200500444000
00200200504444400
00000000500000000
00000000500000000
00000000500000000
00000000500000000
```
**Test output**

```text
888
800
888
```

**Written solution:** The output is not derived from either object alone but from their numerical difference. Compute the two row profiles, align them by row index, pad with zeros when one profile is shorter, and take the absolute difference at each position. Then render that difference list as a left-justified cyan histogram.

**Reference program**

```python
def solve_S14_H5(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    a = single_largest_component(panels[0])
    b = single_largest_component(panels[1])
    ra = row_profile_cells(a["cells"])
    rb = row_profile_cells(b["cells"])
    L = max(len(ra), len(rb))
    ra = ra + [0] * (L - len(ra))
    rb = rb + [0] * (L - len(rb))
    diff = [abs(x - y) for x, y in zip(ra, rb)]
    return row_histogram_from_profile(diff, 8)
```

## S14_H6 — Majority Row Profile Across Panels
**Skills:** consensus reasoning, profile classes, constructive output

**Primitive note:** Find the row-profile class that appears in at least two panels, then output its canonical histogram.

**Scaffold:**

- Compute one row profile per panel.
- Identify which profile signature occurs more than once.
- Output the row histogram corresponding to that majority signature.

**Train 1 input**

```text
00000005000000050000000
00000005000000050000000
00200005000400050060600
00220005000440050066600
00222005004440050060600
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Train 1 output**

```text
800
880
888
```

**Train 2 input**

```text
00000005000000050000000
00000005000000050000000
00222005004440050666600
00200005000400050600600
00200005000400050600600
00222005004440050000000
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Train 2 output**

```text
888
800
800
888
```

**Test input**

```text
00000005000000050000000
00000005000000050000000
00222005004440050066600
00202005004400050006000
00222005004440050006000
00000005000000050000000
00000005000000050000000
00000005000000050000000
```
**Test output**

```text
888
880
888
```

**Written solution:** Two of the three panels agree on the same row-profile signature, even if their exact shapes are not identical. Ignore the outlier, keep the majority profile, and convert that profile into the canonical left-justified cyan histogram. The output is therefore a consensus summary rather than one of the raw input objects.

**Reference program**

```python
def solve_S14_H6(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    profiles = []
    for panel in panels:
        comp = single_largest_component(panel)
        profiles.append(tuple(row_profile_cells(comp["cells"])))
    counts = Counter(profiles)
    majority = max(counts.items(), key=lambda kv: (kv[1], sum(kv[0]), len(kv[0])))[0]
    return row_histogram_from_profile(list(majority), 8)
```

## S14_H7 — Intersect Blue Rows with Red Columns
**Skills:** dual-source construction, row/column fusion, canonical output

**Primitive note:** Blue contributes row counts, red contributes column counts; the output is the intersection of the corresponding canonical histograms.

**Scaffold:**

- Extract the blue object's row profile.
- Extract the red object's column profile.
- Build the canonical row- and column-histogram shapes and keep only their overlap.

**Train 1 input**

```text
000000000000000000
010000000002000000
011000000022000000
011100000222000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 1 output**

```text
800
080
008
```

**Train 2 input**

```text
00000000000000000000
01110000002220000000
01000000000200000000
01000000000200000000
01110000002220000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```
**Train 2 output**

```text
888
800
000
080
```

**Test input**

```text
000000000000000000
011100000222000000
010100000022000000
011100000222000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Test output**

```text
888
880
088
```

**Written solution:** The two anchors control different dimensions of the construction. Use the blue object only for row counts and the red object only for column counts. Build the canonical left-justified row histogram and the canonical top-justified column histogram, intersect them, and draw the overlap in cyan(8).

**Reference program**

```python
def solve_S14_H7(grid):
    comps = components(grid)
    blue = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    red = min([comp for comp in comps if comp["color"] == 2], key=top_left_of_comp)
    rows = row_profile_cells(blue["cells"])
    cols = col_profile_cells(red["cells"])
    return canonical_intersection_shape(rows, cols, 8)
```

