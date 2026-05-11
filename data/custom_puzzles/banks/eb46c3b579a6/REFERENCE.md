# ARC-style Puzzle Bank — 21 more puzzles (set 16)

This sixteenth bank leans into **connector geometry, alignment, segment-defined regions, and symbolic outputs**. The puzzles are not all just 'draw a line'; the more interesting ones use line segments as probes, selectors, boundaries, or symbolic measurements. A span can become a midpoint, an intersection, a rectangle edge, a filled band, a silhouette row, a diamond boundary, or even an entry in an alignment matrix.

The core primitive introduced here is:

```text
span_cells(a, b, include_ends=True)
Return the lattice cells on the horizontal, vertical, or 45° diagonal segment between
two aligned points. This makes connector drawing, midpoint extraction, rectangle
synthesis, band filling, diamond edges, and alignment-based symbolic outputs explicit.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set16_reference.py`.

## Index

### Easy

- **S16_E1** — Connect the Two Markers

- **S16_E2** — Draw Only the Interior of the Segment

- **S16_E3** — Mark the Segment Midpoint

- **S16_E4** — Rectangle Border from Corner Markers

- **S16_E5** — Output Only the Span Intersection

- **S16_E6** — Longest Pair Wins

- **S16_E7** — Turn the Segment Length into a Bar


### Medium

- **S16_M1** — Legend Chooses Which Pair to Connect

- **S16_M2** — Draw the Full Cross from Two Pairs

- **S16_M3** — Fill the Rectangle from Opposite Corners

- **S16_M4** — Draw Every Pair in Its Own Color

- **S16_M5** — Crop the Object Hit by the Connector

- **S16_M6** — Fill the Band Between Parallel Pairs

- **S16_M7** — Complete the Rectangle from Adjacent Sides


### Hard

- **S16_H1** — Alignment Matrix of Marked Points

- **S16_H2** — Crop the Odd Pair by Orientation-Length Signature

- **S16_H3** — Fill the Diamond from Cardinal Markers

- **S16_H4** — Reconstruct the Silhouette from Row Endpoints

- **S16_H5** — Majority Orientation Across Panels

- **S16_H6** — Crop the Object Between Parallel Spans

- **S16_H7** — Sort Span Lengths into Ranking Bars



# Easy


## S16_E1 — Connect the Two Markers
**Skills:** straight-line completion, alignment detection, horizontal/vertical/diagonal generalization

**Primitive note:** This is the base case for span_cells: once the markers are aligned, the answer is exactly the span joining them.

**Scaffold:**

- Find the only two nonzero cells.
- Check how they are aligned.
- Draw the full segment between them and recolor it to 8.

**Train 1 input**

```text
00000000
02000200
00000000
00000000
00000000
00000000
00000000
00000000
```
**Train 1 output**

```text
00000000
08888800
00000000
00000000
00000000
00000000
00000000
00000000
```
**Train 2 input**

```text
000000000
000000000
000000200
000000000
000000000
000000000
000000200
000000000
000000000
```
**Train 2 output**

```text
000000000
000000000
000000800
000000800
000000800
000000800
000000800
000000000
000000000
```
**Test input**

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
**Expected test output**

```text
00000000
08000000
00800000
00080000
00008000
00000800
00000000
00000000
```
**Written solution**

Ignore the marker color and location details. The whole job is to connect the two aligned markers with one straight horizontal, vertical, or diagonal segment. Put that segment on a blank grid and recolor it to 8.

**Reference program**

```python
def solve_S16_E1(grid):
    return connect_single_pair(grid)
```

## S16_E2 — Draw Only the Interior of the Segment
**Skills:** segment interior, endpoint exclusion, alignment reasoning

**Primitive note:** span_cells gives the full segment; this task asks for the same primitive but with the endpoints removed.

**Scaffold:**

- Find the two aligned markers.
- Enumerate the cells on the segment between them.
- Drop the endpoints and keep only the interior cells.

**Train 1 input**

```text
00000000
00000000
03000030
00000000
00000000
00000000
00000000
00000000
```
**Train 1 output**

```text
00000000
00000000
00888800
00000000
00000000
00000000
00000000
00000000
```
**Train 2 input**

```text
000000000
000030000
000000000
000000000
000000000
000000000
000000000
000030000
000000000
```
**Train 2 output**

```text
000000000
000000000
000080000
000080000
000080000
000080000
000080000
000000000
000000000
```
**Test input**

```text
00000000
00000030
00000000
00000000
00000000
00300000
00000000
00000000
```
**Expected test output**

```text
00000000
00000000
00000800
00008000
00080000
00000000
00000000
00000000
```
**Written solution**

First find the segment between the two markers. Then throw away the two endpoint cells and keep everything strictly between them. The output is blank except for those interior cells, recolored to 8.

**Reference program**

```python
def solve_S16_E2(grid):
    return segment_interior_only(grid)
```

## S16_E3 — Mark the Segment Midpoint
**Skills:** odd-length spans, midpoint extraction, geometric reduction

**Primitive note:** The primitive supplies the ordered cells on the segment, which makes midpoint selection trivial.

**Scaffold:**

- Find the straight segment joining the two markers.
- Count how many cells it contains.
- Because the length is odd, one exact middle cell exists; output only that cell.

**Train 1 input**

```text
000000000
000000000
000000000
040000040
000000000
000000000
000000000
```
**Train 1 output**

```text
000000000
000000000
000000000
000080000
000000000
000000000
000000000
```
**Train 2 input**

```text
000000000
040000000
000000000
000000000
000000000
000000000
000000000
000000040
000000000
```
**Train 2 output**

```text
000000000
000000000
000000000
000000000
000080000
000000000
000000000
000000000
000000000
```
**Test input**

```text
000000000
000000040
000000000
000000000
000000000
000000000
000000000
040000000
000000000
```
**Expected test output**

```text
000000000
000000000
000000000
000000000
000080000
000000000
000000000
000000000
000000000
```
**Written solution**

Join the two markers into one ordered span. The training cases are chosen so the span always has an odd number of cells, so there is one exact center. Output only that center cell as 8.

**Reference program**

```python
def solve_S16_E3(grid):
    return segment_midpoint(grid)
```

## S16_E4 — Rectangle Border from Corner Markers
**Skills:** bounding-box inference, edge synthesis, rectangle geometry

**Primitive note:** Each edge of the rectangle is itself a span between two corner markers.

**Scaffold:**

- Use the four markers as rectangle corners.
- Recover the top, bottom, left, and right edges.
- Draw only the border.

**Train 1 input**

```text
0000000000
0010000100
0000000000
0000000000
0000000000
0010000100
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0088888800
0080000800
0080000800
0080000800
0088888800
0000000000
0000000000
```
**Train 2 input**

```text
000000000
000000000
010001000
000000000
000000000
000000000
000000000
010001000
000000000
```
**Train 2 output**

```text
000000000
000000000
088888000
080008000
080008000
080008000
080008000
088888000
000000000
```
**Test input**

```text
000000000000
000000000000
000000000000
000100000100
000000000000
000000000000
000000000000
000000000000
000100000100
000000000000
```
**Expected test output**

```text
000000000000
000000000000
000000000000
000888888800
000800000800
000800000800
000800000800
000800000800
000888888800
000000000000
```
**Written solution**

The four nonzero cells are the rectangle corners. Take the axis-aligned box they define and draw its four edges. The output is blank except for that border, recolored to 8.

**Reference program**

```python
def solve_S16_E4(grid):
    return rectangle_border_from_corners(grid)
```

## S16_E5 — Output Only the Span Intersection
**Skills:** two-line interaction, intersection detection, cross reasoning

**Primitive note:** span_cells is used twice, then reduced to the set intersection of the two spans.

**Scaffold:**

- Build the horizontal or diagonal span for one pair and the vertical or horizontal span for the other.
- Find where the two spans overlap.
- Output only the overlap cell.

**Train 1 input**

```text
000000000
000030000
000000000
000000000
020000020
000000000
000000000
000030000
000000000
```
**Train 1 output**

```text
000000000
000000000
000000000
000000000
000080000
000000000
000000000
000000000
000000000
```
**Train 2 input**

```text
0000000000
0000030000
0020000020
0000000000
0000000000
0000000000
0000030000
0000000000
```
**Train 2 output**

```text
0000000000
0000000000
0000080000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Test input**

```text
0000000000
0000000000
0000300000
0000000000
0000000000
0000000000
0200000020
0000000000
0000000000
0000300000
```
**Expected test output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000800000
0000000000
0000000000
0000000000
```
**Written solution**

There are two marker pairs, and each pair defines one straight segment. Do not draw the whole cross. Instead, compute both segments and keep only the single cell where they meet. That one cell becomes 8.

**Reference program**

```python
def solve_S16_E5(grid):
    return span_intersection_only(grid)
```

## S16_E6 — Longest Pair Wins
**Skills:** length comparison, multi-pair selection, connector choice

**Primitive note:** The new primitive gives both the cells and the length of each candidate segment.

**Scaffold:**

- Compute the span for every marker pair.
- Measure each span length.
- Keep only the longest one and recolor it to 8.

**Train 1 input**

```text
0000000000
0101000000
0030000000
0000000200
0000000000
0000000000
0000000000
0000000200
0000000030
0000000000
```
**Train 1 output**

```text
0000000000
0000000000
0080000000
0008000000
0000800000
0000080000
0000008000
0000000800
0000000080
0000000000
```
**Train 2 input**

```text
00000000000
03000000100
02000200000
00000000000
00000000000
00000000100
00000000000
00000003000
00000000000
```
**Train 2 output**

```text
00000000000
08000000000
00800000000
00080000000
00008000000
00000800000
00000080000
00000008000
00000000000
```
**Test input**

```text
0000000000
0200200000
0000000100
0000000030
0000000000
0000000000
0000000000
0000000000
0100000030
0000000000
```
**Expected test output**

```text
0000000000
0000000000
0000000800
0000008000
0000080000
0000800000
0008000000
0080000000
0800000000
0000000000
```
**Written solution**

Several colored marker pairs are present, but only one output survives. Connect every valid pair conceptually, compare the segment lengths, and keep the longest segment only. Recolor that winning segment to 8.

**Reference program**

```python
def solve_S16_E6(grid):
    return longest_pair_wins(grid)
```

## S16_E7 — Turn the Segment Length into a Bar
**Skills:** counting from geometry, symbolic output, length abstraction

**Primitive note:** span_cells turns a geometric object into an exact integer length, which is then re-encoded as a bar.

**Scaffold:**

- Find the segment joining the markers.
- Count its cells, including endpoints.
- Produce a 1×L bar of 8s where L is that length.

**Train 1 input**

```text
00000000
00000000
02000200
00000000
00000000
00000000
```
**Train 1 output**

```text
88888
```
**Train 2 input**

```text
00000000
00000020
00000000
00000000
00000000
00200000
00000000
00000000
```
**Train 2 output**

```text
88888
```
**Test input**

```text
000000000
000020000
000000000
000000000
000000000
000000000
000000000
000020000
000000000
```
**Expected test output**

```text
8888888
```
**Written solution**

The segment itself is not redrawn in place. Instead, measure how many cells long it is and convert that number into a one-row bar. The output width equals the segment length, and every cell in that bar is 8.

**Reference program**

```python
def solve_S16_E7(grid):
    return length_bar_from_pair(grid)
```

# Medium


## S16_M1 — Legend Chooses Which Pair to Connect
**Skills:** legend decoding, orientation routing, selective connector drawing

**Primitive note:** The primitive is the same span construction, but the interesting step is routing to the correct pair via a legend.

**Scaffold:**

- Read the legend marker in the top-left corner.
- Map it to one of the candidate pair colors.
- Connect only that chosen pair and ignore the others.

**Train 1 input**

```text
500000000000
000000000030
002000020000
000000000000
000000000000
040000000000
000000000030
000000000000
000040000000
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
008888880000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 input**

```text
60000000000
00000000003
00200002000
00000000000
00000000000
04000000000
00000000003
00000000000
00004000000
```
**Train 2 output**

```text
00000000000
00000000008
00000000008
00000000008
00000000008
00000000008
00000000008
00000000000
00000000000
```
**Test input**

```text
70000000000
00000000003
00200002000
00000000000
00000000000
04000000000
00000000003
00000000000
00004000000
00000000000
```
**Expected test output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
08000000000
00800000000
00080000000
00008000000
00000000000
```
**Written solution**

Three candidate pairs are present at once. The top-left legend cell tells you which pair matters. Decode the legend, select the corresponding pair, build its segment, and output only that segment in 8.

**Reference program**

```python
def solve_S16_M1(grid):
    return legend_chooses_orientation(grid)
```

## S16_M2 — Draw the Full Cross from Two Pairs
**Skills:** union of segments, cross synthesis, compositional drawing

**Primitive note:** Two separate uses of span_cells compose into one larger object.

**Scaffold:**

- Build one span from the horizontal pair and one from the vertical pair.
- Take their union.
- Recolor the whole combined cross to 8.

**Train 1 input**

```text
000000000
000030000
000000000
000000000
020000020
000000000
000000000
000030000
000000000
```
**Train 1 output**

```text
000000000
000080000
000080000
000080000
088888880
000080000
000080000
000080000
000000000
```
**Train 2 input**

```text
0000000000
0000000000
0000030000
0000000000
0000000000
0000000000
0020000020
0000000000
0000000000
0000030000
```
**Train 2 output**

```text
0000000000
0000000000
0000080000
0000080000
0000080000
0000080000
0088888880
0000080000
0000080000
0000080000
```
**Test input**

```text
00000000000
00000030000
00000000000
00000000000
00000000000
02000000020
00000000000
00000000000
00000000000
00000030000
00000000000
```
**Expected test output**

```text
00000000000
00000080000
00000080000
00000080000
00000080000
08888888880
00000080000
00000080000
00000080000
00000080000
00000000000
```
**Written solution**

Each pair defines one arm-set of the cross. Compute both spans and overlay them. The output is the full union of those two segments, recolored to 8.

**Reference program**

```python
def solve_S16_M2(grid):
    return full_cross_from_pairs(grid)
```

## S16_M3 — Fill the Rectangle from Opposite Corners
**Skills:** opposite-corner reasoning, rectangle fill, size-changing output

**Primitive note:** The corner relation can be understood as spans across rows and columns, then expanded into a full filled region.

**Scaffold:**

- Read the two marked opposite corners.
- Recover the axis-aligned rectangle they define.
- Fill the entire rectangle, not just the border.

**Train 1 input**

```text
000000000
001000000
000000000
000000000
000000000
000000100
000000000
000000000
```
**Train 1 output**

```text
88888
88888
88888
88888
88888
```
**Train 2 input**

```text
0000000000
0000000000
0000010000
0000000000
0000000000
0000000000
0000000000
0100000000
0000000000
0000000000
```
**Train 2 output**

```text
88888
88888
88888
88888
88888
88888
```
**Test input**

```text
000000000000
000000001000
000000000000
000000000000
000000000000
000000000000
000100000000
000000000000
000000000000
```
**Expected test output**

```text
888888
888888
888888
888888
888888
888888
```
**Written solution**

The two markers are opposite corners of an axis-aligned rectangle. Take the min and max row and column coordinates, and fill every cell inside that box. The output is just that filled rectangle in 8.

**Reference program**

```python
def solve_S16_M3(grid):
    return filled_rectangle_from_opposite_corners(grid)
```

## S16_M4 — Draw Every Pair in Its Own Color
**Skills:** parallel independent rules, multicolor output, connector overlay

**Primitive note:** span_cells stays local to each color class, then the colored results are overlaid.

**Scaffold:**

- Group the markers by color.
- For each color, connect its two markers.
- Keep the original color of each resulting segment.

**Train 1 input**

```text
0000000000
0200020000
0000000030
0000000000
0000000000
0000040000
0000000030
0000000000
0040000000
0000000000
```
**Train 1 output**

```text
0000000000
0222220000
0000000030
0000000030
0000000030
0000040030
0000400030
0004000000
0040000000
0000000000
```
**Train 2 input**

```text
000000000000
000000000030
000000000000
020000020000
000004000000
000000000000
000000000030
004000000000
000000000000
```
**Train 2 output**

```text
000000000000
000000000030
000000000030
022222220030
000004000030
000040000030
000400000030
004000000000
000000000000
```
**Test input**

```text
0000000000
0000000030
0040040000
0000002000
0000000000
0000000000
0000000030
0000000000
0200000000
0000000000
```
**Expected test output**

```text
0000000000
0000000030
0044440030
0000002030
0000020030
0000200030
0002000030
0020000000
0200000000
0000000000
```
**Written solution**

Instead of choosing one pair, solve all of them. Each color appears exactly twice, so each color defines one segment. Draw every segment on a blank grid, keeping each segment in its own original color.

**Reference program**

```python
def solve_S16_M4(grid):
    return draw_every_pair_in_own_color(grid)
```

## S16_M5 — Crop the Object Hit by the Connector
**Skills:** line-object interaction, component selection, cropping

**Primitive note:** The span is not the output; it is the probe used to select the correct component.

**Scaffold:**

- Construct the connector line from the marker pair.
- Check which object component intersects that line.
- Crop that one object tightly and recolor it to 8.

**Train 1 input**

```text
000000000000
000002200000
010002200010
000000000000
000000000000
030000000000
030000004400
033000000440
000000000000
000000000000
```
**Train 1 output**

```text
88
88
```
**Train 2 input**

```text
00000000000
01000000000
00000000000
00003000000
00033300000
02203000000
02200000000
00000001400
00000000400
00000000440
00000000000
```
**Train 2 output**

```text
080
888
080
```
**Test input**

```text
0000000000
0030001000
0333000000
0030000000
0000022200
0000022200
0000000000
0440001000
0044000000
0000000000
```
**Expected test output**

```text
888
888
```
**Written solution**

First build the connector defined by the marker pair. Then test which colored object is touched by that connector. Ignore the others, crop the touched object to its tight bounding box, and recolor the cropped shape to 8.

**Reference program**

```python
def solve_S16_M5(grid):
    return crop_object_hit_by_connector(grid)
```

## S16_M6 — Fill the Band Between Parallel Pairs
**Skills:** parallelism, region filling, pair-to-band abstraction

**Primitive note:** The primitive identifies each boundary span; the task then upgrades two spans into a filled band.

**Scaffold:**

- Find the two parallel marker pairs.
- Treat them as opposite sides of a band.
- Fill every cell between them.

**Train 1 input**

```text
00000000000
00000000000
00200002000
00000000000
00000000000
00000000000
00300003000
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00000000000
00888888000
00888888000
00888888000
00888888000
00888888000
00000000000
00000000000
```
**Train 2 input**

```text
0000000000
0000000000
0002003000
0000000000
0000000000
0000000000
0000000000
0002003000
0000000000
0000000000
```
**Train 2 output**

```text
0000000000
0000000000
0008888000
0008888000
0008888000
0008888000
0008888000
0008888000
0000000000
0000000000
```
**Test input**

```text
000000000000
000020000200
000000000000
000000000000
000000000000
000030000300
000000000000
000000000000
000000000000
000000000000
```
**Expected test output**

```text
000000000000
000088888800
000088888800
000088888800
000088888800
000088888800
000000000000
000000000000
000000000000
000000000000
```
**Written solution**

Two parallel pairs define two matching boundary segments. The solution is the full axis-aligned band between them, including the boundary rows or columns. Fill that whole band with 8.

**Reference program**

```python
def solve_S16_M6(grid):
    return fill_band_between_parallel_pairs(grid)
```

## S16_M7 — Complete the Rectangle from Adjacent Sides
**Skills:** shared-corner reasoning, width-height transfer, rectangle completion

**Primitive note:** Two short spans sharing a corner imply the full rectangle once width and height are known.

**Scaffold:**

- Use the shared corner marker as the anchor.
- Use one extra marker to get the width and the other to get the height.
- Complete the missing two sides of the rectangle.

**Train 1 input**

```text
0000000000
0000000000
0010000200
0000000000
0000000000
0000000000
0030000000
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0000000000
0088888800
0080000800
0080000800
0080000800
0088888800
0000000000
0000000000
```
**Train 2 input**

```text
00000000000
00000000000
00000000300
00000000000
00000000000
00000000000
00000000000
00020000100
00000000000
00000000000
```
**Train 2 output**

```text
00000000000
00000000000
00088888800
00080000800
00080000800
00080000800
00080000800
00088888800
00000000000
00000000000
```
**Test input**

```text
000000000000
000000000000
000020000100
000000000000
000000000000
000000000000
000000000000
000000000300
000000000000
000000000000
```
**Expected test output**

```text
000000000000
000000000000
000088888800
000080000800
000080000800
000080000800
000080000800
000088888800
000000000000
000000000000
```
**Written solution**

One marker is the shared corner. Another marker fixes the horizontal reach, and the third fixes the vertical reach. Combine those two side lengths to reconstruct the whole rectangle border and recolor it to 8.

**Reference program**

```python
def solve_S16_M7(grid):
    return complete_rectangle_from_adjacent_sides(grid)
```

# Hard


## S16_H1 — Alignment Matrix of Marked Points
**Skills:** symbolic pairwise reasoning, matrix construction, alignment predicates

**Primitive note:** span_cells is not drawn directly here; instead, its alignment predicate becomes symbolic matrix structure.

**Scaffold:**

- Order the points by color.
- For every ordered pair of points, test whether they are row-aligned, column-aligned, or diagonal-aligned.
- Write that truth table as a square matrix.

**Train 1 input**

```text
000000000
010002000
000000000
000000000
000003000
000000000
000400000
000000000
000000000
```
**Train 1 output**

```text
8800
8880
0888
0088
```
**Train 2 input**

```text
0000000000
0000000000
0040000100
0000000000
0000000000
0000000200
0000000000
0000000000
0000300000
0000000000
```
**Train 2 output**

```text
8808
8880
0880
8008
```
**Test input**

```text
00000000000
00000400010
00000000000
00000000000
00000000000
00000200030
00000000000
00000000000
00000000000
```
**Expected test output**

```text
8888
8888
8888
8888
```
**Written solution**

The colored points act like labeled nodes. Sort them by label color, then compare every point to every other point. If a pair lies on one horizontal, vertical, or 45° diagonal line, mark the matrix entry with 8; otherwise use 0. Self-pairs are marked too.

**Reference program**

```python
def solve_S16_H1(grid):
    return alignment_matrix_of_marked_points(grid)
```

## S16_H2 — Crop the Odd Pair by Orientation-Length Signature
**Skills:** signature extraction, odd-one-out selection, normalized output

**Primitive note:** The primitive supplies exactly the two features that matter here: orientation class and segment length.

**Scaffold:**

- Build the span for every pair.
- Represent each pair by its orientation and length.
- Find the unique signature, then crop that winning span tightly.

**Train 1 input**

```text
000000000000
020002000000
000000000400
000000000000
003000300000
000000000000
000000000400
000000000000
000000000000
000000000000
```
**Train 1 output**

```text
8
8
8
8
8
```
**Train 2 input**

```text
00000000000
02000030000
04000000000
00000000000
00002000030
00000000000
00000000000
00000040000
00000000000
00000000000
```
**Train 2 output**

```text
800000
080000
008000
000800
000080
000008
```
**Test input**

```text
00000000000
00000000040
02000002000
00000000000
00000000000
03000003000
00000000000
00000000040
00000000000
00000000000
00000000000
```
**Expected test output**

```text
8
8
8
8
8
8
8
```
**Written solution**

Each pair becomes a signature: horizontal/vertical/diagonal plus its segment length. Two pairs share a signature and one does not. Find the odd signature and output that pair's span as a tightly cropped 8-shape.

**Reference program**

```python
def solve_S16_H2(grid):
    return odd_pair_crop_by_signature(grid)
```

## S16_H3 — Fill the Diamond from Cardinal Markers
**Skills:** diamond geometry, center-radius inference, Manhattan distance

**Primitive note:** Each diamond edge is a diagonal span; the full region is the filled shape bounded by those spans.

**Scaffold:**

- Identify the north, south, west, and east markers.
- Recover the diamond center and radius.
- Fill every cell inside that diamond.

**Train 1 input**

```text
000000000
000010000
000000000
000000000
010000010
000000000
000000000
000010000
000000000
```
**Train 1 output**

```text
000000000
000080000
000888000
008888800
088888880
008888800
000888000
000080000
000000000
```
**Train 2 input**

```text
00000000000
00000000000
00000100000
00000000000
00000000000
00100000100
00000000000
00000000000
00000100000
00000000000
00000000000
```
**Train 2 output**

```text
00000000000
00000000000
00000800000
00008880000
00088888000
00888888800
00088888000
00008880000
00000800000
00000000000
00000000000
```
**Test input**

```text
0000000000000
0000000000000
0000001000000
0000000000000
0000000000000
0000000000000
0010000000100
0000000000000
0000000000000
0000000000000
0000001000000
0000000000000
0000000000000
```
**Expected test output**

```text
0000000000000
0000000000000
0000008000000
0000088800000
0000888880000
0008888888000
0088888888800
0008888888000
0000888880000
0000088800000
0000008000000
0000000000000
0000000000000
```
**Written solution**

The four markers are the cardinal extreme points of a diamond. Compute the center from opposite markers, read the radius, and fill all cells whose Manhattan distance from the center is at most that radius. Recolor the whole diamond to 8.

**Reference program**

```python
def solve_S16_H3(grid):
    return fill_diamond_from_cardinal_markers(grid)
```

## S16_H4 — Reconstruct the Silhouette from Row Endpoints
**Skills:** row-wise spans, shape reconstruction, many-local-rules aggregation

**Primitive note:** This is repeated use of span_cells across many rows to rebuild a larger silhouette.

**Scaffold:**

- Treat each nonempty row independently.
- Use the two markers in that row as left and right endpoints.
- Fill the full row segment between them and combine the rows.

**Train 1 input**

```text
00000000000
00001010000
00010001000
00100000100
00010001000
00001010000
00000000000
00000000000
00000000000
```
**Train 1 output**

```text
00000000000
00008880000
00088888000
00888888800
00088888000
00008880000
00000000000
00000000000
00000000000
```
**Train 2 input**

```text
000000000000
010010000000
010001000000
001000100000
000100010000
000100010000
001000100000
010001000000
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
088880000000
088888000000
008888800000
000888880000
000888880000
008888800000
088888000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000000000000
0000010100000
0000100010000
0001000001000
0010000000100
0001000001000
0000100010000
0000010100000
0000000000000
0000000000000
```
**Expected test output**

```text
0000000000000
0000000000000
0000088800000
0000888880000
0008888888000
0088888888800
0008888888000
0000888880000
0000088800000
0000000000000
0000000000000
```
**Written solution**

Every informative row contains exactly two endpoints. Fill the cells between them on that row, then do the same for all rows and combine the results. The output is the reconstructed silhouette in 8.

**Reference program**

```python
def solve_S16_H4(grid):
    return row_endpoint_silhouette_fill(grid)
```

## S16_H5 — Majority Orientation Across Panels
**Skills:** panel parsing, majority vote, normalized geometric output

**Primitive note:** The primitive is used inside each panel; the hard part is aggregating those local span orientations globally.

**Scaffold:**

- Split the input into panels using the separator columns.
- Read the orientation of the pair inside each panel.
- Find the majority orientation and output a normalized span with that orientation.

**Train 1 input**

```text
00000900100900000
00000900000910001
10001900000900000
00000900000900000
00000900100900000
```
**Train 1 output**

```text
88888
```
**Train 2 input**

```text
10000900001900100
00000900000900000
00000900000900000
00000900000900000
00001910000900100
```
**Train 2 output**

```text
80000
08000
00800
00080
00008
```
**Test input**

```text
00100900000900100
00000900000900000
00000910001900000
00000900000900000
00100900000900100
```
**Expected test output**

```text
8
8
8
8
8
```
**Written solution**

Read each panel separately. Each panel contains one pair, which gives one orientation class. Take the majority orientation across panels, choose the longest span among panels with that majority, and output that span in normalized cropped form as 8s.

**Reference program**

```python
def solve_S16_H5(grid):
    return majority_orientation_panels(grid)
```

## S16_H6 — Crop the Object Between Parallel Spans
**Skills:** region selection, band reasoning, component filtering

**Primitive note:** Again the spans are probes rather than outputs: they define the geometric filter used to select the target component.

**Scaffold:**

- Use the two parallel marker pairs to define a band.
- Check which object lies fully inside that band.
- Crop that object tightly and recolor it to 8.

**Train 1 input**

```text
0000000000000
0000000000400
0010000001400
0000000000440
0000033000000
0000033000000
0000000000000
0020000002000
0050000000000
0555000000000
0050000000000
```
**Train 1 output**

```text
88
88
```
**Train 2 input**

```text
000000000000
000000000440
000100002440
000000000000
000000000000
000000300000
000003330000
000000300000
500000000000
500100002000
550000000000
000000000000
```
**Train 2 output**

```text
080
888
080
```
**Test input**

```text
44000000000000
44001000000100
00000000000000
00000003300000
00000000330000
00000000000000
00002000000200
00000000055500
00000000055500
00000000000000
```
**Expected test output**

```text
880
088
```
**Written solution**

The marker pairs define a horizontal or vertical band. Ignore objects that stick out of that band. Find the unique object completely contained inside, crop it to its tight box, and recolor the cropped shape to 8.

**Reference program**

```python
def solve_S16_H6(grid):
    return crop_object_between_parallel_spans(grid)
```

## S16_H7 — Sort Span Lengths into Ranking Bars
**Skills:** measurement, sorting, symbolic re-encoding

**Primitive note:** The primitive turns geometry into sortable numbers, then the output re-encodes those numbers symbolically.

**Scaffold:**

- Measure the length of each pair's span.
- Sort those lengths from shortest to longest.
- Emit one horizontal 8-bar per length in sorted order.

**Train 1 input**

```text
0000000000
0101000000
0000000000
0000000000
0200002000
0000000000
0000000000
0300000300
0000000000
0000000000
```
**Train 1 output**

```text
8880000
8888880
8888888
```
**Train 2 input**

```text
00000000000
00000000100
02020000000
00000030000
00000000000
00000000100
00000000000
00000000000
03000000000
00000000000
00000000000
```
**Train 2 output**

```text
888000
888880
888888
```
**Test input**

```text
000000000000
010001000000
000000300000
000000000020
000000000000
000000000000
000000000000
030000000000
000000000020
000000000000
```
**Expected test output**

```text
888880
888888
888888
```
**Written solution**

Do not redraw the original segments. Instead, measure their lengths, sort those lengths, and create a bar chart made of 8s: one row per segment length, from shortest row to longest row.

**Reference program**

```python
def solve_S16_H7(grid):
    return length_ranking_bars(grid)
```