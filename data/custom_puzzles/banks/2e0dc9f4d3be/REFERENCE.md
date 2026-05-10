# ARC Puzzle Bank — Set 22


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `four_ortho_center`: Fill an empty center cell when its four orthogonal neighbors share one nonzero color.
- `prune_singletons`: Remove every nonzero cell that has no orthogonally adjacent cell of the same color.
- `complete_mono_2x2`: Complete any 2x2 block containing exactly three equal nonzero cells and one zero.
- `mirror_down`: Reflect all nonzero cells in the top half across the horizontal midline into the bottom half.
- `diag_extend_one`: Extend each same-color diagonal domino by one cell at every open end along its diagonal.
- `top_beam_fill`: Let each top-border seed color beam downward until a blocker is hit.
- `seed_plus_bloom`: Grow a four-arm plus around each isolated interior seed.
- `largest_crop`: Crop out the largest monochrome object by area.
- `aspect_recolor`: Recolor every object by its bounding-box aspect class.
- `rect_outline_fill`: Turn each rectangular outline into a filled rectangle of the same color.
- `area_gallery`: Crop objects and concatenate them left-to-right sorted by area.
- `frame_seed_fill`: Fill each hollow frame interior with the color of its interior seed.
- `vector_clone_union`: Clone the main object by the vector between two marker cells and union the result.
- `corner_key_transform_crop`: Use a corner key to transform the main object crop and output only that crop.
- `dual_key_frame_insert`: Select an object by one key, transform it by another, and center it inside a frame.
- `normalize_overlay_priority`: Normalize two objects to one origin and overlay them with keyed overlap priority.
- `key_door_bfs`: Find a shortest path that may pass through a door only after collecting the key.
- `contact_matrix`: Output an adjacency matrix for top-left-sorted objects using orthogonal contact.
- `transform_script_gallery`: Emit the initial object crop and each cumulative transform state in a gallery.
- `symmetry_frame_match`: Insert each object into the frame matching its reflection-symmetry class.
- `portal_checkpoint_path`: Find a shortest path that must visit a checkpoint and may use linked portals.

## easy_p01 — Orthogonal Center Fill (easy)

**Tags:** local, completion, same_size

**Written rule:** Fill any 0 cell whose up, down, left, and right neighbors are all the same nonzero color. Leave everything else unchanged.

**Program:** `solve_easy_p01`

**Primitives:** `four_ortho_center`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 4 0 0 0 7 0 0
0 0 0 0 7 0 7 0
0 0 0 0 0 7 0 0
0 0 3 0 0 0 0 0
0 3 0 3 0 0 0 0
0 0 3 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 4 0 0 0 7 0 0
0 0 0 0 7 7 7 0
0 0 0 0 0 7 0 0
0 0 3 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 3 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 2 0 0 0 0 0
2 0 2 0 0 0 0
0 2 0 8 0 0 0
0 0 8 0 8 0 0
0 0 0 8 0 6 0
0 0 0 0 6 0 6
0 0 0 0 0 6 0
```

#### Train 3 output
```text
0 2 0 0 0 0 0
2 2 2 0 0 0 0
0 2 0 8 0 0 0
0 0 8 8 8 0 0
0 0 0 8 0 6 0
0 0 0 0 6 6 6
0 0 0 0 0 6 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 3 0 4 0 0
0 0 0 3 0 3 0 0 0
0 0 7 0 3 0 0 0 0
0 7 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 3 0 4 0 0
0 0 0 3 3 3 0 0 0
0 0 7 0 3 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## easy_p02 — Prune Singletons (easy)

**Tags:** local, components, filtering

**Written rule:** Delete every nonzero cell that has no orthogonally adjacent cell of the same color. Keep all cells that belong to a same-color orthogonal cluster.

**Program:** `solve_easy_p02`

**Primitives:** `prune_singletons`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 4
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
9 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 2
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 2
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## easy_p03 — Complete Monochrome 2x2 Blocks (easy)

**Tags:** local, 2x2, completion

**Written rule:** Whenever a 2x2 window contains exactly three equal nonzero cells and one 0, fill the missing corner with that same color.

**Program:** `solve_easy_p03`

**Primitives:** `complete_mono_2x2`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0
0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0
0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 0 0
0 5 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 5 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 4 0 0 0 2 2 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0
0 4 4 0 0 2 2 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## easy_p04 — Mirror Down (easy)

**Tags:** reflection, same_size, copy

**Written rule:** Reflect every nonzero cell in the top half of the grid across the horizontal midline into the corresponding cell in the bottom half.

**Program:** `solve_easy_p04`

**Primitives:** `mirror_down`

### Train pairs

#### Train 1 input
```text
0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 0 2 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 0 2 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 5 0 0
0 0 2 0 0 0 5 0 0
0 2 0 0 0 0 0 0 0
```

#### Train 2 input
```text
4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 7 0 0
0 4 4 0 0 0 0 0
4 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 3 0
0 6 0 0 0 0 0 3 0 0
0 0 6 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 3 0
0 6 0 0 0 0 0 3 0 0
0 0 6 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 6 0 0 0 3 0 0 0
0 6 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 2 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 2 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 2 0
0 0 0 0 8 0 0 0 0
```

## easy_p05 — Diagonal Domino Extension (easy)

**Tags:** diagonal, growth, same_size

**Written rule:** Each same-color diagonal domino grows by one additional cell at every open end along that same diagonal.

**Program:** `solve_easy_p05`

**Primitives:** `diag_extend_one`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 5
0 0 0 2 0 0 0 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0
3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0
3 0 0 7 0 0 0 0
0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 6 0 0 0 0 5 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 5
0 6 0 0 0 0 0 0 5 0
0 0 6 0 0 0 0 5 0 0
0 0 0 6 0 2 5 0 0 0
0 0 0 0 6 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p06 — Top Beam Fill (easy)

**Tags:** beam, columns, blockers

**Written rule:** Every nonzero top-row seed projects its color downward through 0s in the same column until a blocker 9 is reached.

**Program:** `solve_easy_p06`

**Primitives:** `top_beam_fill`

### Train pairs

#### Train 1 input
```text
0 2 0 0 5 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 2 0 0 5 0 0 3 0
0 2 0 0 5 0 0 3 0
0 2 0 0 9 0 0 3 0
0 2 0 0 0 0 0 3 0
0 9 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
4 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 0 6 0 0 8 0
4 0 0 6 0 0 8 0
4 0 0 6 0 0 8 0
4 0 0 9 0 0 8 0
4 0 0 0 0 0 8 0
9 0 0 0 0 0 8 0
0 0 0 0 0 0 8 0
```

#### Train 3 input
```text
0 0 7 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 9 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 9 0
0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 7 0 0 2 0
0 0 7 0 0 2 0
0 0 7 0 0 2 0
0 0 7 0 0 2 0
0 0 9 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 9 0
0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 5 0 0 3 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 5 0 0 3 0 0 0 4 0
0 5 0 0 3 0 0 0 4 0
0 9 0 0 3 0 0 0 4 0
0 0 0 0 3 0 0 0 4 0
0 0 0 0 3 0 0 0 4 0
0 0 0 0 3 0 0 0 9 0
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p07 — Seed Plus Bloom (easy)

**Tags:** growth, cross, same_size

**Written rule:** If an interior nonzero seed has 0 in all four orthogonal neighboring cells, copy that seed color into those four neighbors to form a plus.

**Program:** `solve_easy_p07`

**Primitives:** `seed_plus_bloom`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
0 0 7 7 7 0 0 0
0 4 0 7 0 0 0 0
4 4 4 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 6 0 3 0 0
0 0 0 6 6 6 0 0 0
0 0 8 0 6 0 0 0 0
0 8 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 9 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
```

## medium_p01 — Largest Object Crop (medium)

**Tags:** objects, selection, crop

**Written rule:** Find the monochrome connected component with the largest area and output only its tight crop.

**Program:** `solve_medium_p01`

**Primitives:** `largest_crop`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 7 0
7 7 7
0 7 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
6 6 6
6 6 6
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 9 0 0 0
0 5 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 9 0
9 9 9
0 9 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 7 0 0 0 0 0 3 3 0 0
0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
4 4
4 4
4 4
```

## medium_p02 — Aspect Recolor (medium)

**Tags:** objects, classification, recolor

**Written rule:** Recolor each monochrome object by its bounding-box aspect class: horizontal objects become 2, vertical objects become 3, and square objects become 4.

**Program:** `solve_medium_p02`

**Primitives:** `aspect_recolor`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 8 8 0 0
0 2 2 2 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 3 3 0 0
0 2 2 2 0 0 3 3 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 7 7 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 4 4 0
0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 8 8 0 0 6 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 4 4 0 0 3 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## medium_p03 — Fill Rectangular Outlines (medium)

**Tags:** frames, geometry, fill

**Written rule:** Every monochrome rectangular outline becomes a fully filled rectangle of the same color.

**Program:** `solve_medium_p03`

**Primitives:** `rect_outline_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 5 5 5 5 0
0 2 0 0 2 0 0 5 0 0 5 0
0 2 2 2 2 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 7 7 7 7 7 0 0 0
4 4 4 4 0 0 0 0 0 0
4 0 0 4 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0
0 0 7 7 7 7 7 0 0 0
0 0 7 7 7 7 7 0 0 0
0 0 7 7 7 7 7 0 0 0
0 0 7 7 7 7 7 0 0 0
4 4 4 4 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0
```

#### Train 3 input
```text
6 6 6 6 0 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0 0
6 0 0 6 0 0 3 3 3 3 3
6 6 6 6 0 0 3 0 0 0 3
0 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 3 3 3 3 3
```

#### Train 3 output
```text
6 6 6 6 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0 0
6 6 6 6 0 0 3 3 3 3 3
6 6 6 6 0 0 3 3 3 3 3
0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 3 3 3 3 3
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 8 0 0 0 0 8 0
0 2 2 2 0 8 0 0 0 0 8 0
0 2 0 2 0 8 8 8 8 8 8 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 8 0
0 2 2 2 0 8 8 8 8 8 8 0
0 2 2 2 0 8 8 8 8 8 8 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
```

## medium_p04 — Area Gallery (medium)

**Tags:** objects, sorting, gallery

**Written rule:** Crop all monochrome objects, sort them by descending area, and concatenate the crops left-to-right with one blank separator column between consecutive crops.

**Program:** `solve_medium_p04`

**Primitives:** `area_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 4 0 0 7 7 0 2 0
4 4 4 0 7 7 0 2 2
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 8 8 8 0 0
0 0 3 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
8 8 8 0 0 5 0 0 3 3
8 8 8 0 5 5 5 0 0 3
0 0 0 0 0 5 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 2 2 0 0 0 0 0 0
0 6 0 0 0 2 2 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
2 2 0 6 0 9 0
2 2 0 6 0 9 9
0 0 0 6 0 0 0
0 0 0 6 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
4 4 0 0 7 0 0 3 3
4 4 0 7 7 7 0 0 3
4 4 0 0 0 0 0 0 0
```

## medium_p05 — Frame Seed Fill (medium)

**Tags:** frames, interiors, propagation

**Written rule:** Each hollow frame contains one interior seed of a different color. Fill that frame's entire interior with the seed color while preserving the frame border.

**Program:** `solve_medium_p05`

**Primitives:** `frame_seed_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 2 0 0 0 2 0 4 4 4 4 0
0 2 0 7 0 2 0 4 0 0 4 0
0 2 0 0 0 2 0 4 8 0 4 0
0 2 2 2 2 2 0 4 0 0 4 0
0 0 0 0 0 0 0 4 0 0 4 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 2 7 7 7 2 0 4 4 4 4 0
0 2 7 7 7 2 0 4 8 8 4 0
0 2 7 7 7 2 0 4 8 8 4 0
0 2 2 2 2 2 0 4 8 8 4 0
0 0 0 0 0 0 0 4 8 8 4 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 3 0 6 0 0 0 0 0
0 6 0 0 6 0 5 5 5 0
0 6 0 0 6 0 5 0 5 0
0 6 0 0 6 0 5 0 5 0
0 6 6 6 6 0 5 2 5 0
0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 3 3 6 0 0 0 0 0
0 6 3 3 6 0 5 5 5 0
0 6 3 3 6 0 5 2 5 0
0 6 3 3 6 0 5 2 5 0
0 6 6 6 6 0 5 2 5 0
0 0 0 0 0 0 5 2 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
7 7 7 7 7 0 0 0 0 0 0 0 0
7 0 0 0 7 0 0 0 3 3 3 3 3
7 0 9 0 7 0 0 0 3 0 0 0 3
7 0 0 0 7 0 0 0 3 0 4 0 3
7 7 7 7 7 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
7 7 7 7 7 0 0 0 0 0 0 0 0
7 9 9 9 7 0 0 0 3 3 3 3 3
7 9 9 9 7 0 0 0 3 4 4 4 3
7 9 9 9 7 0 0 0 3 4 4 4 3
7 7 7 7 7 0 0 0 3 4 4 4 3
0 0 0 0 0 0 0 0 3 4 4 4 3
0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 8 8 8 8 0 0 2 0 2 0
0 0 8 0 0 8 0 0 2 0 2 0
0 0 8 0 0 8 0 0 2 5 2 0
0 0 8 6 0 8 0 0 2 0 2 0
0 0 8 0 0 8 0 0 2 0 2 0
0 0 8 0 0 8 0 0 2 0 2 0
0 0 8 8 8 8 0 0 2 0 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 8 8 8 8 0 0 2 5 2 0
0 0 8 6 6 8 0 0 2 5 2 0
0 0 8 6 6 8 0 0 2 5 2 0
0 0 8 6 6 8 0 0 2 5 2 0
0 0 8 6 6 8 0 0 2 5 2 0
0 0 8 6 6 8 0 0 2 5 2 0
0 0 8 8 8 8 0 0 2 5 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p06 — Vector Clone Union (medium)

**Tags:** translation, markers, objects

**Written rule:** The two 9 markers define a translation vector from the first marker to the second. Remove the markers, keep the main object, and add a translated clone of it by that vector.

**Program:** `solve_medium_p06`

**Primitives:** `vector_clone_union`

### Train pairs

#### Train 1 input
```text
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 9 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 9 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## medium_p07 — Corner-Key Transform Crop (medium)

**Tags:** keyed_transform, crop, rotation

**Written rule:** Use the top-left key to transform the main object crop: 1=rotate 90 degrees clockwise, 2=rotate 180 degrees, 3=mirror left-right, 4=mirror top-bottom. Output only the transformed crop.

**Program:** `solve_medium_p07`

**Primitives:** `corner_key_transform_crop`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 2
2 2
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 5 5
0 5 0
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 7
7 7
0 7
```

### Test pairs

#### Test 1 input
```text
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
4 4
4 0
```

## hard_p01 — Dual-Key Frame Insert (hard)

**Tags:** selection, keyed_transform, frames

**Written rule:** The top-left key names the color of the loose object to use. The top-right key chooses its transform (1=rotate 90 degrees clockwise, 2=rotate 180 degrees, 3=mirror left-right, 4=mirror top-bottom). Insert the transformed crop centered inside the hollow frame and discard everything else.

**Program:** `solve_hard_p01`

**Primitives:** `dual_key_frame_insert`

### Train pairs

#### Train 1 input
```text
3 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 0 0 0
0 0 2 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0
0 4 0 0 0 0 8 0 0 0 8 0
0 4 4 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 8 3 0 0 8 0
0 0 0 0 0 0 8 3 3 0 8 0
0 0 0 0 0 0 8 3 0 0 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
4 0 0 0 0 0 0 0 0 0 0 0 2
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 2 2 0 0 0
0 0 4 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8
0 0 3 3 0 0 0 0 8 0 0 0 8
0 0 0 3 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 8 0 4 0 8
0 0 0 0 0 0 0 0 8 4 4 0 8
0 0 0 0 0 0 0 0 8 0 4 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
2 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 4 0 0 0
0 0 0 2 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8
0 0 5 0 0 0 8 0 0 0 8
0 5 5 5 0 0 8 0 0 0 8
0 0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 8 2 2 0 8
0 0 0 0 0 0 8 2 0 0 8
0 0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
5 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 3 3 0 0
0 0 5 5 0 0 0 0 0 3 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8
0 0 6 0 0 0 0 8 0 0 0 8
0 0 6 6 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 8 5 0 0 8
0 0 0 0 0 0 0 8 5 5 0 8
0 0 0 0 0 0 0 8 5 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p02 — Normalized Priority Overlay (hard)

**Tags:** overlay, normalization, keyed_control

**Written rule:** Ignore the top-left key cell. Crop the two remaining objects, normalize both to the same top-left origin, and overlay them. If the key is 1, the earlier top-left object wins on overlaps; if the key is 2, the later top-left object wins on overlaps.

**Program:** `solve_hard_p02`

**Primitives:** `normalize_overlay_priority`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 3
2 2
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 4 0 0 0 6 6 0 0
0 4 4 4 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
6 4 0
4 4 4
6 0 0
```

#### Train 3 input
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
7 7
7 7
```

### Test pairs

#### Test 1 input
```text
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
9 9 2
9 9 2
9 9 0
```

## hard_p03 — Key-Door Shortest Path (hard)

**Tags:** pathfinding, state, maze

**Written rule:** Find the shortest path from start 2 to goal 3, but the door 6 may be crossed only after visiting the key 5. Preserve the maze and mark traversed empty cells on the chosen path with 4.

**Program:** `solve_hard_p03`

**Primitives:** `key_door_bfs`

### Train pairs

#### Train 1 input
```text
8 8 8 8 8 8 8 8 8
8 2 0 0 6 0 0 3 8
8 8 8 0 8 0 8 8 8
8 5 0 0 8 0 0 0 8
8 0 8 8 8 8 8 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

#### Train 1 output
```text
8 8 8 8 8 8 8 8 8
8 2 4 4 6 4 4 3 8
8 8 8 4 8 0 8 8 8
8 5 4 4 8 0 0 0 8
8 0 8 8 8 8 8 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

#### Train 2 input
```text
8 8 8 8 8 8 8 8
8 2 0 6 0 0 3 8
8 0 8 8 8 0 8 8
8 0 0 5 8 0 0 8
8 8 0 0 8 8 0 8
8 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8
```

#### Train 2 output
```text
8 8 8 8 8 8 8 8
8 2 4 6 4 4 3 8
8 4 8 8 8 0 8 8
8 4 4 5 8 0 0 8
8 8 0 0 8 8 0 8
8 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8
```

#### Train 3 input
```text
8 8 8 8 8 8 8 8 8
8 2 0 0 0 6 0 3 8
8 0 8 8 0 8 0 8 8
8 0 0 8 0 8 0 0 8
8 8 0 8 5 8 8 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

#### Train 3 output
```text
8 8 8 8 8 8 8 8 8
8 2 4 4 4 6 4 3 8
8 0 8 8 4 8 0 8 8
8 0 0 8 4 8 0 0 8
8 8 0 8 5 8 8 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

### Test pairs

#### Test 1 input
```text
8 8 8 8 8 8 8 8 8 8
8 2 0 6 0 0 0 0 3 8
8 0 8 8 8 8 8 0 8 8
8 0 0 0 0 0 8 0 0 8
8 8 8 8 8 0 8 8 0 8
8 5 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

#### Test 1 output
```text
8 8 8 8 8 8 8 8 8 8
8 2 0 6 0 0 0 4 3 8
8 4 8 8 8 8 8 4 8 8
8 4 4 4 4 4 8 4 4 8
8 8 8 8 8 4 8 8 4 8
8 5 4 4 4 4 4 4 4 8
8 8 8 8 8 8 8 8 8 8
```

## hard_p04 — Contact Matrix (hard)

**Tags:** relations, objects, matrix

**Written rule:** Sort the monochrome objects by the top-left corner of their bounding boxes. Output an N x N matrix with 1 on the diagonal and 2 wherever two objects touch orthogonally by at least one edge-adjacent cell; use 0 elsewhere.

**Program:** `solve_hard_p04`

**Primitives:** `contact_matrix`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 2 3 3 0 0 0 0
0 2 2 3 3 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
1 2 0
2 1 2
0 2 1
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 5 0 6 6 0 0 0 0 0
0 5 5 6 6 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 8 8 0
0 7 0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
1 2 2 0
2 1 0 0
2 0 1 0
0 0 0 1
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0
0 2 2 3 3 0 0 0
0 2 2 3 3 0 0 0
0 0 4 4 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
1 2 2
2 1 2
2 2 1
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 5 5 0 0 0 0 0
0 2 2 5 5 0 0 0 0 0
0 7 7 6 6 0 0 0 0 0
0 7 7 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
1 2 2 0
2 1 0 2
2 0 1 2
0 2 2 1
```

## hard_p05 — Transform Script Gallery (hard)

**Tags:** keyed_transform, timeline, gallery

**Written rule:** Read the nonzero keys in the top row from left to right. Starting from the main object crop below, output a gallery containing the initial crop and then each cumulative transform state. Keys mean 1=rotate 90 degrees clockwise, 2=rotate 180 degrees, 3=mirror left-right, 4=mirror top-bottom.

**Program:** `solve_hard_p05`

**Primitives:** `transform_script_gallery`

### Train pairs

#### Train 1 input
```text
0 1 0 3 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 2 0 0 2 0 2 0 0 2 2
0 2 0 2 2 0 2 2 0 0 2
```

#### Train 2 input
```text
4 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 0 0 5 0 0 5 5 5
5 5 0 5 5 0 0 5 0
5 0 0 5 0 0 0 0 0
```

#### Train 3 input
```text
0 2 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
7 0 0 7 7 0 7 7 0 7 0
7 7 0 0 7 0 7 0 0 7 7
```

### Test pairs

#### Test 1 input
```text
0 0 1 0 0 1 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 4 0 0 4 0 0 4 4 4 0 4 4 4
4 4 4 0 4 4 0 0 4 0 0 0 4 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0
```

## hard_p06 — Symmetry Frame Match (hard)

**Tags:** symmetry, assignment, frames

**Written rule:** Match each loose object to the hollow frame whose border color encodes its reflection symmetry class: frame 2 expects a left-right symmetric crop, frame 3 expects a top-bottom symmetric crop, and frame 4 expects a crop symmetric in both directions. Center each matching object inside its frame.

**Program:** `solve_hard_p06`

**Primitives:** `symmetry_frame_match`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 2 2 2 2 2 3 3 3 3 3
0 6 6 6 0 0 0 0 2 0 0 0 2 3 0 0 0 3
0 0 0 0 0 0 0 0 2 0 0 0 2 3 0 0 0 3
0 0 0 0 0 0 0 0 2 0 0 0 2 3 0 0 0 3
0 7 0 0 0 0 0 0 2 2 2 2 2 3 3 3 3 3
0 7 7 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 7 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0 0
0 0 9 0 0 0 0 0 0 0 4 0 0 0 4 0 0 0
0 9 9 9 0 0 0 0 0 0 4 0 0 0 4 0 0 0
0 0 9 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 3 3 3 3 3
0 0 0 0 0 0 0 0 2 0 6 0 2 3 7 0 0 3
0 0 0 0 0 0 0 0 2 6 6 6 2 3 7 7 0 3
0 0 0 0 0 0 0 0 2 0 0 0 2 3 7 0 0 3
0 0 0 0 0 0 0 0 2 2 2 2 2 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 9 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 9 9 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 9 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 6 0 0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 6 6 6 0 0 0 0 2 0 0 0 2 4 4 4 4
0 0 0 0 0 0 0 0 0 2 0 0 0 2 4 0 0 4
0 0 0 0 0 0 0 0 0 2 2 2 2 2 4 0 0 4
0 7 0 0 0 0 0 0 0 3 3 3 3 3 4 0 0 4
0 7 7 0 0 0 0 0 0 3 0 0 0 3 4 4 4 4
0 7 0 0 0 9 0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 0 9 9 9 0 0 3 0 0 0 3 0 0 0 0
0 0 0 0 0 9 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 6 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 2 6 6 6 2 4 4 4 4
0 0 0 0 0 0 0 0 0 2 0 0 0 2 4 9 0 4
0 0 0 0 0 0 0 0 0 2 2 2 2 2 9 9 9 4
0 0 0 0 0 0 0 0 0 3 3 3 3 3 4 9 0 4
0 0 0 0 0 0 0 0 0 3 7 0 0 3 4 4 4 4
0 0 0 0 0 0 0 0 0 3 7 7 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 7 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 6 6 6 0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 4 3 3 3 3
0 0 0 0 0 0 0 0 4 0 0 0 4 3 0 0 3
0 0 0 7 0 0 0 0 4 4 4 4 4 3 0 0 3
0 0 0 7 7 0 0 0 2 2 2 2 2 3 0 0 3
0 0 0 7 0 0 0 0 2 0 0 0 2 3 3 3 3
0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 9 0 0 0 0 0 2 0 0 0 2 0 0 0 0
0 9 9 9 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 9 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 9 9 9 4 3 3 3 3
0 0 0 0 0 0 0 0 4 0 9 0 4 3 7 0 3
0 0 0 0 0 0 0 0 4 4 4 4 4 3 7 7 3
0 0 0 0 0 0 0 0 2 2 2 2 2 3 7 0 3
0 0 0 0 0 0 0 0 2 0 6 0 2 3 3 3 3
0 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 6 6 6 0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 3 2 2 2 2
0 7 0 0 0 0 0 0 3 0 0 0 3 2 0 0 2
0 7 7 0 0 0 0 0 3 3 3 3 3 2 0 0 2
0 7 0 0 0 0 0 0 4 4 4 4 4 2 0 0 2
0 0 0 9 0 0 0 0 4 0 0 0 4 2 2 2 2
0 0 9 9 9 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 9 0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 7 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 7 7 0 3 2 2 2 2
0 0 0 0 0 0 0 0 3 7 0 0 3 2 6 0 2
0 0 0 0 0 0 0 0 3 3 3 3 3 6 6 6 2
0 0 0 0 0 0 0 0 4 4 4 4 4 2 0 0 2
0 0 0 0 0 0 0 0 4 0 9 0 4 2 2 2 2
0 0 0 0 0 0 0 0 4 9 9 9 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 9 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p07 — Portal Checkpoint Path (hard)

**Tags:** pathfinding, portals, state

**Written rule:** Find a shortest path from start 2 to goal 3 that must visit checkpoint 5. Portal cells of the same color (6 and 7) are linked in pairs: stepping onto one teleports immediately to its partner. Preserve the maze and mark traversed empty path cells with 4.

**Program:** `solve_hard_p07`

**Primitives:** `portal_checkpoint_path`

### Train pairs

#### Train 1 input
```text
8 8 8 8 8 8 8 8 8 8
8 2 0 0 6 8 0 0 3 8
8 8 8 0 8 8 0 8 8 8
8 5 0 0 8 8 0 0 6 8
8 0 8 8 8 8 8 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

#### Train 1 output
```text
8 8 8 8 8 8 8 8 8 8
8 2 4 4 6 8 4 4 3 8
8 8 8 4 8 8 4 8 8 8
8 5 4 4 8 8 4 4 6 8
8 0 8 8 8 8 8 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

#### Train 2 input
```text
8 8 8 8 8 8 8 8 8
8 2 0 8 6 0 0 3 8
8 0 0 8 8 8 0 8 8
8 0 5 0 0 8 0 0 8
8 8 8 8 0 8 8 6 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

#### Train 2 output
```text
8 8 8 8 8 8 8 8 8
8 2 0 8 6 4 4 3 8
8 4 0 8 8 8 0 8 8
8 4 5 4 4 8 0 0 8
8 8 8 8 4 8 8 6 8
8 0 0 0 4 4 4 4 8
8 8 8 8 8 8 8 8 8
```

#### Train 3 input
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 6 8 0 0 0 3 8
8 8 8 0 8 8 0 8 8 8 8
8 0 5 0 0 8 0 0 7 0 8
8 0 8 8 0 8 8 0 8 0 8
8 0 0 0 0 0 0 0 8 7 8
8 8 8 8 8 8 8 8 8 6 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 output
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 4 4 6 8 4 4 4 3 8
8 8 8 4 8 8 4 8 8 8 8
8 0 5 4 0 8 4 4 7 0 8
8 0 8 8 0 8 8 0 8 0 8
8 0 0 0 0 0 0 0 8 7 8
8 8 8 8 8 8 8 8 8 6 8
8 8 8 8 8 8 8 8 8 8 8
```

### Test pairs

#### Test 1 input
```text
8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 6 0 3 8
8 8 8 8 0 8 8 0 8 8
8 5 0 0 0 0 0 0 6 8
8 0 8 8 8 8 8 0 8 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

#### Test 1 output
```text
8 8 8 8 8 8 8 8 8 8
8 2 4 4 4 8 6 4 3 8
8 8 8 8 4 8 8 4 8 8
8 5 4 4 4 4 4 4 6 8
8 0 8 8 8 8 8 0 8 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```
