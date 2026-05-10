# ARC-style Puzzle Bank: 21 More Tasks (Eleventh Batch)

This eleventh batch deliberately pushes into a different slice of the ARC design space:
axis echoes, row/column projections, border outer-products, keyed selection, packing,
relative-offset transfer, aspect reasoning, dimension matching, topology matching,
stateful pathfinding, and keyed portal transforms.

## New helper primitives highlighted in this batch

- `vertical_echo` — Copy every cell to its mirror position across the vertical axis.
- `crosshair_project` — Project each seed across its full row and full column.
- `solid_to_frame` — Hollow a solid rectangle so only its border remains.
- `diagonal_echo` — Copy every cell to its transposed position across the main diagonal.
- `downcast` — Extend a seed straight downward to the bottom border.
- `block_main_diagonal` — Reduce each solid 2×2 block to its main diagonal.
- `border_intersections` — Fill the intersections defined by matching border markers.
- `corner_select_crop` — Select the object whose color matches the corner key and crop it.
- `count_rotate` — Rotate an object according to the number of key markers.
- `pack_by_area` — Crop objects and pack them in increasing order of area.
- `column_histogram` — Turn each column’s count into a bottom-aligned bar.
- `offset_transfer` — Copy a motif using its offset from one marker to another.
- `wall_shadow` — Project occupied cells rightward until a wall stops them.
- `aspect_recolor` — Recolor objects by whether their bounding boxes are tall, wide, or square.
- `socket_fit` — Match solid inserts to frames by interior dimensions.
- `normalized_overlay` — Normalize two objects and color-code only-A, only-B, and overlap.
- `keyed_path` — Find a shortest path whose state changes after collecting a key.
- `pack_by_holes` — Crop objects and pack them by increasing hole count.
- `portal_transfer` — Move a framed pattern into a target frame with a keyed transform.
- `ordered_centroid_polyline` — Connect component centers in key order using L-shaped segments.
- `topology_socket` — Match objects to frames by topological class (hole count).

## 1. `easy_k01` — Mirror singleton seeds across the vertical axis
**Difficulty:** easy

**Tags:** same_size, symmetry, projection, seeds

**Written rule:** Copy every nonzero cell to its mirror position across the vertical center line, keeping the original cells too.

**Program function:** `solve_k01_vertical_echo`

**Primitive names:** `vertical_echo`


### Train examples

**Train 1 — input**

```text
0 0 4 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 4 0 0 0 4 0 0
0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
```

---

## 2. `easy_k02` — Grow full crosshairs from seeds
**Difficulty:** easy

**Tags:** same_size, projection, rows, columns

**Written rule:** Each nonzero seed paints its entire row and entire column with the seed color.

**Program function:** `solve_k02_crosshair_project`

**Primitive names:** `crosshair_project`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 2 0 0 2 0 0
2 2 2 2 2 2 2
0 2 0 0 2 0 0
0 2 0 0 2 0 0
0 2 0 0 2 0 0
2 2 2 2 2 2 2
0 2 0 0 2 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 3 3 0 0 0 3 0 0
0 3 3 0 0 0 3 0 0
3 3 3 3 3 3 3 3 3
0 3 3 0 0 0 3 0 0
3 3 3 3 3 3 3 3 3
0 3 3 0 0 0 3 0 0
3 3 3 3 3 3 3 3 3
0 3 3 0 0 0 3 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 7 0 0 7 0 0
7 7 7 7 7 7 7 7
0 0 7 0 0 7 0 0
0 0 7 0 0 7 0 0
7 7 7 7 7 7 7 7
0 0 7 0 0 7 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 4 0 0 4 0 0 4 0
4 4 4 4 4 4 4 4 4
0 4 0 0 4 0 0 4 0
4 4 4 4 4 4 4 4 4
0 4 0 0 4 0 0 4 0
0 4 0 0 4 0 0 4 0
0 4 0 0 4 0 0 4 0
4 4 4 4 4 4 4 4 4
0 4 0 0 4 0 0 4 0
```

---

## 3. `easy_k03` — Turn solid rectangles into hollow frames
**Difficulty:** easy

**Tags:** same_size, rectangles, frames, local

**Written rule:** Every solid monochrome rectangle is hollowed out so that only its border remains.

**Program function:** `solve_k03_solid_to_frame`

**Primitive names:** `solid_to_frame`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 4 4 0 0 0 0
0 7 7 7 7 7 0 0 0
0 7 7 7 7 7 0 0 0
0 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 0 4 0 0 0 0
0 0 4 0 4 0 0 0 0
0 0 4 4 4 0 0 0 0
0 7 7 7 7 7 0 0 0
0 7 0 0 0 7 0 0 0
0 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0
0 0 9 9 9 9 0 0 3 3 0
0 0 9 9 9 9 0 0 3 3 0
0 0 9 9 9 9 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0 0 0
0 0 9 0 0 9 0 0 0 0 0
0 0 9 0 0 9 0 0 3 3 0
0 0 9 0 0 9 0 0 3 3 0
0 0 9 9 9 9 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## 4. `easy_k04` — Reflect cells across the main diagonal
**Difficulty:** easy

**Tags:** same_size, square, transpose, symmetry

**Written rule:** Copy every nonzero cell to its transposed position across the main diagonal, keeping the original cells too.

**Program function:** `solve_k04_diagonal_echo`

**Primitive names:** `diagonal_echo`


### Train examples

**Train 1 — input**

```text
0 0 0 2 0 0
0 0 0 0 5 0
0 0 0 0 0 7
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 2 0 0
0 0 0 0 5 0
0 0 0 0 0 7
2 0 0 0 0 0
0 5 0 0 0 0
0 0 7 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 4 0 0
0 0 0 0 0 0 3
0 0 0 6 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 4 0 0
0 0 0 0 0 0 3
0 0 0 6 0 0 0
0 0 6 0 0 0 0
4 0 0 0 0 8 0
0 0 0 0 8 0 0
0 3 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 9 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 9 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
9 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 1 0 0 0
0 0 0 0 8 0
0 0 0 6 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 1 0 0 0
0 0 0 0 8 0
1 0 0 6 0 0
0 0 6 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
```

---

## 5. `easy_k05` — Cast downward rays from seeds
**Difficulty:** easy

**Tags:** same_size, rays, projection, columns

**Written rule:** Every nonzero seed extends straight downward to the bottom border in the same color.

**Program function:** `solve_k05_downcast`

**Primitive names:** `downcast`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 8 0
0 2 0 0 0 0 8 0
0 2 0 0 0 0 8 0
0 2 0 0 5 0 8 0
0 2 0 0 5 0 8 0
0 2 0 0 5 0 8 0
0 2 0 0 5 0 8 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
3 0 0 7 0 0 0 0 0
3 0 0 7 0 0 0 0 0
3 0 0 7 0 0 0 4 0
3 0 0 7 0 0 0 4 0
3 0 0 7 0 0 0 4 0
3 0 0 7 0 0 0 4 0
```

**Train 3 — input**

```text
0 0 6 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 9 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 6 0 0 0 0
0 0 6 0 0 0 0
0 0 6 0 0 9 0
0 0 6 0 0 9 0
0 0 6 0 0 9 0
0 0 6 0 0 9 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 3 0
0 1 0 0 2 0 0 3 0
0 1 0 0 2 0 0 3 0
0 1 0 0 2 0 0 3 0
0 1 0 0 2 0 0 3 0
0 1 0 0 2 0 0 3 0
0 1 0 0 2 0 0 3 0
```

---

## 6. `easy_k06` — Keep only the main diagonal of each 2×2 block
**Difficulty:** easy

**Tags:** same_size, local, blocks, diagonal

**Written rule:** Each solid monochrome 2×2 block is reduced to its top-left and bottom-right diagonal cells.

**Program function:** `solve_k06_block_main_diagonal`

**Primitive names:** `block_main_diagonal`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 2 2 0 0 0 0 0
0 0 0 0 5 5 0 0
0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0
0 0 0 0 0 6 6 0 0
0 0 8 8 0 0 0 0 0
0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0
0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0
0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0
0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0
0 0 9 9 0 0 0 2 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 9 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
```

---

## 7. `easy_k07` — Fill the border-marker intersections
**Difficulty:** easy

**Tags:** same_size, markers, outer_product, borders

**Written rule:** Top-row markers choose columns and left-column markers choose rows; fill every matching-color row/column intersection.

**Program function:** `solve_k07_border_intersections`

**Primitive names:** `border_intersections`


### Train examples

**Train 1 — input**

```text
0 0 2 0 0 2 3 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 4 0 6 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 2 0 5 0 5
2 0 0 0 0 0 0
0 0 0 0 0 0 0
5 0 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 5 0 5
0 0 2 0 0 0 0
0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 3 0 0 7 0 0 3 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
```

---

## 8. `medium_k08` — Crop the corner-selected object
**Difficulty:** medium

**Tags:** selection, crop, marker_key, objects

**Written rule:** A single colored corner marker chooses the object of the same color; output that object cropped to its tight bounding box.

**Program function:** `solve_k08_corner_select_crop`

**Primitive names:** `corner_select_crop`


### Train examples

**Train 1 — input**

```text
4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 8 0 0 0
0 4 4 4 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 0 0
4 0 0
4 4 4
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 8 0 0 0
0 3 3 0 0 0 0 8 8 0 0
0 3 3 0 0 0 0 8 8 8 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
6 6 0
0 6 6
0 0 6
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 8 0 0 0
0 5 5 5 0 0 0 8 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 8 8
8 8 0
8 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 3 0 0 0 0
0 7 7 7 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5
```

**Test 1 — expected output**

```text
0 5 5
5 5 0
0 5 0
```

---

## 9. `medium_k09` — Rotate the object by marker count
**Difficulty:** medium

**Tags:** rotation, counting, marker_key, crop

**Written rule:** Count the top-row key markers: 1 means rotate the object 90° clockwise, 2 means 180°, and 3 means 270° clockwise. Output the rotated object tightly cropped.

**Program function:** `solve_k09_count_rotate`

**Primitive names:** `count_rotate`


### Train examples

**Train 1 — input**

```text
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 4 4
4 0 0
4 0 0
```

**Train 2 — input**

```text
0 9 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
6 6 6
0 0 6
```

**Train 3 — input**

```text
0 0 9 0 0 9 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
2 2 2
0 2 2
0 0 2
```


### Test example

**Test 1 — input**

```text
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 7 0
7 7 7
0 0 7
```

---

## 10. `medium_k10` — Pack objects left-to-right by area
**Difficulty:** medium

**Tags:** packing, ordering, objects, area

**Written rule:** Crop each connected object to its bounding box and pack the crops left-to-right in ascending order of object area, bottom-aligned with one blank column between them.

**Program function:** `solve_k10_pack_by_area`

**Primitive names:** `pack_by_area`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 7 7 0 0 0 0
0 2 2 2 0 0 7 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
7 7 0 2 0 0 0 4 4 4
7 7 0 2 0 0 0 0 4 0
7 0 0 2 2 2 0 0 4 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 3 3 0 8 0 0
5 0 0 0 3 3 0 0 8 8 0
5 5 5 0 0 3 0 0 8 8 8
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 4 4
0 0 6 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 9 0 4 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
6 6 0 0 4 4 0 9 0 4
6 6 0 4 4 0 0 9 0 0
6 0 0 4 0 0 0 9 9 9
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 5 5 5 0 8 0 0
2 0 0 0 0 5 0 0 8 8 0
2 2 2 0 0 5 0 0 8 8 8
```

---

## 11. `medium_k11` — Convert columns into bottom-aligned histograms
**Difficulty:** medium

**Tags:** histogram, columns, counting, same_size

**Written rule:** For each column, count its nonzero cells and replace them with a bottom-aligned vertical bar of the same height and color in that same column.

**Program function:** `solve_k11_column_histogram`

**Primitive names:** `column_histogram`


### Train examples

**Train 1 — input**

```text
0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 4 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 4 0 0 7 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 2 0 0 0 0 7 0
0 2 0 4 0 0 7 0
0 2 0 4 0 0 7 0
```

**Train 2 — input**

```text
0 0 0 0 5 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 8 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
3 0 0 0 5 0 0 0 0
3 0 0 0 5 0 0 8 0
```

**Train 3 — input**

```text
0 0 0 0 0 2 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 9 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 9 0
0 0 6 0 0 2 0 0 9 0
0 0 6 0 0 2 0 0 9 0
```


### Test example

**Test 1 — input**

```text
0 4 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 4 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 4 0 0 7 0 0 3 0
0 4 0 0 7 0 0 3 0
```

---

## 12. `medium_k12` — Transfer a motif by marker offset
**Difficulty:** medium

**Tags:** translation, relative_position, markers, crop

**Written rule:** Treat the color-1 cell as a source marker and the color-2 cell as a target marker. Copy the entire motif using the same relative offsets from the target marker, then crop tightly around the copied motif.

**Program function:** `solve_k12_offset_transfer`

**Primitive names:** `offset_transfer`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 4 0 5 0 0 0 0
0 0 0 4 6 0 0 0 0 0
0 0 0 0 6 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
4 0 5
4 6 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 9 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
7 7 0
0 8 8
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 3 0 0 0 0 0
0 0 0 0 0 2 4 3 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 3 0 0 0
2 4 3 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 2
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 4 0 5 0 0 0 0 0
0 0 0 0 4 6 0 0 0 0 0 0
0 0 0 0 0 6 5 0 0 0 0 0
```

**Test 1 — expected output**

```text
4 0
4 6
0 6
```

---

## 13. `medium_k13` — Project row shadows to a wall
**Difficulty:** medium

**Tags:** projection, wall, rows, same_size

**Written rule:** A vertical wall of color 5 stops the projection. Every colored cell to the left of the wall fills the empty cells to its right until the wall.

**Program function:** `solve_k13_wall_shadow`

**Primitive names:** `wall_shadow`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 5 0 0
0 2 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 4 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 6 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 5 0 0
0 2 2 2 2 2 2 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 4 4 4 4 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 6 6 6 6 6 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 3 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 7 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 9 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 3 3 3 3 3 3 3 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 7 7 7 7 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 9 9 9 9 9 9 5 0 0
0 0 0 0 0 0 0 0 5 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 5 0 0
4 0 0 0 0 0 5 0 0
0 0 0 2 0 0 5 0 0
0 0 0 0 0 0 5 0 0
0 8 0 0 0 0 5 0 0
0 0 0 0 0 0 5 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 5 0 0
4 4 4 4 4 4 5 0 0
0 0 0 2 2 2 5 0 0
0 0 0 0 0 0 5 0 0
0 8 8 8 8 8 5 0 0
0 0 0 0 0 0 5 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 7 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 2 2 2 2 2 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 7 7 7 7 7 7 7 7 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
```

---

## 14. `medium_k14` — Recolor objects by aspect ratio
**Difficulty:** medium

**Tags:** classification, objects, bounding_box, recolor

**Written rule:** Recolor each object according to its bounding-box aspect: tall objects become red(2), wide objects become green(3), and square objects become yellow(4).

**Program function:** `solve_k14_aspect_recolor`

**Primitive names:** `aspect_recolor`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 7 7 0 0
0 6 6 6 6 6 0 0 7 7 0 0
0 6 6 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 2 2 0 0
0 3 3 3 3 3 0 0 2 2 0 0
0 3 3 3 3 3 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 9 9 9 9 0
0 5 5 0 0 9 9 9 9 0
0 5 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 3 3 0
0 2 2 0 0 3 3 3 3 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 6 6 0 0 0 0
0 4 4 4 4 4 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 2 2 0 0 0 0
0 3 3 3 3 3 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4 4
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 8 8 8 0 0 4 4 4 4 0
0 0 8 8 8 0 0 4 4 4 4 0
0 0 8 8 8 0 0 4 4 4 4 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 3 3 3 3 0
0 0 2 2 2 0 0 3 3 3 3 0
0 0 2 2 2 0 0 3 3 3 3 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 15. `hard_k15` — Fit solid inserts into matching frames
**Difficulty:** hard

**Tags:** matching, frames, dimensions, placement

**Written rule:** Loose solid rectangles match frames by interior size. Place each insert into the frame whose empty interior has the same height and width.

**Program function:** `solve_k15_socket_fit`

**Primitive names:** `socket_fit`


### Train examples

**Train 1 — input**

```text
0 2 2 2 2 0 0 0 4 4 4 0 0 0
0 2 2 2 2 0 0 0 4 4 4 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8
0 8 8 8 8 8 8 0 0 8 0 0 0 8
0 8 0 0 0 0 8 0 0 8 0 0 0 8
0 8 0 0 0 0 8 0 0 8 8 8 8 8
0 8 0 0 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8
0 8 8 8 8 8 8 0 0 8 4 4 4 8
0 8 2 2 2 2 8 0 0 8 4 4 4 8
0 8 2 2 2 2 8 0 0 8 8 8 8 8
0 8 2 2 2 2 8 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 7 7 7 0 0 0 0 0 3 3 3 3 0
0 0 7 7 7 0 0 0 0 0 3 3 3 3 0
0 0 7 7 7 0 0 0 0 0 3 3 3 3 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 8 8 8 8 8 0 0 8 0 0 0 0 8
0 0 8 0 0 0 8 0 0 8 0 0 0 0 8
0 0 8 0 0 0 8 0 0 8 0 0 0 0 8
0 0 8 0 0 0 8 0 0 8 8 8 8 8 8
0 0 8 0 0 0 8 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 8 8 8 8 8 0 0 8 3 3 3 3 8
0 0 8 7 7 7 8 0 0 8 3 3 3 3 8
0 0 8 7 7 7 8 0 0 8 3 3 3 3 8
0 0 8 7 7 7 8 0 0 8 8 8 8 8 8
0 0 8 7 7 7 8 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 6 6 6 6 6 0 0 0 9 9 0 0
0 6 6 6 6 6 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 9 9 8 8
0 8 8 8 8 8 8 8 0 8 0 0 8
0 8 0 0 0 0 0 8 0 8 0 0 8
0 8 0 0 0 0 0 8 0 8 0 0 8
0 8 8 8 8 8 8 8 0 8 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0
0 8 6 6 6 6 6 8 0 0 0 0 0
0 8 6 6 6 6 6 8 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 5 5 5 0 0 0 0 0 0 2 2 2 2 2 0
0 5 5 5 0 0 0 0 0 0 2 2 2 2 2 0
0 5 5 5 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 8 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 8 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 8 0 8 0 0 0 0 0 8 0
0 0 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 0 8 2 2 2 2 2 8 0
0 0 8 5 5 5 8 0 8 2 2 2 2 2 8 0
0 0 8 5 5 5 8 0 8 2 2 2 2 2 8 0
0 0 8 5 5 5 8 0 8 2 2 2 2 2 8 0
0 0 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 16. `hard_k16` — Color-code the normalized overlap of two objects
**Difficulty:** hard

**Tags:** boolean_shape_algebra, normalization, overlay, objects

**Written rule:** Normalize the color-2 object and the color-3 object to their own top-left corners, overlay them, and output a crop where cells only in the first object stay 2, only in the second stay 3, and shared cells become cyan(8).

**Program function:** `solve_k16_normalized_overlay`

**Primitive names:** `normalized_overlay`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
8 3 3
2 3 0
2 8 2
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
8 0 0
8 8 2
3 3 3
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 8 8
8 8 0
3 2 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
8 0 0
8 8 3
2 2 2
```

---

## 17. `hard_k17` — Find the key-and-door shortest path
**Difficulty:** hard

**Tags:** pathfinding, state, maze, key_door

**Written rule:** Find the shortest orthogonal route from start red(2) to goal green(3), but door cells 5 can only be crossed after the key cell 4 has been visited. Mark the traversed empty cells with orange(7).

**Program function:** `solve_k17_keyed_path`

**Primitive names:** `keyed_path`


### Train examples

**Train 1 — input**

```text
8 8 8 8 8 8 8 8 8
8 2 0 0 8 0 0 0 8
8 0 8 0 8 0 8 5 8
8 0 8 0 0 0 8 0 8
8 0 8 8 8 0 8 0 8
8 0 0 0 4 0 8 3 8
8 8 8 8 8 8 8 8 8
```

**Train 1 — output**

```text
8 8 8 8 8 8 8 8 8
8 2 0 0 8 7 7 7 8
8 7 8 0 8 7 8 5 8
8 7 8 0 0 7 8 7 8
8 7 8 8 8 7 8 7 8
8 7 7 7 4 7 8 3 8
8 8 8 8 8 8 8 8 8
```

**Train 2 — input**

```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 0 8 0 0 0 8
8 8 8 0 8 0 8 0 8 5 8
8 0 0 0 8 0 0 0 8 0 8
8 0 8 8 8 8 8 0 8 0 8
8 0 8 4 0 0 0 0 8 3 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 — output**

```text
8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 7 7 8 7 7 7 8
8 8 8 0 8 7 8 7 8 5 8
8 0 0 0 8 7 7 7 8 7 8
8 0 8 8 8 8 8 7 8 7 8
8 0 8 4 7 7 7 7 8 3 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 — input**

```text
8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 0 0 0 8
8 0 8 0 8 0 8 5 8 8
8 0 8 0 0 0 8 0 0 8
8 0 8 8 8 0 8 0 8 8
8 4 0 0 0 0 8 3 8 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 — output**

```text
8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 0 0 0 8
8 0 8 0 8 0 8 5 8 8
8 0 8 0 0 0 8 0 0 8
8 0 8 8 8 0 8 0 8 8
8 4 0 0 0 0 8 3 8 8
8 8 8 8 8 8 8 8 8 8
```


### Test example

**Test 1 — input**

```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 8 0 0 0 0 3 8
8 0 8 0 8 0 8 8 8 5 8
8 0 8 0 0 0 8 0 0 0 8
8 0 8 8 8 8 8 0 8 0 8
8 0 0 4 0 0 0 0 8 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Test 1 — expected output**

```text
8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 8 7 7 7 7 3 8
8 0 8 7 8 7 8 8 8 5 8
8 0 8 7 7 7 8 0 0 0 8
8 0 8 8 8 8 8 0 8 0 8
8 0 0 4 0 0 0 0 8 0 8
8 8 8 8 8 8 8 8 8 8 8
```

---

## 18. `hard_k18` — Pack objects by hole count
**Difficulty:** hard

**Tags:** topology, holes, packing, ordering

**Written rule:** Crop each connected object and pack the crops left-to-right in ascending order of the number of holes inside the object, bottom-aligned with one blank column between them.

**Program function:** `solve_k18_pack_by_holes`

**Primitive names:** `pack_by_holes`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 4 4 4 0 0 0 0 0
0 2 0 0 0 0 4 0 0 4 0 0 0 0 0
0 2 2 2 0 0 4 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 4 4 4 4 0 7 0 7 0 7
2 0 0 0 4 0 0 4 0 7 0 7 0 7
2 0 0 0 4 0 0 4 0 7 0 7 0 7
2 2 2 0 4 4 4 4 0 7 7 7 7 7
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 6 6 6 6 6 0 0
0 0 3 3 0 0 0 0 6 0 0 0 6 0 0
0 0 3 0 0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 9 9 9 9 9 9 9 6 6 0 0
0 0 0 0 9 0 0 9 0 0 9 0 0 0 0
0 0 0 0 9 0 0 9 0 0 9 0 0 0 0
0 0 0 0 9 0 0 9 0 0 9 0 0 0 0
0 0 0 0 9 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 6 6 6 6 6 0 9 9 9 9 9 9 9
0 0 0 6 0 0 0 6 0 9 0 0 9 0 0 9
3 3 0 6 0 0 0 6 0 9 0 0 9 0 0 9
3 3 0 6 0 0 0 6 0 9 0 0 9 0 0 9
3 0 0 9 9 9 6 6 0 9 9 9 9 9 9 9
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 8 0 8 0
0 0 0 0 0 0 0 0 8 0 8 0 8 0
0 7 7 7 7 0 0 0 8 0 8 0 8 0
0 7 0 0 7 0 0 0 8 8 8 8 8 0
0 7 0 0 7 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 7 7 7 7 0 8 0 8 0 8
0 0 0 0 7 0 0 7 0 8 0 8 0 8
5 0 0 0 7 0 0 7 0 8 0 8 0 8
5 5 5 0 7 7 7 7 0 8 8 8 8 8
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 2 2 2 2 2 0 0 0
0 4 4 0 0 0 0 0 2 0 0 0 2 0 0 0
0 4 4 4 0 0 0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 2 0 0 0
0 0 0 0 0 6 0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 6 0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 6 0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 2 2 2 2 2 0 6 6 6 6 6 6 6
0 0 0 0 2 0 0 0 2 0 6 0 0 6 0 0 6
4 0 0 0 2 0 0 0 2 0 6 0 0 6 0 0 6
4 4 0 0 2 0 0 0 2 0 6 0 0 6 0 0 6
4 4 4 0 6 6 6 6 2 0 6 6 6 6 6 6 6
```

---

## 19. `hard_k19` — Transfer a framed pattern through a keyed portal
**Difficulty:** hard

**Tags:** frames, transforms, portal, marker_key

**Written rule:** Two same-sized frames form a portal pair. Move the source frame’s interior pattern into the empty target frame using the key marker: 1 = mirror left-right, 2 = mirror top-bottom, 3 = rotate 180°.

**Program function:** `solve_k19_portal_transfer`

**Primitive names:** `portal_transfer`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 7 7 7 7 7 0
0 6 4 0 5 6 0 0 0 7 0 0 0 7 0
0 6 0 8 0 6 0 0 0 7 0 0 0 7 0
0 6 9 0 4 6 0 0 0 7 0 0 0 7 0
0 6 6 6 6 6 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 7 7 7 7 7 0
0 6 0 0 0 6 0 0 0 7 5 0 4 7 0
0 6 0 0 0 6 0 0 0 7 0 8 0 7 0
0 6 0 0 0 6 0 0 0 7 4 0 9 7 0
0 6 6 6 6 6 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0 7 7 7 7 7 7
0 0 6 4 0 5 0 6 0 0 7 0 0 0 0 7
0 0 6 0 8 0 9 6 0 0 7 0 0 0 0 7
0 0 6 5 0 4 0 6 0 0 7 0 0 0 0 7
0 0 6 0 0 0 0 6 0 0 7 0 0 0 0 7
0 0 6 6 6 6 6 6 0 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0 7 7 7 7 7 7
0 0 6 0 0 0 0 6 0 0 7 0 0 0 0 7
0 0 6 0 0 0 0 6 0 0 7 5 0 4 0 7
0 0 6 0 0 0 0 6 0 0 7 0 8 0 9 7
0 0 6 0 0 0 0 6 0 0 7 4 0 5 0 7
0 0 6 6 6 6 6 6 0 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 7 7 7 7 7 0
0 6 4 5 0 6 0 0 7 0 0 0 7 0
0 6 0 8 9 6 0 0 7 0 0 0 7 0
0 6 4 0 5 6 0 0 7 0 0 0 7 0
0 6 6 6 6 6 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 7 7 7 7 7 0
0 6 0 0 0 6 0 0 7 5 0 4 7 0
0 6 0 0 0 6 0 0 7 9 8 0 7 0
0 6 0 0 0 6 0 0 7 0 5 4 7 0
0 6 6 6 6 6 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 7 7 7 7 7 7
0 0 6 4 0 5 0 6 0 7 0 0 0 0 7
0 0 6 0 8 0 9 6 0 7 0 0 0 0 7
0 0 6 5 0 4 0 6 0 7 0 0 0 0 7
0 0 6 6 6 6 6 6 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 7 7 7 7 7 7
0 0 6 0 0 0 0 6 0 7 0 5 0 4 7
0 0 6 0 0 0 0 6 0 7 9 0 8 0 7
0 0 6 0 0 0 0 6 0 7 0 4 0 5 7
0 0 6 6 6 6 6 6 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 20. `hard_k20` — Connect component centers in color order
**Difficulty:** hard

**Tags:** geometry, ordering, polylines, centers

**Written rule:** Order the components by color value and connect their centers in that order using L-shaped polylines: horizontal first, then vertical. Each segment uses the color of its starting component.

**Program function:** `solve_k20_ordered_centroid_polyline`

**Primitive names:** `ordered_centroid_polyline`


### Train examples

**Train 1 — input**

```text
0 2 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 7 0 0
0 2 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 7 0 0
0 0 0 0 0 2 0 0 0 4 0 0
0 0 0 0 0 2 0 0 0 4 0 0
0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1 8 0
0 0 0 0 0 0 0 0 0 0 1 8 8 8
0 0 3 0 0 0 0 0 0 0 0 0 8 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 1 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 8 0
0 0 1 0 0 0 0 0 0 0 0 0 6 0
0 0 3 3 3 3 3 3 0 0 0 0 6 0
0 0 0 0 0 0 0 3 0 0 0 0 6 0
0 0 0 0 0 0 0 3 0 0 0 0 6 0
0 0 0 0 0 0 0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 2 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 5 0 0 0 0 7 0
0 0 0 5 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 7 0
0 0 0 0 2 0 0 0 0 5 0
0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 1 0 0 0 0 0 0 0 9 9 9
0 1 1 1 0 0 0 0 0 0 0 9 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 6 0 0 0 4 4 4 0
0 0 0 0 6 6 6 0 0 0 4 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 1 1 1 1 1 1 1 1 1 6 0
0 0 0 0 0 0 0 0 0 0 1 6 0
0 0 0 0 0 0 0 0 0 0 1 6 0
0 0 0 0 0 0 0 0 0 0 1 6 0
0 0 0 0 0 4 4 4 4 4 4 6 0
0 0 0 0 0 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## 21. `hard_k21` — Place objects into topology-matching sockets
**Difficulty:** hard

**Tags:** matching, topology, frames, placement

**Written rule:** Frame color encodes the required topology: color 1 wants a zero-hole object, color 2 wants a one-hole object, and color 3 wants a two-hole object. Center each object inside the matching frame.

**Program function:** `solve_k21_topology_socket`

**Primitive names:** `topology_socket`


### Train examples

**Train 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 1 1 1 1 0 0 2 0 0 0 0 2 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0 8 8 8 8 8 0 0
0 6 0 0 0 0 0 0 0 7 0 0 7 0 0 0 0 8 0 8 0 8 0 0
0 6 0 0 0 0 0 0 0 7 0 0 7 0 0 0 0 8 0 8 0 8 0 0
0 6 6 6 0 0 0 0 0 7 7 7 7 0 0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 8 8 8 8 8 3 0
0 1 6 0 0 1 0 0 2 7 7 7 7 2 0 0 3 8 0 8 0 8 3 0
0 1 6 0 0 1 0 0 2 7 0 0 7 2 0 0 3 8 0 8 0 8 3 0
0 1 6 6 6 1 0 0 2 7 0 0 7 2 0 0 3 8 0 8 0 8 3 0
0 1 1 1 1 1 0 0 2 7 7 7 7 2 0 0 3 8 8 8 8 8 3 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 2 2 2 2 2 2 2 0 0 3 3 3 3 3 3
0 1 0 0 0 0 1 0 0 2 0 0 0 0 0 2 0 0 3 0 0 0 0 3
0 1 0 0 0 0 1 0 0 2 0 0 0 0 0 2 0 0 3 0 0 0 0 3
0 1 0 0 0 0 1 0 0 2 0 0 0 0 0 2 0 0 3 0 0 0 0 3
0 1 0 0 0 0 1 0 0 2 0 0 0 0 0 2 0 0 3 0 0 0 0 3
0 1 1 1 1 1 1 0 0 2 0 0 0 0 0 2 0 0 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 6 6 6 6 6 0
0 4 4 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 6 0 6 0 6 0
0 4 4 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 6 0 6 0 6 0
0 4 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 6 0 6 0 6 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 2 2 2 2 2 2 2 0 0 6 6 6 6 6 3
0 1 0 4 4 0 1 0 0 2 5 5 5 5 5 2 0 0 6 0 6 0 6 3
0 1 0 4 4 0 1 0 0 2 5 0 0 0 5 2 0 0 6 0 6 0 6 3
0 1 0 4 0 0 1 0 0 2 5 0 0 0 5 2 0 0 6 0 6 0 6 3
0 1 0 0 0 0 1 0 0 2 5 0 0 0 5 2 0 0 6 6 6 6 6 3
0 1 1 1 1 1 1 0 0 2 5 5 5 5 5 2 0 0 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 3 3 3 3 0
0 1 0 0 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 3 0
0 1 0 0 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 3 0
0 1 0 0 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 3 0
0 1 1 1 1 1 1 1 0 0 2 0 0 0 0 2 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0 0 9 9 9 9 9 0
0 7 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 9 0 9 0 9 0
0 7 7 7 0 0 0 0 0 0 8 0 0 8 0 0 0 0 9 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0 0 9 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 — output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 9 9 9 9 9 0
0 1 0 7 0 0 0 1 0 0 2 8 8 8 8 2 0 0 9 0 9 0 9 0
0 1 0 7 7 7 0 1 0 0 2 8 0 0 8 2 0 0 9 0 9 0 9 0
0 1 0 0 0 0 0 1 0 0 2 8 0 0 8 2 0 0 9 0 9 0 9 0
0 1 1 1 1 1 1 1 0 0 2 8 8 8 8 2 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


### Test example

**Test 1 — input**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 0 0 0 1 0 0 2 0 0 0 0 2 0 0 3 0 0 0 0 0 3 0
0 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 7 7 7 7 7 0 0
0 4 0 0 0 0 0 0 6 0 0 0 6 0 0 0 0 7 0 7 0 7 0 0
0 4 4 0 0 0 0 0 6 0 0 0 6 0 0 0 0 7 0 7 0 7 0 0
0 4 4 4 0 0 0 0 6 0 0 0 6 0 0 0 0 7 0 7 0 7 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 — expected output**

```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 6 6 6 6 6 2 0 0 3 7 7 7 7 7 3 0
0 1 4 0 0 1 0 0 6 0 0 0 6 2 0 0 3 7 0 7 0 7 3 0
0 1 4 4 0 1 0 0 6 0 0 0 6 2 0 0 3 7 0 7 0 7 3 0
0 1 4 4 4 1 0 0 6 0 0 0 6 2 0 0 3 7 0 7 0 7 3 0
0 1 0 0 0 1 0 0 6 6 6 6 6 2 0 0 3 7 7 7 7 7 3 0
0 1 1 1 1 1 0 0 2 2 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

---
