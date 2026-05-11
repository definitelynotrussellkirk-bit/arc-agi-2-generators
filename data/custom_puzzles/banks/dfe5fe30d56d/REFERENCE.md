# ARC-style Puzzle Bank: 21 More Tasks (Tenth Batch)

This tenth batch deliberately pushes into a different slice of the ARC design space:
run rewrites, profile extraction, symmetry classification, legend-driven recoloring,
marker docking, waypoint routing, majority overlays, keyed transforms, and structured galleries.

## New helper primitives highlighted in this batch

- `anchor_polyline` — Connect ordered object anchors with orthogonal polylines.
- `bbox_frame` — Replace an object by the rectangular frame of its tight bounding box.
- `diamond_bloom` — Expand a singleton seed into its full Manhattan-distance-2 diamond.
- `dual_key_transform` — One key selects an object and the other key selects a transform.
- `frame_rotate_insert` — Rotate an external insert object according to a key and place it into its matching frame.
- `marker_dock` — Dock each colored object under its matching marker column.
- `palette_legend` — Read adjacent old→new color pairs from a legend row.
- `perimeter_rank` — Rank connected objects by perimeter and map the ranks to output colors.
- `plus_vote_fill` — Fill a center cell when all four orthogonal neighbors agree.
- `row_flush_right` — Slide each row’s nonzero cells to the right edge, preserving order.
- `row_profile` — Convert a cropped object into a row-count histogram.
- `run_dash` — Keep every other cell of each horizontal run.
- `run_grow` — Extend each horizontal run by one cell at both ends.
- `run_median` — Collapse each odd horizontal run to its middle cell.
- `stack_by_height` — Crop objects and stack them from tallest to shortest.
- `symmetry_class` — Classify objects by vertical and horizontal mirror symmetry.
- `symmetry_table` — Pack objects into a 2×2 gallery based on symmetry class.
- `threeway_majority` — Keep cells occupied by at least two of three normalized shapes.
- `transform_timeline` — Apply a script of transforms and emit every intermediate stage.
- `waypoint_path` — Route a shortest orthogonal path that must pass through a waypoint.
- `zebra_bridge` — Fill every other cell between matched row endpoints.

## Index

- 1. `easy_j01` — Expand singleton seeds into radius-2 diamonds
- 2. `easy_j02` — Keep only the middle cell of each odd horizontal run
- 3. `easy_j03` — Fill alternating cells between matched row endpoints
- 4. `easy_j04` — Fill the missing center of each plus
- 5. `easy_j05` — Grow each horizontal run by one cell at both ends
- 6. `easy_j06` — Dash each horizontal run
- 7. `easy_j07` — Flush each row to the right
- 8. `medium_j08` — Recolor objects by perimeter rank
- 9. `medium_j09` — Replace each object with its bounding-box frame
- 10. `medium_j10` — Convert the object into a row-profile chart
- 11. `medium_j11` — Recolor objects by symmetry class
- 12. `medium_j12` — Stack cropped objects vertically by height
- 13. `medium_j13` — Dock each object under its matching top-row marker
- 14. `medium_j14` — Apply the top-row color legend
- 15. `hard_j15` — Route a waypoint path through the maze
- 16. `hard_j16` — Take the majority overlay of three normalized shapes
- 17. `hard_j17` — Rotate inserts into matching-color frames
- 18. `hard_j18` — Connect object anchors in x-order
- 19. `hard_j19` — Use two keys to select and transform an object
- 20. `hard_j20` — Build a transformation timeline gallery
- 21. `hard_j21` — Pack one object from each symmetry class into a 2x2 table

## 1. `easy_j01` — Expand singleton seeds into radius-2 diamonds
**Difficulty:** easy

**Tags:** same_size, local, manhattan, seeds

**Written rule:** Every nonzero singleton seed expands into the full Manhattan-distance-2 diamond of the same color.

**Program function:** `solve_j01_diamond_bloom`

**Primitive names:** `diamond_bloom`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
2 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 3 3 3 3 3
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 4 4 4 4 4
0 0 6 0 0 0 4 4 4 0
0 6 6 6 0 0 0 4 0 0
6 6 6 6 6 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 8 0 0
0 0 7 7 7 0 8 8 8 0
0 7 7 7 7 8 8 8 8 8
0 0 7 7 7 0 8 8 8 0
0 0 0 7 0 2 0 8 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 2 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 9 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 0 9 9 9 0 0 0 0 0
0 0 0 0 9 0 0 0 5 0 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 0
```

---

## 2. `easy_j02` — Keep only the middle cell of each odd horizontal run
**Difficulty:** easy

**Tags:** same_size, runs, rows, selection

**Written rule:** Each odd-length horizontal run collapses to just its middle cell. Background stays black(0).

**Program function:** `solve_j02_run_median`

**Primitive names:** `run_median`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0
0 0 0 0 0 0 0 0
0 6 6 6 0 7 7 7
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 0 0 7 0
```

**Train 2 — input**

```text
0 3 3 3 3 3 0
0 0 0 0 0 0 0
5 5 5 0 0 8 8
0 0 0 0 0 0 0
0 0 9 9 9 0 0
```

**Train 2 — output**

```text
0 0 0 3 0 0 0
0 0 0 0 0 0 0
0 5 0 0 0 0 8
0 0 0 0 0 0 0
0 0 0 9 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 5 5 5 0 0
0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 0 0 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
```

---

## 3. `easy_j03` — Fill alternating cells between matched row endpoints
**Difficulty:** easy

**Tags:** same_size, rows, bridges, alternation

**Written rule:** When a row has exactly two equal nonzero endpoints with only black(0) cells between them, fill every other interior cell starting from the left endpoint side.

**Program function:** `solve_j03_zebra_bridge`

**Primitive names:** `zebra_bridge`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 2 0 0 0 2 0
0 0 0 0 0 0 0
0 0 4 0 0 0 4
0 0 0 0 0 0 0
7 0 0 0 0 0 7
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 2 2 0 2 2 0
0 0 0 0 0 0 0
0 0 4 4 0 4 4
0 0 0 0 0 0 0
7 7 0 7 0 7 7
```

**Train 2 — input**

```text
0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0
0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0
```

**Train 2 — output**

```text
0 3 3 0 3 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 0
0 0 0 0 0 0 0 0
8 8 0 8 8 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0
0 6 6 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 0 2 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0
0 4 4 0 4 4 0 0
0 0 0 0 0 0 0 0
0 0 7 7 0 7 7 0
```

---

## 4. `easy_j04` — Fill the missing center of each plus
**Difficulty:** easy

**Tags:** same_size, local, plus, completion

**Written rule:** If a black(0) cell has four orthogonal neighbors of the same nonzero color, fill the center with that color.

**Program function:** `solve_j04_plus_vote_fill`

**Primitive names:** `plus_vote_fill`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 0 2 0 0 4 0
0 2 0 2 4 0 4
0 0 2 0 0 4 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 0 2 0 0 4 0
0 2 2 2 4 4 4
0 0 2 0 0 4 0
0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0
0 3 0 0 0 0
3 0 3 0 5 0
0 3 0 5 0 5
0 0 0 0 5 0
0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0
0 3 0 0 0 0
3 3 3 0 5 0
0 3 0 5 5 5
0 0 0 0 5 0
0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0
0 6 0 0 0 0 8 0
6 0 6 0 0 8 0 8
0 6 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0
0 6 0 0 0 0 8 0
6 6 6 0 0 8 8 8
0 6 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0
0 9 0 0 7 0
9 0 9 7 0 7
0 9 0 0 7 0
0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0
0 9 0 0 7 0
9 9 9 7 7 7
0 9 0 0 7 0
0 0 0 0 0 0
```

---

## 5. `easy_j05` — Grow each horizontal run by one cell at both ends
**Difficulty:** easy

**Tags:** same_size, runs, growth, rows

**Written rule:** Extend every horizontal run of a nonzero color by one extra cell on the left and one on the right whenever those cells are black(0).

**Program function:** `solve_j05_run_grow`

**Primitive names:** `run_grow`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0
7 7 7 7 7 7 0 0
```

**Train 2 — input**

```text
0 0 3 3 0 0 0
0 0 0 0 0 0 0
0 6 6 6 0 9 9
0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 3 3 3 3 0 0
0 0 0 0 0 0 0
6 6 6 6 9 9 9
0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0
4 4 4 4 0 8 8 8 8
0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0
0 2 2 2 0 5 5
0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0
2 2 2 2 5 5 5
0 0 0 0 0 0 0
```

---

## 6. `easy_j06` — Dash each horizontal run
**Difficulty:** easy

**Tags:** same_size, runs, rows, subsampling

**Written rule:** Replace each horizontal run by a dashed version that keeps every other cell, starting from the run’s leftmost cell.

**Program function:** `solve_j06_run_dash`

**Primitive names:** `run_dash`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 5 5 5 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 2 0 2 0 2 0
0 0 0 0 0 0 0
0 0 5 0 5 0 0
```

**Train 2 — input**

```text
0 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0
```

**Train 2 — output**

```text
0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 7 0 7 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0
4 4 4 4 0 9 9
0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0
4 0 4 0 0 9 0
0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0
0 6 6 6 6 0
0 0 0 0 0 0
8 8 8 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0
0 6 0 6 0 0
0 0 0 0 0 0
8 0 8 0 0 0
```

---

## 7. `easy_j07` — Flush each row to the right
**Difficulty:** easy

**Tags:** same_size, rows, packing, order_preserving

**Written rule:** Within each row, keep the nonzero cells in their original left-to-right order but slide them all the way to the right edge.

**Program function:** `solve_j07_row_flush_right`

**Primitive names:** `row_flush_right`


### Train examples

**Train 1 — input**

```text
0 2 0 3 0 0 0
4 0 0 5 6 0 0
0 0 0 0 0 0 0
7 0 8 0 0 9 0
```

**Train 1 — output**

```text
0 0 0 0 0 2 3
0 0 0 0 4 5 6
0 0 0 0 0 0 0
0 0 0 0 7 8 9
```

**Train 2 — input**

```text
0 0 1 0 2 0
3 0 0 0 0 4
0 5 0 6 0 0
```

**Train 2 — output**

```text
0 0 0 0 1 2
0 0 0 0 3 4
0 0 0 0 5 6
```

**Train 3 — input**

```text
0 7 0 0 0 8 9 0
0 0 0 2 0 0 0 0
4 5 0 0 6 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 7 8 9
0 0 0 0 0 0 0 2
0 0 0 0 0 4 5 6
```


### Test example

**Test 1 — input**

```text
0 2 0 3 0 0
4 0 0 5 6 0
0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 2 3
0 0 0 4 5 6
0 0 0 0 0 0
```

---

## 8. `medium_j08` — Recolor objects by perimeter rank
**Difficulty:** medium

**Tags:** same_size, objects, ranking, perimeter

**Written rule:** Measure each object’s perimeter. The largest perimeter becomes red(2), the next becomes green(3), the next yellow(4), and so on by descending rank.

**Program function:** `solve_j08_perimeter_rank`

**Primitive names:** `perimeter_rank`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 7 7 0 0
0 0 2 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 4 4 0 0
0 0 2 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 8 0 0
0 3 3 3 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 4 0 0
0 2 2 2 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 1 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 0 0
0 0 4 4 0 0 0 0 0 9 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 6 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 4 4 0 0 0 0 0 2 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 4 4 0 0 0 0 6 6 6 0 0
0 4 4 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 4 4 0 0 0 0 3 3 3 0 0
0 4 4 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 9. `medium_j09` — Replace each object with its bounding-box frame
**Difficulty:** medium

**Tags:** same_size, objects, bounding_box, frames

**Written rule:** For every connected object, ignore its internal shape and draw only the rectangular frame of its tight bounding box in the same color.

**Program function:** `solve_j09_bbox_frame`

**Primitive names:** `bbox_frame`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 10. `medium_j10` — Convert the object into a row-profile chart
**Difficulty:** medium

**Tags:** resize, object, histogram, rows

**Written rule:** Crop the object, count how many colored cells appear in each cropped row, and output a left-justified bar chart of those row counts using the object’s color.

**Program function:** `solve_j10_row_profile`

**Primitive names:** `row_profile`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 4 4 4 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 4 0
4 4 4
4 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
7 7 0 0
7 7 7 7
7 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 0 3 3 3 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
3 3 0
3 3 3
3 0 0
3 3 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 6 6 6 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
6 6 6
6 6 6
6 0 0
```

---

## 11. `medium_j11` — Recolor objects by symmetry class
**Difficulty:** medium

**Tags:** same_size, objects, symmetry, classification

**Written rule:** Classify each cropped object by its mirror symmetries: both vertical and horizontal → cyan(8), vertical only → red(2), horizontal only → green(3), neither → yellow(4). Preserve the shape positions.

**Program function:** `solve_j11_symmetry_class`

**Primitive names:** `symmetry_class`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0
0 2 2 2 0 0 0 0 4 4 4 0 0 0
0 0 2 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 7 7 0 0 0 0
0 0 5 5 0 0 0 0 0 7 7 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 2 0 0 0 0
0 8 8 8 0 0 0 0 2 2 2 0 0 0
0 0 8 0 0 0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 4 4 0 0 0 0
0 0 3 3 0 0 0 0 0 4 4 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 8 8 0 0
0 3 3 3 0 0 0 0 0 0 8 8 0
0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 4 0 0
0 2 2 2 0 0 0 0 0 0 4 4 0
0 2 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 4 0 0 0 0 7 7 7 0 0
0 4 4 4 0 0 0 7 0 7 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 8 0 0 0 0 2 2 2 0 0
0 8 8 8 0 0 0 2 0 2 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 5 0 0 0
0 3 3 3 0 0 0 0 5 5 5 0 0
0 0 3 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 9 9 0 0 0
0 0 6 6 0 0 0 0 0 9 9 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 2 0 0 0
0 8 8 8 0 0 0 0 2 2 2 0 0
0 0 8 0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 4 4 0 0 0
0 0 3 3 0 0 0 0 0 4 4 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 12. `medium_j12` — Stack cropped objects vertically by height
**Difficulty:** medium

**Tags:** resize, objects, packing, sorting

**Written rule:** Crop every object and stack the cropped shapes from tallest to shortest, with one blank row between consecutive shapes. Keep original colors.

**Program function:** `solve_j12_stack_by_height`

**Primitive names:** `stack_by_height`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 4 0 0 0
0 2 0 2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 0 0
4 0 0
4 0 0
4 0 0
0 0 0
2 2 2
2 0 2
0 0 0
7 7 0
7 7 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 8 0 0
0 0 3 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 0 0
3 3 0
3 0 0
0 0 0
0 5 0
5 5 5
0 5 0
0 0 0
8 0 0
8 0 0
8 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 2 0 0 0 0 9 0 0 0
0 0 0 2 0 0 0 0 9 0 0 0
0 0 0 2 2 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
9 0 0
9 0 0
9 0 0
9 0 0
0 0 0
2 0 0
2 0 0
2 2 0
0 0 0
6 6 6
6 6 6
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 7 7 0 0 0
0 4 4 0 0 0 0 0 7 7 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
2 0
2 0
2 0
2 0
0 0
4 0
4 4
4 0
0 0
7 7
7 7
```

---

## 13. `medium_j13` — Dock each object under its matching top-row marker
**Difficulty:** medium

**Tags:** resize, markers, objects, alignment

**Written rule:** Each nonzero cell in the top row is a dock marker. Find the object of the same color, crop it, then place it in the output so its left edge starts in that marker’s column and its bottom edge sits on the output floor.

**Program function:** `solve_j13_marker_dock`

**Primitive names:** `marker_dock`


### Train examples

**Train 1 — input**

```text
0 2 0 0 0 4 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 4 4 4 0 0 0 0 0
0 2 0 0 0 4 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 2 2 0 0 4 4 4 7 0 0 0
0 2 0 0 0 0 4 0 7 7 0 0
```

**Train 2 — input**

```text
3 0 0 0 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 5 5 0 0 0 0
0 0 0 3 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 5 5 0 0 8 0 0
3 3 3 0 0 0 5 0 0 0 8 0 0
0 3 0 0 0 0 5 0 0 0 8 0 0
```

**Train 3 — input**

```text
0 0 6 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 6 6 0 0 0 9 9 9 0
0 0 0 6 0 0 0 9 0 0 0
```


### Test example

**Test 1 — input**

```text
0 4 0 0 0 0 7 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 2 0
0 4 4 0 0 0 7 7 0 0 2 0
0 0 0 0 0 0 7 7 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 2 0 0
0 4 4 0 0 0 7 7 0 2 0 0
0 0 4 4 0 0 7 7 0 2 0 0
```

---

## 14. `medium_j14` — Apply the top-row color legend
**Difficulty:** medium

**Tags:** resize, legend, recolor, mapping

**Written rule:** Read the top row as adjacent old→new color pairs. Apply that recoloring to the body of the grid and drop the legend row from the output.

**Program function:** `solve_j14_palette_legend`

**Primitive names:** `palette_legend`


### Train examples

**Train 1 — input**

```text
2 7 4 3 0 0 0
0 2 2 0 4 4 0
0 2 0 0 0 4 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 7 7 0 3 3 0
0 7 0 0 0 3 0
0 0 0 0 0 0 0
```

**Train 2 — input**

```text
3 8 5 2 6 4 0 0
0 3 0 5 0 6 0 0
3 3 0 5 5 0 6 0
0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 8 0 2 0 4 0 0
8 8 0 2 2 0 4 0
0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
1 9 7 2 0 0
1 0 7 7 0 0
0 1 0 7 0 0
0 0 0 0 0 0
```

**Train 3 — output**

```text
9 0 2 2 0 0
0 9 0 2 0 0
0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
2 5 6 3 0 0 0
0 2 0 6 6 0 0
2 2 0 0 6 0 0
0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 5 0 3 3 0 0
5 5 0 0 3 0 0
0 0 0 0 0 0 0
```

---

## 15. `hard_j15` — Route a waypoint path through the maze
**Difficulty:** hard

**Tags:** same_size, pathfinding, waypoint, walls

**Written rule:** Find one shortest path from red(2) to green(4) that must pass through the waypoint yellow(3), moving only orthogonally through black(0) cells and avoiding gray(5) walls. Paint the whole routed path cyan(8).

**Program function:** `solve_j15_waypoint_path`

**Primitive names:** `waypoint_path`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 2 0 5 0 0 0 4 0
0 0 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0
0 5 0 0 0 5 0 0 0
0 5 5 5 0 5 5 5 0
0 0 0 3 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0
0 8 0 5 8 8 8 8 0
8 8 0 5 8 5 0 5 0
8 5 0 5 8 5 0 5 0
8 5 0 0 8 5 0 0 0
8 5 5 5 8 5 5 5 0
8 8 8 8 8 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0
0 2 5 0 0 0 4 0
0 0 5 0 5 0 5 0
0 0 0 0 5 0 5 0
0 5 5 0 5 0 0 0
0 3 0 0 0 0 5 0
0 0 0 5 5 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0
0 8 5 8 8 8 8 0
0 8 5 8 5 0 5 0
8 8 0 8 5 0 5 0
8 5 5 8 5 0 0 0
8 8 8 8 0 0 5 0
0 0 0 5 5 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 2 0 5 0 0 0 0 4 0
0 0 0 5 0 5 5 0 5 0
0 5 0 0 0 5 0 0 5 0
0 5 5 5 0 5 0 5 5 0
0 0 0 3 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 8 0 5 8 8 8 8 8 0
8 8 0 5 8 5 5 0 5 0
8 5 0 0 8 5 0 0 5 0
8 5 5 5 8 5 0 5 5 0
8 8 8 8 8 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 2 0 5 0 0 0 4 0
0 0 0 5 0 5 0 5 0
0 5 0 0 0 5 0 0 0
0 5 5 5 0 5 5 5 0
0 0 0 3 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 8 0 5 8 8 8 8 0
8 8 0 5 8 5 0 5 0
8 5 0 0 8 5 0 0 0
8 5 5 5 8 5 5 5 0
8 8 8 8 8 0 0 0 0
```

---

## 16. `hard_j16` — Take the majority overlay of three normalized shapes
**Difficulty:** hard

**Tags:** resize, objects, overlay, consensus

**Written rule:** Crop the three objects, align their top-left corners on a common canvas, and keep exactly the cells occupied in at least two of the three shapes. Paint the consensus shape cyan(8) and crop it.

**Program function:** `solve_j16_threeway_majority`

**Primitive names:** `threeway_majority`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 4 4 4 0 6 0 0 0
0 0 2 2 0 0 4 0 0 6 6 6 0
0 0 2 0 0 0 4 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
8 8 0
0 8 8
0 8 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 5 0 0 0 7 7 0 0
0 0 3 0 0 0 5 5 5 0 0 7 7 0
0 0 3 0 0 0 0 5 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
8 8 0
0 8 8
0 8 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 4 4 0 0 8 0 0
0 2 0 0 0 0 4 4 0 8 8 0
0 2 2 0 0 0 4 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
8 8
8 8
0 8
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 5 0 0 0 7 7 7 0
0 0 2 2 0 5 5 5 0 0 7 0 0
0 0 2 0 0 0 5 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
8 8 0
0 8 8
0 8 0
```

---

## 17. `hard_j17` — Rotate inserts into matching-color frames
**Difficulty:** hard

**Tags:** same_size, frames, matching, rotation

**Written rule:** Each hollow frame matches the external object of the same color. A key inside the frame says how to rotate that object before placing it into the frame interior: blue(1)=identity, red(2)=90° clockwise, green(3)=180°, yellow(4)=270° clockwise.

**Program function:** `solve_j17_frame_rotate_insert`

**Primitive names:** `frame_rotate_insert`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 2 2 2 2 0 0
0 2 0 0 0 0 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 4 0 0 0 0 0 0 0 0 4 2 2 4 0 0
0 4 4 0 0 0 0 0 0 0 4 0 1 4 0 0
0 4 0 0 0 0 0 0 0 0 4 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 3 0 0
0 0 3 0 0 0 0 0 0 0 0 3 0 4 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 6 6 0 0 0 0 0 0 0 0 6 0 3 0 6 0 0
0 0 6 6 0 0 0 0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 0
0 7 7 7 0 0 7 0 3 0 7 0
0 0 7 0 0 0 7 0 0 0 7 0
0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 7 0 7 0 7 0
0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 5 5 0 0 0 0 0 0 0 5 0 4 0 5 0
0 5 0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 5 0
0 8 8 8 0 0 0 0 0 0 8 0 0 8 0 0
0 8 0 0 0 0 0 0 0 0 8 0 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
```

---

## 18. `hard_j18` — Connect object anchors in x-order
**Difficulty:** hard

**Tags:** same_size, objects, routing, ordering

**Written rule:** Take the top-left anchor of each object’s bounding box, sort those anchors from left to right, and connect consecutive anchors with orthogonal polylines: first horizontally, then vertically. Draw the connector in cyan(8) on top of the original grid.

**Program function:** `solve_j18_anchor_polyline`

**Primitive names:** `anchor_polyline`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0
0 2 2 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 3 0 0 0 0 8 0 0 0 8 9 9 0
0 0 0 0 0 0 0 8 0 0 0 8 9 0 0
0 0 0 0 0 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 8 0 0 0 0 8 2 0
0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0
0 2 2 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 19. `hard_j19` — Use two keys to select and transform an object
**Difficulty:** hard

**Tags:** resize, keys, selection, transform

**Written rule:** The top-left key names which colored object to select. The top-right key names the transform to apply to that cropped object: blue(1)=identity, red(2)=rotate 90° clockwise, green(3)=horizontal mirror, yellow(4)=transpose, gray(5)=rotate 180°.

**Program function:** `solve_j19_dual_key_transform`

**Primitive names:** `dual_key_transform`


### Train examples

**Train 1 — input**

```text
4 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 4
4 4
4 0
```

**Train 2 — input**

```text
7 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 7 0 0 0 0
0 0 4 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 7
7 7
7 0
```

**Train 3 — input**

```text
2 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
2 0 0
2 2 2
0 0 2
```


### Test example

**Test 1 — input**

```text
6 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 6 0 0 0 0
0 0 3 3 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 6
6 6
0 6
```

---

## 20. `hard_j20` — Build a transformation timeline gallery
**Difficulty:** hard

**Tags:** resize, keys, gallery, sequential

**Written rule:** Read the top-row keys from left to right. Starting from the cropped object, apply each transform in sequence and output a horizontal gallery of every stage: the original, then after key 1, then after key 2, and so on, with one blank column between stages.

**Program function:** `solve_j20_transform_timeline`

**Primitive names:** `transform_timeline`


### Train examples

**Train 1 — input**

```text
2 3 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 4 0 0 0 4 0 4 0 0 4 4 0
0 4 4 0 4 4 0 4 4 0 0 4 4
0 0 0 0 4 0 0 0 4 0 0 0 0
```

**Train 2 — input**

```text
3 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
7 7 7 0 7 7 7 0 0 7 0
0 7 0 0 0 7 0 0 7 7 7
```

**Train 3 — input**

```text
4 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
2 0 0 2 2 0 0 0 2 0 2 0
2 2 0 0 2 2 0 2 2 0 2 2
0 2 0 0 0 0 0 2 0 0 0 2
```


### Test example

**Test 1 — input**

```text
2 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
5 5 0 0 0 5 0 0 5 5
0 5 5 0 5 5 0 5 5 0
0 0 0 0 5 0 0 0 0 0
```

---

## 21. `hard_j21` — Pack one object from each symmetry class into a 2x2 table
**Difficulty:** hard

**Tags:** resize, objects, symmetry, gallery

**Written rule:** Identify one object from each symmetry class and pack them into a 2×2 gallery: top-left = both axes symmetric, top-right = vertical-only, bottom-left = horizontal-only, bottom-right = neither. Use tight crops and separate the gallery cells with one blank row and one blank column.

**Program function:** `solve_j21_symmetry_table`

**Primitive names:** `symmetry_table`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 4 0 0 0 0
0 2 2 2 0 0 0 0 0 0 4 4 4 0 0 0
0 0 2 0 0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 8 8 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 2 0 0 0 4 0
2 2 2 0 4 4 4
0 2 0 0 4 0 4
0 0 0 0 0 0 0
6 6 0 0 8 8 0
0 6 6 0 0 8 8
6 6 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 5 0 0 0 0
0 3 3 3 0 0 0 0 0 5 5 5 0 0 0
0 3 0 3 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 7 7 0 0 0
0 0 9 9 0 0 0 0 0 0 0 7 7 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 5 0 0 0 3 0
5 5 5 0 3 3 3
0 5 0 0 3 0 3
0 0 0 0 0 0 0
9 9 0 0 7 7 0
0 9 9 0 0 7 7
9 9 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 8 0 0 0 0
0 6 6 6 0 0 0 0 0 0 8 8 8 0 0 0
0 0 6 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 6 0 0 0 8 0
6 6 6 0 8 8 8
0 6 0 0 8 0 8
0 0 0 0 0 0 0
4 4 0 0 2 2 0
0 4 4 0 0 2 2
4 4 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 5 0 0 0 0
0 3 3 3 0 0 0 0 0 0 5 5 5 0 0 0
0 0 3 0 0 0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 9 9 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 9 9 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 3 0 0 0 5 0
3 3 3 0 5 5 5
0 3 0 0 5 0 5
0 0 0 0 0 0 0
7 7 0 0 9 9 0
0 7 7 0 0 9 9
7 7 0 0 0 0 0
```

---

