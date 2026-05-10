# ARC-style Puzzle Bank: 21 More Tasks (Ninth Batch)

This ninth batch pushes into a different slice of the ARC design space:
run logic, header-driven projection, blocker-aware gravity, frame relocation,
shortest-path routing, rigid pivot motion, parity flood fills, dihedral shape
matching, and keyed Boolean composition.

## New helper primitives highlighted in this batch

- `run_endpoints` — Reduce each horizontal run to its first and last cell.
- `column_paint_from_header` — Treat top-row markers as seeds that paint full columns.
- `complete_monochrome_block` — Complete a 2x2 monochrome block when one corner is missing.
- `bridge_if_clear` — Connect two matching endpoints only when the segment between them is empty.
- `diagonal_consensus_fill` — Fill a center cell when its four diagonal neighbors agree.
- `global_color_parity` — Filter colors by whether their total frequency is even or odd.
- `half_mirror` — Mirror one half of the grid into the other half.
- `corner_color_select` — Use a corner key color to choose which object to crop.
- `color_area_rank` — Rank connected objects by area and map those ranks to new colors.
- `corner_rectangle_fill` — Fill a rectangle once all four same-color corners are present.
- `gravity_segments` — Apply gravity independently inside blocker-separated segments.
- `frame_center` — Center a cropped object inside a frame interior.
- `axis_mirror` — Reflect content across an explicit mirror axis.
- `hole_fill` — Detect enclosed black holes and fill them with the surrounding object color.
- `match_by_bbox_size` — Pair objects and containers by exact bounding-box size.
- `frame_insert` — Move an insert object into its matching hollow frame.
- `apply_script` — Map marker colors to geometric transforms.
- `pack_gallery` — Pack several cropped shapes into one gallery with gaps.
- `bfs_path` — Use breadth-first search to recover one shortest path through free cells.
- `orbit_about_pivot` — Rotate an object rigidly around a designated pivot cell.
- `parity_flood` — Color cells according to shortest-path or Manhattan-distance parity from a seed.
- `match_under_dihedral` — Compare shapes up to rotation and reflection.
- `dihedral_select` — Select the object whose normalized shape matches a template under dihedral symmetry.
- `keyed_boolean` — Choose union, intersection, or xor from a key marker.
- `shape_boolean` — Combine two aligned binary shapes with a Boolean set operation.

## Index
- `easy_i01` — **Keep only the endpoints of each horizontal run** (easy; same_size, runs, rows, projection; primitives: run_endpoints)
- `easy_i02` — **Top-row markers paint their full columns** (easy; same_size, markers, columns, projection; primitives: column_paint_from_header)
- `easy_i03` — **Complete monochrome L-triominoes into 2x2 squares** (easy; same_size, local, completion, blocks; primitives: complete_monochrome_block)
- `easy_i04` — **Bridge vertical gaps between matching endpoints** (easy; same_size, columns, segments, connection; primitives: bridge_if_clear)
- `easy_i05` — **Fill the center of each diagonal X** (easy; same_size, local, diagonals, completion; primitives: diagonal_consensus_fill)
- `easy_i06` — **Keep only colors that appear an even number of times** (easy; same_size, global, counting, color_filter; primitives: global_color_parity)
- `easy_i07` — **Mirror the upper half onto the lower half** (easy; same_size, symmetry, reflection, halves; primitives: half_mirror)
- `medium_i08` — **Crop the object whose color is named by the corner key** (medium; output_resize, selection, color_key, objects; primitives: corner_color_select)
- `medium_i09` — **Recolor objects by area rank** (medium; same_size, objects, ranking, recolor; primitives: color_area_rank)
- `medium_i10` — **Fill rectangles defined by same-color corner markers** (medium; same_size, geometry, rectangles, markers; primitives: corner_rectangle_fill)
- `medium_i11` — **Apply gravity inside vertical blocker segments** (medium; same_size, physics, gravity, blockers; primitives: gravity_segments)
- `medium_i12` — **Move the object into the center of the frame** (medium; same_size, objects, frames, relocation; primitives: frame_center)
- `medium_i13` — **Mirror the left side across the gray axis** (medium; same_size, symmetry, axis, objects; primitives: axis_mirror)
- `medium_i14` — **Fill each enclosed hole with its frame color** (medium; same_size, topology, holes, objects; primitives: hole_fill)
- `hard_i15` — **Match inserts to hollow frames by interior size** (hard; same_size, assignment, frames, objects; primitives: match_by_bbox_size, frame_insert)
- `hard_i16` — **Build a transformation gallery from a bottom-row script** (hard; output_resize, script, transforms, gallery; primitives: apply_script, pack_gallery)
- `hard_i17` — **Fill one shortest corridor path through the maze** (hard; same_size, pathfinding, maze, connectivity; primitives: bfs_path)
- `hard_i18` — **Rotate the object rigidly around the pivot using the key** (hard; same_size, rigid_motion, pivot, rotation; primitives: orbit_about_pivot)
- `hard_i19` — **Parity-fill the frame interior from the seed** (hard; same_size, flood_fill, parity, frames; primitives: parity_flood)
- `hard_i20` — **Find the candidate that matches the template up to dihedral symmetry** (hard; output_resize, shape_matching, dihedral, selection; primitives: match_under_dihedral, dihedral_select)
- `hard_i21` — **Apply the keyed Boolean operation to two shapes** (hard; output_resize, shape_algebra, boolean, keyed; primitives: keyed_boolean, shape_boolean)


## 1. `easy_i01` — Keep only the endpoints of each horizontal run

**Difficulty:** easy

**Tags:** same_size, runs, rows, projection

**Written rule:** Replace every horizontal run of equal nonzero color by just its two endpoints. A singleton stays as it is because its first and last cell coincide.

**Program function:** `solve_i01_run_endpoints`

**Primitive names:** `run_endpoints`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0
```

**Train 2 — input**

```text
3 3 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 6 6 6 0
0 0 0 0 0 0 0
8 8 8 0 0 0 0
```

**Train 2 — output**

```text
3 3 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 0 0 6 0
0 0 0 0 0 0 0
8 0 8 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7
```

---

## 2. `easy_i02` — Top-row markers paint their full columns

**Difficulty:** easy

**Tags:** same_size, markers, columns, projection

**Written rule:** Each nonzero cell in the top row is a column seed. Paint its entire column with that color and leave all other columns black(0).

**Program function:** `solve_i02_top_row_columns`

**Primitive names:** `column_paint_from_header`


### Train examples

**Train 1 — input**

```text
0 2 0 0 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 2 0 0 4 0 0 0
0 2 0 0 4 0 0 0
0 2 0 0 4 0 0 0
0 2 0 0 4 0 0 0
0 2 0 0 4 0 0 0
```

**Train 2 — input**

```text
3 0 0 0 6 0 1 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 0 0 0 6 0 1 0
3 0 0 0 6 0 1 0
3 0 0 0 6 0 1 0
3 0 0 0 6 0 1 0
```

**Train 3 — input**

```text
0 0 8 0 0 0 0 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 8 0 0 0 0 5
0 0 8 0 0 0 0 5
0 0 8 0 0 0 0 5
0 0 8 0 0 0 0 5
0 0 8 0 0 0 0 5
0 0 8 0 0 0 0 5
```


### Test example

**Test 1 — input**

```text
1 0 0 5 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
1 0 0 5 0 0 8 0 0
1 0 0 5 0 0 8 0 0
1 0 0 5 0 0 8 0 0
1 0 0 5 0 0 8 0 0
```

---

## 3. `easy_i03` — Complete monochrome L-triominoes into 2x2 squares

**Difficulty:** easy

**Tags:** same_size, local, completion, blocks

**Written rule:** Whenever a 2x2 window contains exactly three cells of the same nonzero color and one black(0) cell, fill the missing corner with that same color.

**Program function:** `solve_i03_complete_l_to_square`

**Primitive names:** `complete_monochrome_block`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0
0 2 2 0 0 0
0 2 0 0 0 0
0 0 0 0 3 3
0 0 0 0 0 3
0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0
0 2 2 0 0 0
0 2 2 0 0 0
0 0 0 0 3 3
0 0 0 0 3 3
0 0 0 0 0 0
```

**Train 2 — input**

```text
7 0 0 0 0 0
7 7 0 0 0 0
0 0 0 0 0 0
0 0 0 4 4 0
0 0 0 0 4 4
0 0 0 0 0 0
```

**Train 2 — output**

```text
7 7 0 0 0 0
7 7 0 0 0 0
0 0 0 0 0 0
0 0 0 4 4 4
0 0 0 4 4 4
0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 5 0 0
0 0 0 0 0 0
0 6 0 0 0 0
0 6 6 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0
0 0 5 5 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 6 6 0 0 0
0 6 6 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0
0 2 2 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 2 0 0
0 0 0 0 2 2 0
0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0
0 2 2 0 0 0 0
0 2 2 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 2 2 0
0 0 0 0 2 2 0
0 0 0 0 0 0 0
```

---

## 4. `easy_i04` — Bridge vertical gaps between matching endpoints

**Difficulty:** easy

**Tags:** same_size, columns, segments, connection

**Written rule:** If a column contains exactly two cells of the same nonzero color and every cell between them is black(0), fill the whole vertical segment between them with that color.

**Program function:** `solve_i04_vertical_bridge_clear`

**Primitive names:** `bridge_if_clear`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 2 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 4 0 0
0 0 0 0 4 0 0
0 0 0 0 4 0 0
```

**Train 2 — input**

```text
0 3 0 0 0 6 0
0 0 0 0 0 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 3 0 0 0 6 0
0 3 0 0 0 6 0
0 3 0 0 0 6 0
0 0 0 0 0 6 0
0 0 0 0 0 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 8 0 0
0 0 0 0 0 0 0
0 0 5 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 0 0 0 0
0 0 5 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 8 0 0
0 0 0 0 8 0 0
0 0 5 0 8 0 0
0 0 5 0 8 0 0
0 0 5 0 8 0 0
0 0 5 0 0 0 0
0 0 5 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 6 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 6 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 6 0 0
0 0 0 0 6 0 0
0 0 3 0 6 0 0
0 0 3 0 6 0 0
0 0 3 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
```

---

## 5. `easy_i05` — Fill the center of each diagonal X

**Difficulty:** easy

**Tags:** same_size, local, diagonals, completion

**Written rule:** If a black(0) cell has all four diagonal neighbors present and those four diagonals are the same nonzero color, recolor the center cell to that color.

**Program function:** `solve_i05_x_center_fill`

**Primitive names:** `diagonal_consensus_fill`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 2 0 2 0 0 0
0 0 0 0 0 0 0
0 2 0 2 0 0 0
0 0 0 0 4 0 4
0 0 0 0 0 0 0
0 0 0 0 4 0 4
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 2 0 2 0 0 0
0 0 2 0 0 0 0
0 2 0 2 0 0 0
0 0 0 0 4 0 4
0 0 0 0 0 4 0
0 0 0 0 4 0 4
```

**Train 2 — input**

```text
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 3 0 3 0
0 0 0 0 0 3 0 0
0 0 0 0 3 0 3 0
0 7 0 7 0 0 0 0
0 0 7 0 0 0 0 0
0 7 0 7 0 0 0 0
```

**Train 3 — input**

```text
8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 0 8 6 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
8 0 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
8 0 8 6 0 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 4 0 7 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 0 4 0 7 0 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
```

---

## 6. `easy_i06` — Keep only colors that appear an even number of times

**Difficulty:** easy

**Tags:** same_size, global, counting, color_filter

**Written rule:** Count how many cells each nonzero color occupies in the whole grid. Preserve colors with even total counts and erase every color whose count is odd.

**Program function:** `solve_i06_keep_even_frequency`

**Primitive names:** `global_color_parity`


### Train examples

**Train 1 — input**

```text
2 0 2 0 0 0 0
0 0 0 3 0 0 0
0 0 0 0 3 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
2 0 2 0 0 0 0
0 0 0 3 0 0 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 5 0 0 0 5 0
0 0 0 0 0 0 0
0 0 6 0 0 0 0
0 0 0 0 6 0 0
0 0 0 6 0 0 0
0 0 0 0 0 0 0
0 7 0 0 0 7 0
```

**Train 2 — output**

```text
0 5 0 0 0 5 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 7 0 0 0 7 0
```

**Train 3 — input**

```text
8 0 0 8 0 0 8
0 0 0 0 0 0 0
0 1 0 0 0 1 0
0 0 0 0 0 0 0
0 0 2 0 2 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 1 0 0 0 1 0
0 0 0 0 0 0 0
0 0 2 0 2 0 0
```


### Test example

**Test 1 — input**

```text
2 0 0 2 0 0 2
0 0 0 0 0 0 0
0 3 0 0 0 3 0
0 0 0 0 0 0 0
0 0 4 0 4 0 0
0 0 0 0 5 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 0 0 0 3 0
0 0 0 0 0 0 0
0 0 4 0 4 0 0
0 0 0 0 0 0 0
```

---

## 7. `easy_i07` — Mirror the upper half onto the lower half

**Difficulty:** easy

**Tags:** same_size, symmetry, reflection, halves

**Written rule:** Treat the top half of the grid as the source. Copy it into the bottom half by vertical mirroring, replacing whatever was originally in the lower half.

**Program function:** `solve_i07_mirror_upper_to_lower`

**Primitive names:** `half_mirror`


### Train examples

**Train 1 — input**

```text
2 0 0 2 0 0
0 3 3 0 0 0
0 0 0 0 0 0
9 9 9 9 9 9
8 8 8 8 8 8
7 7 7 7 7 7
```

**Train 1 — output**

```text
2 0 0 2 0 0
0 3 3 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 3 3 0 0 0
2 0 0 2 0 0
```

**Train 2 — input**

```text
0 4 0 0 0 0 7
0 0 4 0 0 0 0
0 0 0 0 0 0 0
1 1 1 1 1 1 1
2 2 2 2 2 2 2
3 3 3 3 3 3 3
```

**Train 2 — output**

```text
0 4 0 0 0 0 7
0 0 4 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 4 0 0 0 0
0 4 0 0 0 0 7
```

**Train 3 — input**

```text
0 0 0 0 0 5 0 0
0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9
8 8 8 8 8 8 8 8
7 7 7 7 7 7 7 7
6 6 6 6 6 6 6 6
```

**Train 3 — output**

```text
0 0 0 0 0 5 0 0
0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0
0 6 0 0 0 0 0 0
0 0 0 0 0 5 0 0
```


### Test example

**Test 1 — input**

```text
0 0 8 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9
7 7 7 7 7 7 7 7
6 6 6 6 6 6 6 6
5 5 5 5 5 5 5 5
```

**Test 1 — expected output**

```text
0 0 8 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0
```

---

## 8. `medium_i08` — Crop the object whose color is named by the corner key

**Difficulty:** medium

**Tags:** output_resize, selection, color_key, objects

**Written rule:** The top-left cell is a key color. Find the object of that same color elsewhere in the grid and output its tight crop.

**Program function:** `solve_i08_crop_corner_named_color`

**Primitive names:** `corner_color_select`


### Train examples

**Train 1 — input**

```text
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 4 4 0 3 0 0
0 0 0 0 0 0 3 0
```

**Train 1 — output**

```text
2 2
2 0
```

**Train 2 — input**

```text
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
5 5 5
0 5 0
```

**Train 3 — input**

```text
7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
7 0 0
7 7 7
```


### Test example

**Test 1 — input**

```text
6 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
6 0
6 0
6 6
```

---

## 9. `medium_i09` — Recolor objects by area rank

**Difficulty:** medium

**Tags:** same_size, objects, ranking, recolor

**Written rule:** Find the connected nonzero objects, rank them by area from smallest to largest, and recolor them in place as red(2), green(3), and yellow(4) respectively.

**Program function:** `solve_i09_recolor_by_area_rank`

**Primitive names:** `color_area_rank`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 8 0 0
0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 0 0
0 6 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0
0 5 0 0 0 9 0 0
0 5 0 5 0 9 0 0
0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0
0 4 0 0 0 2 0 0
0 4 0 4 0 2 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 4 0
0 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 2 0
0 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
0 6 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
0 3 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

---

## 10. `medium_i10` — Fill rectangles defined by same-color corner markers

**Difficulty:** medium

**Tags:** same_size, geometry, rectangles, markers

**Written rule:** Whenever four cells of the same color sit at the corners of an axis-aligned rectangle, fill that whole rectangle with that color.

**Program function:** `solve_i10_fill_corner_rectangles`

**Primitive names:** `corner_rectangle_fill`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 2 0 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 2 0 0 0 2 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
```

**Train 2 — input**

```text
3 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 4
3 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 3 3 3 3 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0
3 3 3 3 3 0 0 4 4 4
3 3 3 3 3 0 0 4 4 4
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0
0 0 6 6 6 6 0 0
0 0 6 6 6 6 0 0
0 0 6 6 6 6 0 0
0 0 6 6 6 6 0 0
0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 5 0 5
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 5
0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 5 5 5
0 2 2 2 2 0 0 5 5 5
0 2 2 2 2 0 0 5 5 5
0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0
```

---

## 11. `medium_i11` — Apply gravity inside vertical blocker segments

**Difficulty:** medium

**Tags:** same_size, physics, gravity, blockers

**Written rule:** Gray(5) cells are fixed blockers. In each column, every nonzero non-blocker cell falls downward as far as it can within each segment separated by blockers.

**Program function:** `solve_i11_gravity_with_blockers`

**Primitive names:** `gravity_segments`


### Train examples

**Train 1 — input**

```text
0 0 2 0 5 0 0
0 0 0 0 5 0 3
0 0 2 0 5 0 0
0 0 4 0 5 0 0
0 0 0 0 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 5 0 0
0 0 0 0 5 0 0
0 0 0 0 5 0 0
0 0 0 0 5 0 0
0 0 2 0 5 0 0
0 0 2 0 0 0 0
0 0 4 0 0 0 3
```

**Train 2 — input**

```text
0 2 0 5 0 7 0 8
0 0 0 5 0 7 0 0
0 4 0 5 0 0 5 0
0 0 0 5 0 0 0 8
0 2 0 5 0 3 0 0
0 0 0 5 0 0 5 0
0 0 0 5 0 3 0 0
0 0 0 5 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 5 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 5 0 0 5 0
0 0 0 5 0 0 0 0
0 0 0 5 0 7 0 0
0 2 0 5 0 7 5 0
0 4 0 5 0 3 0 8
0 2 0 5 0 3 0 8
```

**Train 3 — input**

```text
6 0 0 0 5 0 9 0 0
0 0 2 0 5 0 9 0 0
6 0 0 0 5 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 4
0 0 0 0 5 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 9 0 0
6 0 0 0 5 0 9 0 0
6 0 2 0 5 0 9 0 4
```


### Test example

**Test 1 — input**

```text
0 2 0 0 5 0 0 6 0
0 3 0 0 5 0 0 0 0
0 2 0 0 5 0 0 0 0
0 0 0 0 5 0 0 6 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 7 0
0 0 0 0 5 0 0 0 0
4 0 0 0 5 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 2 0 0 5 0 0 6 0
0 3 0 0 5 0 0 6 0
4 2 0 0 5 0 0 7 0
```

---

## 12. `medium_i12` — Move the object into the center of the frame

**Difficulty:** medium

**Tags:** same_size, objects, frames, relocation

**Written rule:** Keep the hollow rectangular frame where it is. Crop the other object, then place that cropped object centered inside the frame’s interior.

**Program function:** `solve_i12_center_object_in_frame`

**Primitive names:** `frame_center`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 3
0 8 8 8 8 8 8 8 3
0 8 0 0 0 0 0 8 3
0 8 0 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0
0 8 0 0 0 0 0 8 0
0 8 0 0 3 0 0 8 0
0 8 0 0 3 0 0 8 0
0 8 0 0 3 0 0 8 0
0 8 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 6 6 6 6 6 6 6 6
2 0 6 0 0 0 0 0 0 6
2 2 6 0 0 0 0 0 0 6
2 0 6 0 0 0 0 0 0 6
0 0 6 0 0 0 0 0 0 6
0 0 6 0 0 0 0 0 0 6
0 0 6 0 0 0 0 0 0 6
0 0 6 6 6 6 6 6 6 6
```

**Train 2 — output**

```text
0 0 6 6 6 6 6 6 6 6
0 0 6 0 0 0 0 0 0 6
0 0 6 0 0 2 0 0 0 6
0 0 6 0 0 2 2 0 0 6
0 0 6 0 0 2 0 0 0 6
0 0 6 0 0 0 0 0 0 6
0 0 6 0 0 0 0 0 0 6
0 0 6 6 6 6 6 6 6 6
```

**Train 3 — input**

```text
7 7 0 7 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 7 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
2 2 0 0 0 0 0 0 0 0 0
0 2 0 8 8 8 8 8 8 8 0
0 2 0 8 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 0 2 2 0 0 8 0
0 0 0 8 0 0 2 0 0 8 0
0 0 0 8 0 0 2 0 0 8 0
0 0 0 8 0 0 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 13. `medium_i13` — Mirror the left side across the gray axis

**Difficulty:** medium

**Tags:** same_size, symmetry, axis, objects

**Written rule:** A full gray(5) column marks the mirror axis. Keep the left side and copy it across the axis to the right by horizontal reflection.

**Program function:** `solve_i13_mirror_across_gray_axis`

**Primitive names:** `axis_mirror`


### Train examples

**Train 1 — input**

```text
0 0 0 0 5 0 0 0 7
0 3 3 0 5 0 0 0 0
0 0 3 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
3 0 0 0 5 0 0 0 0
3 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 7 0
```

**Train 1 — output**

```text
0 0 0 0 5 0 0 0 0
0 3 3 0 5 0 3 3 0
0 0 3 0 5 0 3 0 0
0 0 0 0 5 0 0 0 0
3 0 0 0 5 0 0 0 3
3 0 0 0 5 0 0 0 3
0 0 0 0 5 0 0 0 0
```

**Train 2 — input**

```text
0 8 0 0 0 5 0 0 0 0 0
0 8 8 0 0 5 0 0 0 0 0
0 0 0 8 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
8 8 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 — output**

```text
0 8 0 0 0 5 0 0 0 8 0
0 8 8 0 0 5 0 0 8 8 0
0 0 0 8 0 5 0 8 0 0 0
0 0 0 0 0 5 0 0 0 0 0
8 8 0 0 0 5 0 0 0 8 8
0 0 0 0 0 5 0 0 0 0 0
```

**Train 3 — input**

```text
2 0 0 0 5 0 0 0 0
0 2 0 0 5 0 0 0 0
0 2 2 0 5 0 0 0 0
2 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 2 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 3 — output**

```text
2 0 0 0 5 0 0 0 2
0 2 0 0 5 0 0 2 0
0 2 2 0 5 0 2 2 0
2 0 0 0 5 0 0 0 2
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 2 0 0
0 2 0 0 5 0 0 2 0
0 0 0 0 5 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 4 0 0 0 5 0 0 0 0 0
0 0 4 0 0 5 0 0 0 0 0
0 0 4 4 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
4 0 0 0 0 5 0 0 0 0 0
0 4 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 4 0 0 0 5 0 0 0 4 0
0 0 4 0 0 5 0 0 4 0 0
0 0 4 4 0 5 0 4 4 0 0
0 0 0 0 0 5 0 0 0 0 0
4 0 0 0 0 5 0 0 0 0 4
0 4 0 0 0 5 0 0 0 4 0
0 0 0 0 0 5 0 0 0 0 0
```

---

## 14. `medium_i14` — Fill each enclosed hole with its frame color

**Difficulty:** medium

**Tags:** same_size, topology, holes, objects

**Written rule:** For every hollow same-color object, detect its enclosed black(0) holes and fill those holes with the surrounding object’s color.

**Program function:** `solve_i14_fill_holes`

**Primitive names:** `hole_fill`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 7 7 7
0 2 0 0 2 0 7 0 7
0 2 0 0 2 0 7 0 7
0 2 0 0 2 0 7 0 7
0 2 2 2 2 0 7 7 7
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 7 7 7
0 2 2 2 2 0 7 7 7
0 2 2 2 2 0 7 7 7
0 2 2 2 2 0 7 7 7
0 2 2 2 2 0 7 7 7
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0
0 4 0 0 0 0 4 0
0 4 0 0 0 0 4 0
0 4 0 0 0 0 4 0
0 4 0 0 0 0 4 0
0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0
0 4 4 4 4 4 4 0
0 4 4 4 4 4 4 0
0 4 4 4 4 4 4 0
0 4 4 4 4 4 4 0
0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 3 3 3 3 0
0 6 0 6 0 3 0 0 3 0
0 6 0 6 0 3 0 0 3 0
0 6 0 6 0 3 0 0 3 0
0 6 6 6 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 3 3 3 3 0
0 6 6 6 0 3 3 3 3 0
0 6 6 6 0 3 3 3 3 0
0 6 6 6 0 3 3 3 3 0
0 6 6 6 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 0 0 2 0 0 6 6 6 0
0 2 0 0 2 0 0 6 0 6 0
0 2 0 0 2 0 0 6 0 6 0
0 2 0 0 2 0 0 6 6 6 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 6 6 6 0
0 2 2 2 2 0 0 6 6 6 0
0 2 2 2 2 0 0 6 6 6 0
0 2 2 2 2 0 0 6 6 6 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 15. `hard_i15` — Match inserts to hollow frames by interior size

**Difficulty:** hard

**Tags:** same_size, assignment, frames, objects

**Written rule:** Each filled object belongs inside the hollow frame whose interior has the same bounding-box size as that object. Move every insert into its matching frame and keep the frames.

**Program function:** `solve_i15_match_frames_and_inserts_by_size`

**Primitive names:** `match_by_bbox_size`, `frame_insert`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 8 8 8 8 8 8 0
0 8 0 0 0 8 0 0 0 8 0 0 0 0 8 0
0 8 0 0 0 8 0 0 0 8 0 0 0 0 8 0
0 8 0 0 0 8 0 0 0 8 0 0 0 0 8 0
0 8 8 8 8 8 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 3 3 3 3 0 0
0 2 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 8 8 8 8 8 8 0
0 8 2 0 0 8 0 0 0 8 3 3 3 3 8 0
0 8 2 0 0 8 0 0 0 8 0 3 0 0 8 0
0 8 2 2 2 8 0 0 0 8 0 3 0 0 8 0
0 8 8 8 8 8 0 0 0 8 0 3 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
7 0 0 0 0 0 7 0 0 7 7 7 7 7 0
7 0 0 0 0 0 7 0 0 7 0 0 0 7 0
7 0 0 0 0 0 7 0 0 7 0 0 0 7 0
7 7 7 7 7 7 7 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 4 0 7 0 0 0 7 0
0 0 0 0 0 0 0 4 0 7 7 7 7 7 0
2 2 2 2 2 0 0 4 0 0 0 0 0 0 0
0 0 0 0 2 0 0 4 0 0 0 0 0 0 0
0 0 0 0 2 0 0 4 4 4 0 0 0 0 0
```

**Train 2 — output**

```text
7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
7 2 2 2 2 2 7 0 0 7 7 7 7 7 0
7 0 0 0 0 2 7 0 0 7 4 0 0 7 0
7 0 0 0 0 2 7 0 0 7 4 0 0 7 0
7 7 7 7 7 7 7 0 0 7 4 0 0 7 0
0 0 0 0 0 0 0 0 0 7 4 0 0 7 0
0 0 0 0 0 0 0 0 0 7 4 4 4 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 8 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 6 8 0 0 6 6 6 6 6 0 0
0 6 0 0 0 0 0 6 8 0 0 6 0 0 0 6 0 0
0 6 0 0 0 0 0 6 8 0 0 6 0 0 0 6 0 0
0 6 0 0 0 0 0 6 8 0 0 6 0 0 0 6 0 0
0 6 6 6 6 6 6 6 8 8 8 6 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0
3 3 3 3 3 0 0 0 0 0 0 6 0 0 0 6 0 0
0 0 3 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0
0 0 3 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 6 3 3 3 3 3 6 0 0 0 6 6 6 6 6 0 0
0 6 0 0 3 0 0 6 0 0 0 6 8 0 0 6 0 0
0 6 0 0 3 0 0 6 0 0 0 6 8 0 0 6 0 0
0 6 0 0 3 0 0 6 0 0 0 6 8 0 0 6 0 0
0 6 6 6 6 6 6 6 0 0 0 6 8 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 8 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 8 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 8 8 8 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 8 8 8 8 8 8 0 0
0 8 0 0 0 0 8 0 0 0 8 0 0 0 0 8 0 0
0 8 0 0 0 0 8 0 0 0 8 0 0 0 0 8 0 0
0 8 0 0 0 0 8 0 0 0 8 0 0 0 0 8 0 0
0 8 0 0 0 0 8 0 0 0 8 0 0 0 0 8 0 0
0 8 8 8 8 8 8 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 0 0
2 2 2 2 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 8 8 8 8 8 8 0 0
0 8 2 2 2 2 8 0 0 0 8 3 3 3 3 8 0 0
0 8 0 0 2 0 8 0 0 0 8 3 0 0 0 8 0 0
0 8 0 0 2 0 8 0 0 0 8 3 0 0 0 8 0 0
0 8 0 0 2 0 8 0 0 0 8 3 0 0 0 8 0 0
0 8 8 8 8 8 8 0 0 0 8 3 3 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 16. `hard_i16` — Build a transformation gallery from a bottom-row script

**Difficulty:** hard

**Tags:** output_resize, script, transforms, gallery

**Written rule:** Crop the template object above the bottom row. Then read the bottom-row markers left to right: 1=identity, 2=rotate 90°, 3=rotate 180°, 4=horizontal flip. Output the transformed copies as a left-to-right gallery with one black column between copies.

**Program function:** `solve_i16_template_gallery_by_marker_script`

**Primitive names:** `apply_script`, `pack_gallery`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 2 0 4 0 0 0
```

**Train 1 — output**

```text
3 0 0 3 3 0 0 3
3 3 0 3 0 0 3 3
```

**Train 2 — input**

```text
0 0 0 0 6 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 1 0 2 0 4 0
```

**Train 2 — output**

```text
0 6 0 0 0 6 0 0 0 6 0 0 0 6 0
6 6 6 0 6 6 6 0 6 6 6 0 6 6 6
0 6 0 0 0 6 0 0 0 6 0 0 0 6 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 2 0 3 0 0
```

**Train 3 — output**

```text
7 7 7 0 0 7 0 0 7 0
0 7 0 0 7 7 0 7 7 7
0 0 0 0 0 7 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 4 0 1 0 3 0 0
```

**Test 1 — expected output**

```text
6 6 0 0 0 6 0 6 0 0 0 6 6 6
6 0 0 6 6 6 0 6 6 6 0 0 0 6
6 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 17. `hard_i17` — Fill one shortest corridor path through the maze

**Difficulty:** hard

**Tags:** same_size, pathfinding, maze, connectivity

**Written rule:** Gray(5) cells are walls. Two matching colored endpoints mark the start and goal; fill one shortest orthogonal black(0)-cell path between them with that color.

**Program function:** `solve_i17_shortest_path_fill`

**Primitive names:** `bfs_path`


### Train examples

**Train 1 — input**

```text
2 5 5 0 0 0 0
0 5 5 5 5 0 0
0 0 0 0 5 0 0
0 5 5 0 5 0 0
0 0 0 0 5 0 2
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
2 5 5 0 0 0 0
2 5 5 5 5 0 0
2 0 0 0 5 0 0
2 5 5 0 5 0 0
2 0 0 0 5 2 2
2 2 2 2 2 2 0
```

**Train 2 — input**

```text
3 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0
0 0 0 0 0 0 5 0
0 5 5 5 5 0 5 0
0 5 0 0 0 0 5 0
0 5 0 5 5 5 5 0
0 5 0 0 0 0 0 3
0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 3 3 3 3 3 3 3
0 5 5 5 5 5 5 3
0 0 0 0 0 0 5 3
0 5 5 5 5 0 5 3
0 5 0 0 0 0 5 3
0 5 0 5 5 5 5 3
0 5 0 0 0 0 0 3
0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
4 0 0 0 0 0 0
0 5 5 5 5 5 0
0 5 0 0 0 0 0
0 5 0 5 5 5 0
0 5 0 0 0 5 0
0 5 0 0 0 5 0
0 0 0 0 0 4 0
```

**Train 3 — output**

```text
4 0 0 0 0 0 0
4 5 5 5 5 5 0
4 5 0 0 0 0 0
4 5 0 5 5 5 0
4 5 0 0 0 5 0
4 5 0 0 0 5 0
4 4 4 4 4 4 0
```


### Test example

**Test 1 — input**

```text
2 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0
0 5 5 5 5 5 0 5 0
0 5 0 0 0 0 0 5 0
0 5 0 5 5 5 5 5 0
0 5 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 2
```

**Test 1 — expected output**

```text
2 0 0 0 0 0 0 0 0
2 5 5 5 5 5 5 5 0
2 0 0 0 0 0 0 5 0
2 5 5 5 5 5 0 5 0
2 5 0 0 0 0 0 5 0
2 5 0 5 5 5 5 5 0
2 5 0 0 0 0 0 0 0
2 5 5 5 5 5 5 5 0
2 2 2 2 2 2 2 2 2
```

---

## 18. `hard_i18` — Rotate the object rigidly around the pivot using the key

**Difficulty:** hard

**Tags:** same_size, rigid_motion, pivot, rotation

**Written rule:** The top-left key says how many clockwise quarter-turns to apply around the maroon(9) pivot: 1→0, 2→90°, 3→180°, 4→270°. Rotate the whole object rigidly around that pivot.

**Program function:** `solve_i18_rotate_object_around_pivot_by_key`

**Primitive names:** `orbit_about_pivot`


### Train examples

**Train 1 — input**

```text
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 3 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 9 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 9 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 2 0 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
4 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 4 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 19. `hard_i19` — Parity-fill the frame interior from the seed

**Difficulty:** hard

**Tags:** same_size, flood_fill, parity, frames

**Written rule:** Inside the hollow frame, use Manhattan distance from the single seed cell. Interior cells at even distance from the seed take the seed’s color; odd-distance interior cells take the frame’s color.

**Program function:** `solve_i19_parity_fill_inside_frame`

**Primitive names:** `parity_flood`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 6 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 0
0 2 6 2 6 2 6 2 0
0 2 2 6 2 6 2 2 0
0 2 6 2 6 2 6 2 0
0 2 2 6 2 6 2 2 0
0 2 6 2 6 2 6 2 0
0 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 0 7 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 4 4 7 4 7 4 4 0
0 0 4 7 4 7 4 7 4 0
0 0 4 4 7 4 7 4 4 0
0 0 4 7 4 7 4 7 4 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 0 3 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 — output**

```text
8 8 8 8 8 8 8 8 8 8
8 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 8
8 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 8
8 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 8
8 8 3 8 3 8 3 8 3 8
8 3 8 3 8 3 8 3 8 8
8 8 8 8 8 8 8 8 8 8
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 3 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 3 6 3 6 3 6 0 0
0 0 6 6 3 6 3 6 6 0 0
0 0 6 3 6 3 6 3 6 0 0
0 0 6 6 3 6 3 6 6 0 0
0 0 6 3 6 3 6 3 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 20. `hard_i20` — Find the candidate that matches the template up to dihedral symmetry

**Difficulty:** hard

**Tags:** output_resize, shape_matching, dihedral, selection

**Written rule:** Treat color 1 as the template object. Among the other objects, find the one with the same shape up to rotation or reflection, crop that matching candidate, and recolor it uniformly to cyan(8).

**Program function:** `solve_i20_select_dihedral_match`

**Primitive names:** `match_under_dihedral`, `dihedral_select`


### Train examples

**Train 1 — input**

```text
1 0 0 0 0 0 0 0 0 0 3 3
1 0 0 0 0 0 0 0 0 0 3 0
1 1 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
8 8
8 0
8 0
```

**Train 2 — input**

```text
0 1 1 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 4 0 0 0 0
1 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 2 2 0 0 0 0 0 0 7 7
0 0 0 0 2 2 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
8 8 0
0 8 8
0 0 8
```

**Train 3 — input**

```text
1 1 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 5 0
0 0 3 3 3 0 0 0 0 5 5 0
0 0 0 3 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 8
8 8
0 8
```


### Test example

**Test 1 — input**

```text
1 0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 4 4 0 0
0 1 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 7 0 0
0 0 5 0 0 0 0 0 0 7 7 0 0
0 0 5 5 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 8 8
8 8 0
```

---

## 21. `hard_i21` — Apply the keyed Boolean operation to two shapes

**Difficulty:** hard

**Tags:** output_resize, shape_algebra, boolean, keyed

**Written rule:** Align the two cropped objects by their top-left corners. The top-left key chooses the Boolean combination: 1=union, 2=intersection, 3=xor. Output the resulting shape in cyan(8).

**Program function:** `solve_i21_boolean_by_key`

**Primitive names:** `keyed_boolean`, `shape_boolean`


### Train examples

**Train 1 — input**

```text
1 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 3 0 0
0 2 0 0 0 0 0 3 0 0
0 2 2 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
8 8
8 8
8 8
```

**Train 2 — input**

```text
2 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 6 0 0
0 0 4 0 0 0 0 6 6 0 0
0 0 4 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
8
8
```

**Train 3 — input**

```text
3 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 7 0 0
0 5 5 0 0 0 0 7 7 0 0
0 0 5 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
8 8
0 0
8 8
```


### Test example

**Test 1 — input**

```text
3 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 4 0 0 0
0 0 2 0 0 0 0 0 4 4 0 0
0 0 2 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 8
8 0
8 8
```
