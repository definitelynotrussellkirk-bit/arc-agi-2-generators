# ARC Puzzle Bank — Sixth 21 Puzzles
This sixth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`36`–`42`) so it follows directly after the fifth bundle.
This volume leans into new routing and local-execution ideas while staying diverse overall: diagonal propagation, elbow-path connections, bounding-box abstraction, rigid-object gravity, legend-driven galleries, boolean template panels, overlay count maps, and pairwise relation matrices.
It also adds two reusable primitives — **`diag_ray_until_block`** and **`elbow_path`** — and reuses them across the bank rather than treating them as one-off tricks.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_sixth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_sixth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_sixth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_36_diagonal_rays_from_seeds` — **Trace Diagonal Rays from the Seeds**
- `easy_37_replace_components_by_bboxes` — **Replace Each Component by its Bounding Box**
- `easy_38_keep_bottommost_component` — **Keep Only the Bottommost Component**
- `easy_39_crop_tallest_component` — **Crop the Tallest Component**
- `easy_40_fill_between_vertical_markers` — **Fill Between the Vertical Marker Pairs**
- `easy_41_stamp_x_at_markers` — **Stamp X Shapes at the Markers**
- `easy_42_component_colors_by_top_order` — **Read Off the Component Colors from Top to Bottom**

### Medium (7)
- `medium_36_perimeter_sorted_gallery` — **Sort the Components by Perimeter and Pack Them**
- `medium_37_elbow_connect_pairs` — **Connect Each Pair with an Elbow Path**
- `medium_38_legend_ordered_component_gallery` — **Use the Legend to Order the Component Gallery**
- `medium_39_fill_tallest_ring_with_key` — **Fill the Tallest Ring with the Key Color**
- `medium_40_drop_whole_components` — **Drop Whole Components to the Bottom**
- `medium_41_color_equality_matrix` — **Build the Color-Equality Matrix**
- `medium_42_crop_union_of_key_components` — **Crop the Union of the Key-Colored Components**

### Hard (7)
- `hard_36_local_diagonal_rays_in_frames` — **Shoot Diagonal Rays Separately Inside Each Frame**
- `hard_37_boolean_panel_from_two_templates` — **Make a Boolean Panel from Two Templates**
- `hard_38_shifted_overlay_count_map` — **Overlay Shifted Copies from the Anchor Markers**
- `hard_39_local_object_gravity_in_frames` — **Apply Whole-Object Gravity Inside Each Frame**
- `hard_40_shape_color_relation_matrix` — **Build the Shape-and-Color Relation Matrix**
- `hard_41_legend_ordered_transformed_gallery` — **Transform the Legend-Ordered Gallery**
- `hard_42_chamber_elbow_paths` — **Solve Elbow Paths Separately in Each Chamber**

## Trace Diagonal Rays from the Seeds (`easy_36_diagonal_rays_from_seeds`)

**Difficulty:** easy

**Skills:** new primitive: diag_ray_until_block, same-size propagation, diagonal reasoning

**Scaffold notes:**
- Treat every red(2) seed as a source cell.
- Walk in the four diagonal directions instead of the cardinal ones.
- Stop before a gray(5) blocker or the grid edge, and recolor the traced cells.

**Written solution:** For each red(2) seed, send rays along all four diagonals. The rays continue through empty cells until they hit a gray(5) blocker or leave the grid. Recolor the seed and every visited diagonal cell to cyan(8), and keep gray blockers unchanged.

**Program solution (Python reference):**
```python
def solve_easy_36_diagonal_rays_from_seeds(g: Grid) -> Grid:
    out = clone(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v == 2:
                for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                    for rr,cc in ray_diag_until_block(g,(r,c),dr,dc,blockers={5},include_start=True):
                        if g[rr][cc] != 5:
                            out[rr][cc] = 8
    return out
```

**Train 1 input**
```text
0 0 5 0 0 0 0 0 0
0 0 5 5 0 0 0 2 0
0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 5 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 5 0 0 0 8 0 8
8 0 5 5 0 0 0 8 0
0 8 0 5 0 0 8 0 8
0 0 8 0 0 8 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 8 8 0 0 0 8
0 0 8 0 0 8 0 8 0
5 5 0 0 0 0 8 0 0
0 0 0 0 0 8 0 8 0
```

**Train 2 input**
```text
0 5 0 0 0 0 0 0
5 0 0 0 0 0 0 5
5 5 0 5 5 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 5 0 0 0 0 0 0
5 8 0 0 0 0 0 5
5 5 8 5 5 0 0 0
0 0 8 8 0 0 0 8
0 8 0 8 8 0 8 0
8 0 0 0 8 8 0 0
0 0 0 0 8 8 8 0
0 0 0 8 0 0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
5 0 0 0 0 5 0 0 0 0 5
0 0 5 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 8 0 0 0 0 0 0
0 5 0 0 0 8 0 0 0 0 0
5 0 0 0 0 5 8 0 0 0 5
8 0 5 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 0 8 0 8
8 0 8 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 8 0 8
0 0 0 0 5 0 0 8 5 0 0
0 0 0 0 0 0 8 0 0 0 0
```

**Train 4 input**
```text
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 8 0 0 0 8 0 8 0
0 8 8 0 8 0 8 0 0
0 0 8 8 0 8 0 8 0
0 0 8 8 5 0 0 0 8
0 8 0 0 8 0 0 0 8
8 0 0 0 5 8 0 8 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 8 5 8 0
0 0 0 0 8 0 0 0 8
```

**Test 1 input**
```text
0 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 5 0 0 0
```

**Test 1 output**
```text
0 5 0 0 0 0 0 8
0 0 5 0 0 0 8 0
0 0 0 0 0 8 0 0
8 0 0 0 8 0 0 0
0 8 0 8 0 0 0 8
0 0 8 0 0 0 8 0
0 8 0 8 0 8 0 0
8 0 0 0 8 5 0 0
0 8 0 8 0 8 0 0
0 0 8 0 0 0 8 0
0 8 0 8 5 0 0 8
```


## Replace Each Component by its Bounding Box (`easy_37_replace_components_by_bboxes`)

**Difficulty:** easy

**Skills:** object detection, bounding boxes, shape abstraction

**Scaffold notes:**
- Ignore the exact interior shape of each object.
- Find the minimal rectangle that contains each connected component.
- Draw only the rectangle border in cyan(8).

**Written solution:** Detect each connected nonzero component, compute its bounding box, and discard the original shape. On a blank grid of the same size, draw the border of each bounding box in cyan(8).

**Program solution (Python reference):**
```python
def solve_easy_37_replace_components_by_bboxes(g: Grid) -> Grid:
    out = zeros(*dims(g), 0)
    for comp in components4_any(g):
        r0,c0,r1,c1 = bbox(comp)
        draw_rect(out, r0, c0, r1-r0+1, c1-c0+1, 8, border_only=True)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0
0 0 3 3 0 0 9 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
7 7 0 0 0 1 1 1 0
0 7 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0
0 0 8 8 0 8 8 0 0
0 0 8 8 0 0 0 0 0
0 0 8 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0
8 8 0 0 0 8 8 8 0
8 8 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 1 0 0
0 0 9 0 0 0 0 0 1 1 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 8 8 0
0 0 8 8 0 0 0 0 8 8 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6
0 0 0 0 0 0 6 6
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 2 2 2 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8
0 0 0 0 0 0 8 8
0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
0 0 0 8 0 8 0 0
0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 2 0
4 4 4 0 0 0 0 2 0 0
4 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 1 1 1
0 0 0 3 3 0 0 1 0 1
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 8 8 0
8 8 8 0 0 0 0 8 8 0
8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 8 8 8
0 0 0 8 8 0 0 8 8 8
0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 3 3 0
0 0 0 0 0 0 3 3
0 0 0 0 9 0 0 0
0 0 0 9 9 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0
0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 8 8 8
0 0 0 0 0 8 8 8
0 0 0 8 8 0 0 0
0 0 0 8 8 0 0 0
0 0 0 8 8 0 0 0
0 0 0 0 8 8 0 0
0 0 0 0 8 8 0 0
0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## Keep Only the Bottommost Component (`easy_38_keep_bottommost_component`)

**Difficulty:** easy

**Skills:** component selection, spatial ranking, same-size filtering

**Scaffold notes:**
- Compare components by how low they reach in the grid.
- The winning object is the one with the greatest bottom row.
- Erase everything else and keep only that component.

**Written solution:** Find all connected components and compare the bottom row of their bounding boxes. Keep only the component that extends lowest in the grid, preserving its color and shape, and replace everything else with background.

**Program solution (Python reference):**
```python
def solve_easy_38_keep_bottommost_component(g: Grid) -> Grid:
    comps = components4_any(g)
    best = max(comps, key=lambda comp: (bbox(comp)[2], bbox(comp)[0], -bbox(comp)[1]))
    out = zeros(*dims(g),0)
    for r,c in best:
        out[r][c] = g[r][c]
    return out
```

**Train 1 input**
```text
0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0
0 0 0 7 7 0 0 4
0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 9 9 9 0 0 0
0 0 0 9 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 9 9 9 0 0 0
0 0 0 9 0 0 0 0
```

**Train 4 input**
```text
0 4 4 0 0 9 9 9
0 0 4 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 3 3 3 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 3 3 3 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0
0 4 4 0 0 0 8 8
0 0 0 0 0 0 0 8
0 0 0 9 9 0 0 8
0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0
0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## Crop the Tallest Component (`easy_39_crop_tallest_component`)

**Difficulty:** easy

**Skills:** bbox height comparison, component selection, size-changing crop

**Scaffold notes:**
- Measure the height of each component’s bounding box.
- Select the component with the greatest height.
- Output only its tight crop.

**Written solution:** Compute the bounding-box height of each connected component. Select the tallest one and output its tight bounding-box crop, preserving the original colors and shape.

**Program solution (Python reference):**
```python
def solve_easy_39_crop_tallest_component(g: Grid) -> Grid:
    comps = components4_any(g)
    best = max(comps, key=lambda comp: ((bbox(comp)[2]-bbox(comp)[0]+1), len(comp), -bbox(comp)[1]))
    return crop_bbox(g, bbox(best))
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 3 3 3 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 8
0 8
8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 4 0
0 0 0 2 2 2 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7
7 7
7 7
```

**Train 3 input**
```text
0 0 4 0 0 0 0 3 0 0 0 0
0 0 4 4 4 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 0
3 3 3
3 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 6 6 6 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
1 1
0 1
0 1
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
```

**Test 1 output**
```text
0 1 0
1 1 1
0 1 0
```


## Fill Between the Vertical Marker Pairs (`easy_40_fill_between_vertical_markers`)

**Difficulty:** easy

**Skills:** column-wise reasoning, segment fill, color-preserving propagation

**Scaffold notes:**
- Look down each column independently.
- Whenever a color appears exactly twice in the same column, those two cells are endpoints.
- Fill the full vertical segment between them with that color.

**Written solution:** Process the grid one column at a time. If a color appears exactly twice in a column, treat those two cells as endpoints and fill the entire vertical segment between them, inclusive, with that same color.

**Program solution (Python reference):**
```python
def solve_easy_40_fill_between_vertical_markers(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for c in range(w):
        by_color = defaultdict(list)
        for r in range(h):
            if g[r][c] != 0:
                by_color[g[r][c]].append(r)
        for color, rows in by_color.items():
            if len(rows) == 2:
                r0,r1 = min(rows), max(rows)
                for r in range(r0, r1+1):
                    out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 9 0
3 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
3 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 9 0
3 0 0 0 0 0 4 9 0
3 0 0 0 0 0 0 9 0
3 0 0 7 0 0 0 9 0
0 0 0 7 0 0 0 9 0
0 0 0 7 0 0 0 9 0
0 0 0 7 0 0 0 9 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 1
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 1
0 0 8 0 0 7 0 0
0 2 0 0 0 7 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 0 8 0 0 0 0 1
0 2 8 0 0 0 0 1
0 2 8 0 0 0 0 1
0 2 8 0 0 7 0 0
0 2 0 0 0 7 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0 0 2
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 8 0 0 2
0 0 0 4 0 0 0 8 0 0 2
0 0 0 4 0 0 0 0 0 0 2
0 0 0 4 0 0 0 0 0 0 2
0 0 0 4 0 0 0 0 0 0 2
0 0 0 4 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0
6 0 0 0 0 2 0 0
6 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
8 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 0 9 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 3 0 0
0 0 0 0 4 0 3 0 0
0 0 0 0 4 0 3 0 0
8 0 9 0 0 0 3 0 0
8 0 9 0 0 0 3 0 0
8 0 9 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```


## Stamp X Shapes at the Markers (`easy_41_stamp_x_at_markers`)

**Difficulty:** easy

**Skills:** marker expansion, local stencil, same-size drawing

**Scaffold notes:**
- Each blue(1) marker becomes the center of a local stencil.
- The stencil is an X, not a plus: center plus four diagonal neighbors.
- Draw the result in orange(7) on a blank grid.

**Written solution:** Treat each blue(1) marker as the center of a 3×3 X pattern. On a blank output grid of the same size, color the center and the four diagonal neighbors orange(7).

**Program solution (Python reference):**
```python
def solve_easy_41_stamp_x_at_markers(g: Grid) -> Grid:
    out = zeros(*dims(g),0)
    h,w = dims(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v == 1:
                for dr,dc in ((0,0),(1,1),(1,-1),(-1,1),(-1,-1)):
                    rr,cc = r+dr, c+dc
                    if 0 <= rr < h and 0 <= cc < w:
                        out[rr][cc] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 0 7 0 0 0 0 0 0
0 7 0 0 0 7 0 7 0
7 0 7 0 0 0 7 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 7 0 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 7 0 7
0 0 0 0 0 0 7 0 0 7 0
0 0 0 0 0 7 0 7 7 0 7
7 0 7 7 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0 0
7 0 7 7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0
0 0 0 0 0 7 0 0
0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0
0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 7 0 7
0 0 0 0 0 0 7 0
0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7
0 7 0 7 0 0 7 0
0 0 7 0 0 7 0 7
0 7 0 7 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 7 0 7 0 0
```


## Read Off the Component Colors from Top to Bottom (`easy_42_component_colors_by_top_order`)

**Difficulty:** easy

**Skills:** component ordering, symbolic summary output, size change

**Scaffold notes:**
- Sort the components by the top edge of their bounding boxes.
- Break ties left to right.
- Write one row whose entries are the component colors in that order.

**Written solution:** Find all connected components, sort them by the top row of their bounding boxes (breaking ties by left position), and output a single row listing their colors in that order.

**Program solution (Python reference):**
```python
def solve_easy_42_component_colors_by_top_order(g: Grid) -> Grid:
    comps = components4_any(g)
    ordered = sorted(comps, key=lambda comp: (bbox(comp)[0], bbox(comp)[1]))
    colors = [g[comp[0][0]][comp[0][1]] for comp in ordered]
    return [colors]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 3 3 0
0 0 0 0 0 0 3 3 0 0
0 6 0 0 0 0 0 0 0 0
6 6 6 0 0 4 0 0 0 0
0 6 0 0 0 4 0 2 2 2
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 3 6 4 2
```

**Train 2 input**
```text
0 9 9 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0
0 9 0 0 0 0 7 7 0
0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 2 2 0 0 0
```

**Train 2 output**
```text
9 7 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 8 2
```

**Train 4 input**
```text
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 0 2 2 2 0
0 9 0 0 0 0 6 0 0 0 0 0
9 9 9 0 8 0 0 0 0 0 0 0
0 9 0 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 2 9 8 1
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 6 6 0 0 0
```

**Test 1 output**
```text
4 8 6
```


## Sort the Components by Perimeter and Pack Them (`medium_36_perimeter_sorted_gallery`)

**Difficulty:** medium

**Skills:** component perimeter, ranking, gallery packing

**Scaffold notes:**
- Treat each component as a separate object and measure its edge perimeter.
- Sort objects from largest perimeter to smallest.
- Tightly crop them and pack the crops left to right with a one-column gap.

**Written solution:** Compute the 4-neighbor perimeter of each connected component. Sort the components by perimeter in descending order, crop each one to its bounding box, and pack the crops left to right with a one-cell separator.

**Program solution (Python reference):**
```python
def solve_medium_36_perimeter_sorted_gallery(g: Grid) -> Grid:
    comps = components4_any(g)
    decorated = []
    for comp in comps:
        crop = crop_bbox(g, bbox(comp))
        decorated.append((component_perimeter(set(comp)), bbox(comp)[0], bbox(comp)[1], crop))
    decorated.sort(key=lambda x: (-x[0], x[1], x[2]))
    crops = [crop for _,_,_,crop in decorated]
    return gallery_h(crops, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 8 8 8 0 4 4 4 0 0 0 0 0
0 0 0 8 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 4 0 8 8 8 0 9 9
4 4 4 0 0 0 8 0 9 9
0 0 4 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8 0 0 0 3 0 9 0
0 8 0 0 3 3 0 9 9
8 8 8 0 3 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 2 0 0 9 0 0 0
0 0 0 0 0 2 2 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 9 0 0 0 4 0 2 0
9 9 9 0 4 4 0 2 2
0 9 0 0 0 4 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0
0 7 7 0 0 0 0 0 0 1 1 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 0 0 2 0 1 0
7 0 0 2 2 0 1 1
7 7 0 2 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 6 0
0 2 0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 9 9 0 0 0 0 0 0 6 0
0 0 0 0 0 9 9 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 6 0 0 0 2 0 9 9
6 6 6 0 2 2 0 9 9
0 6 0 0 2 0 0 0 0
```


## Connect Each Pair with an Elbow Path (`medium_37_elbow_connect_pairs`)

**Difficulty:** medium

**Skills:** new primitive: elbow_path, pairing by color, orthogonal path drawing

**Scaffold notes:**
- Each nonzero color appears exactly twice.
- Connect the topmost endpoint to the other endpoint by going vertically first, then horizontally.
- Draw the whole L-shaped path in the same color.

**Written solution:** Group the singleton markers by color. For each pair, take the topmost marker as the start, draw a vertical segment to the target row, then a horizontal segment to the other marker. The output is the union of all such elbow paths.

**Program solution (Python reference):**
```python
def solve_medium_37_elbow_connect_pairs(g: Grid) -> Grid:
    out = zeros(*dims(g),0)
    pos = defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v != 0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        assert len(cells)==2
        a,b = sorted(cells)
        # start topmost; if same row sorted by left
        for rr,cc in elbow_path(a,b,prefer='vertical_first'):
            out[rr][cc] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 8 0 0 0 0 0 0 0 0 0 4
0 0 8 0 0 0 0 0 0 0 0 0 4
0 0 8 0 0 0 0 0 0 0 0 0 4
0 0 8 0 0 0 0 0 0 0 0 0 4
0 0 8 8 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 4 4 4 4 4 4 4 4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
6 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## Use the Legend to Order the Component Gallery (`medium_38_legend_ordered_component_gallery`)

**Difficulty:** medium

**Skills:** external key row, component lookup by color, gallery packing

**Scaffold notes:**
- Read the nonzero colors in the top legend row from left to right.
- Find the component of each legend color in the body of the grid.
- Crop those components and pack them left to right in legend order.

**Written solution:** Interpret the top row as a legend specifying an order of colors. In the body of the puzzle, find the unique component for each legend color, crop it to its bounding box, and pack the resulting crops left to right in that legend order.

**Program solution (Python reference):**
```python
def solve_medium_38_legend_ordered_component_gallery(g: Grid) -> Grid:
    legend = [v for v in g[0] if v != 0]
    body = [row[:] for row in g[2:]]
    # find components by color
    comps_by_color = {}
    for color in set(legend):
        comps = components4_color(body, color)
        assert len(comps)==1, (color, len(comps))
        crop = crop_bbox(body, bbox(comps[0]))
        comps_by_color[color] = crop
    return gallery_h([comps_by_color[color] for color in legend], sep=1)
```

**Train 1 input**
```text
9 2 4 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 9 0 0 0 0 0 0 0 0 2 2 2 0 0 0
0 9 9 0 0 0 0 0 0 0 0 2 0 0 0 0
```

**Train 1 output**
```text
9 0 0 0 2 0 0 0 4 0 1 1
9 0 0 2 2 2 0 0 4 0 1 1
9 9 0 0 2 0 0 4 4 0 0 0
```

**Train 2 input**
```text
6 9 0 7 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 6 0 0
0 0 0 0 0 7 0 0 6 6 0 0
0 0 0 0 0 7 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 2 2 0
9 9 9 0 0 0 0 0 0 0 2 2
0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 9 0 0 7 0 2 2 0
6 6 0 9 9 9 0 7 0 0 2 2
6 0 0 0 9 0 0 7 0 0 0 0
```

**Train 3 input**
```text
1 0 7 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 7 7 0 0 0 0 2 0 0 0 0
0 0 0 7 7 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 1 0 7 7 0 0 2
1 1 0 7 7 0 0 2
0 0 0 0 0 0 2 2
```

**Train 4 input**
```text
7 0 9 0 1 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 2 2 2 0
0 0 0 0 0 0 0 0 9 0 2 0 0 0
```

**Train 4 output**
```text
0 7 7 0 9 0 1 1 1 0 2 2 2
7 7 0 0 9 0 0 1 0 0 2 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
9 0 7 0 6 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 9 0 0 7
0 0 0 0 0 0 0 0 9 9 0 7
0 0 0 0 0 0 0 0 9 0 0 7
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
9 0 0 7 0 6 0 3 3 3
9 9 0 7 0 6 0 0 0 0
9 0 0 7 0 6 0 0 0 0
```


## Fill the Tallest Ring with the Key Color (`medium_39_fill_tallest_ring_with_key`)

**Difficulty:** medium

**Skills:** ring detection, height-based selection, keyed recolor

**Scaffold notes:**
- Identify the hollow rectangular rings and ignore the singleton key marker.
- Choose the ring with the greatest height.
- Crop that ring and fill its interior with the key marker’s color.

**Written solution:** Among the hollow rectangular border objects, select the one with the greatest height. Output its tight crop, preserving the border color, but fill the rectangular interior with the color of the singleton key cell.

**Program solution (Python reference):**
```python
def solve_medium_39_fill_tallest_ring_with_key(g: Grid) -> Grid:
    comps = components4_any(g)
    ring_comps = []
    key_color = None
    for comp in comps:
        r0,c0,r1,c1 = bbox(comp)
        expected = set(rect_border_cells(r0,c0,r1-r0+1,c1-c0+1))
        if len(comp) == 1:
            # possible key singleton
            key_color = g[comp[0][0]][comp[0][1]]
        elif set(comp) == expected and r1-r0+1 >= 3 and c1-c0+1 >= 3:
            ring_comps.append(comp)
    assert key_color is not None
    best = max(ring_comps, key=lambda comp: ((bbox(comp)[2]-bbox(comp)[0]+1), len(comp), bbox(comp)[1]))
    box = bbox(best)
    out = crop_bbox(g, box)
    # fill interior with key color, preserve border colors
    h,w = dims(out)
    for r in range(1,h-1):
        for c in range(1,w-1):
            out[r][c] = key_color
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 3 3 3 3 0 0 0 8 0 0 0 8 0
0 0 0 0 3 0 0 3 0 0 0 8 8 8 8 8 0
0 0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 3 0 6 6 6 6 6 0 0 0
0 0 0 0 3 3 3 3 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 3 3
3 2 2 3
3 2 2 3
3 2 2 3
3 3 3 3
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 9 9 9 9 9 9 0
0 0 2 2 2 2 2 2 0 9 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 2 2 2 2
2 6 6 6 6 2
2 6 6 6 6 2
2 2 2 2 2 2
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0 1 0 0 0 0
0 0 0 0 1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 7 0 0 7 0 0 0 0 0
0 0 0 0 0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 1 1 1 1 1
1 3 3 3 3 1
1 3 3 3 3 1
1 1 1 1 1 1
```

**Train 4 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 3 0 0 0 7 7 7 7
0 0 0 3 0 0 0 0 3 0 0 0 7 0 0 7
0 0 0 3 0 0 0 0 3 0 0 0 7 0 0 7
0 0 0 3 3 3 3 3 3 0 0 0 7 7 7 7
```

**Train 4 output**
```text
3 3 3 3 3 3
3 4 4 4 4 3
3 4 4 4 4 3
3 4 4 4 4 3
3 3 3 3 3 3
```

**Test 1 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 0 0 2 2 2 2 0 0
9 0 0 0 0 9 0 0 2 0 0 2 0 0
9 9 9 9 9 9 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 2 2
2 7 7 2
2 7 7 2
2 7 7 2
2 2 2 2
```


## Drop Whole Components to the Bottom (`medium_40_drop_whole_components`)

**Difficulty:** medium

**Skills:** object-level gravity, collision handling, same-size transform

**Scaffold notes:**
- Treat each connected component as a rigid object, not as independent cells.
- Every object falls straight down as far as possible.
- Objects stop when they reach the floor or a previously settled object.

**Written solution:** Apply gravity to each connected component as a whole rigid object. Components move straight downward without changing shape or horizontal position, and they stop when they would collide with the floor or another settled component.

**Program solution (Python reference):**
```python
def solve_medium_40_drop_whole_components(g: Grid) -> Grid:
    comps = components4_any(g)
    # preserve each component's colors
    info = []
    for comp in comps:
        color_map = {(r,c): g[r][c] for r,c in comp}
        box = bbox(comp)
        info.append((box[2], box[0], box[1], comp, color_map))
    info.sort(key=lambda x: (-x[0], x[1], x[2]))  # bottommost first
    h,w = dims(g)
    out = zeros(h,w,0)
    for _,_,_,comp,color_map in info:
        shift = 0
        while True:
            ok = True
            for r,c in comp:
                nr = r + shift + 1
                if nr >= h or out[nr][c] != 0:
                    ok = False
                    break
            if ok:
                shift += 1
            else:
                break
        for r,c in comp:
            out[r+shift][c] = color_map[(r,c)]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 9 9 9 0 0 6 0 0 0
1 0 0 0 9 0 0 6 6 6 0 0
1 1 0 0 0 0 0 0 6 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 9 0 0 0 6 0 0 0
1 1 0 9 9 9 0 6 6 6 0 0
0 1 0 0 9 0 0 0 6 0 0 0
```

**Train 2 input**
```text
0 0 0 0 8 8 0 0 0 0 0 0
0 4 4 0 0 8 0 0 1 0 0 0
0 4 4 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 1 0 0 0
0 0 9 0 8 8 0 1 1 1 0 0
0 0 9 9 0 8 0 0 1 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 2 2 0 0 0 0 0
0 0 4 4 0 0 2 2 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 6 0 0 0 0
0 0 0 0 7 7 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 7 0 2 2 6 0 0 0 0
0 0 4 4 7 7 2 2 6 6 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 8 8 8
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 8 8 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
7 7 7 0 4 0 0 0 9 0 0
0 0 0 0 4 4 0 0 9 0 0
0 0 0 0 0 4 0 0 9 9 0
0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 1 0 4 0 0 0 9 0 0
0 0 1 1 4 4 0 0 9 0 0
0 0 0 1 0 4 0 0 9 9 0
```


## Build the Color-Equality Matrix (`medium_41_color_equality_matrix`)

**Difficulty:** medium

**Skills:** legend comparison, matrix construction, symbolic abstraction

**Scaffold notes:**
- The first row and first column are legends.
- Compare every row-legend color with every column-legend color.
- Write the shared color at matches and 0 elsewhere.

**Written solution:** Read the colors on the top legend row and the left legend column. Produce the comparison matrix whose cell is that color when the row color and column color are equal, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_medium_41_color_equality_matrix(g: Grid) -> Grid:
    top = [v for v in g[0][1:] if v != 0 or True]  # allow zeros? legends will be nonzero
    left = [g[r][0] for r in range(1,len(g))]
    return [[rowc if rowc == colc else 0 for colc in top] for rowc in left]
```

**Train 1 input**
```text
5 8 8 1 3
6 0 0 0 0
8 0 0 0 0
3 0 0 0 0
2 0 0 0 0
8 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0
8 8 0 0
0 0 0 3
0 0 0 0
8 8 0 0
```

**Train 2 input**
```text
5 9 4 3
7 0 0 0
3 0 0 0
6 0 0 0
4 0 0 0
```

**Train 2 output**
```text
0 0 0
0 0 3
0 0 0
0 4 0
```

**Train 3 input**
```text
5 6 3 4
8 0 0 0
9 0 0 0
9 0 0 0
1 0 0 0
8 0 0 0
```

**Train 3 output**
```text
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

**Train 4 input**
```text
5 2 1 7 2 8
3 0 0 0 0 0
8 0 0 0 0 0
9 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0
0 0 0 0 8
0 0 0 0 0
```

**Test 1 input**
```text
5 6 3 3 4
1 0 0 0 0
6 0 0 0 0
1 0 0 0 0
3 0 0 0 0
6 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0
6 0 0 0
0 0 0 0
0 3 3 0
6 0 0 0
```


## Crop the Union of the Key-Colored Components (`medium_42_crop_union_of_key_components`)

**Difficulty:** medium

**Skills:** selection by top-row keys, multi-object crop, relative-position preservation

**Scaffold notes:**
- The top row names the two target colors.
- Find those two components in the body of the grid.
- Keep both, preserve their relative positions, and output the tight crop around their union.

**Written solution:** Use the two nonzero cells in the top row as color keys. In the body of the puzzle, select the unique component of each key color, keep both components together, and output the tight bounding-box crop of their union.

**Program solution (Python reference):**
```python
def solve_medium_42_crop_union_of_key_components(g: Grid) -> Grid:
    keys = [v for v in g[0] if v != 0][:2]
    body = [row[:] for row in g[2:]]
    selected_cells = []
    for color in keys:
        comps = components4_color(body, color)
        assert len(comps)==1
        selected_cells.extend(comps[0])
    return crop_bbox(body, bbox(selected_cells))
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 7 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 7 7 0 8 8 0
0 0 0 1 0 0 0 0 7 7 0 0 8 0
0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 8 0
7 7 0 8 8
7 7 0 0 8
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0 0 0 0 0 0
4 4 4 0 0 1 1 0 0 0 0 0 0 0
0 4 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 0 0 0 0 1 0 0 0 0 0 0 0
4 4 4 0 0 1 1 0 0 0 0 0 0 0
0 4 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2
```

**Train 3 input**
```text
0 0 0 0 0 0 1 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 9 0
0 3 0 0 0 0 0 0 1 0 0 9 9 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8 8 0 0 0 0 0 1
0 0 0 0 0 0 0 0 1 1
0 3 0 0 0 0 0 0 1 0
3 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 6 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 9 0 0 0
6 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 7
```

**Train 4 output**
```text
6 6 0 0 0 0 0 9 0 0 0
6 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 7
```

**Test 1 input**
```text
0 0 4 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 4 0 0 0 2 0 0 0 0
0 0 0 4 4 4 0 0 2 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 6 6
```

**Test 1 output**
```text
0 0 3 0
0 3 3 3
0 0 0 0
0 4 0 0
4 4 4 0
0 4 0 0
```


## Shoot Diagonal Rays Separately Inside Each Frame (`hard_36_local_diagonal_rays_in_frames`)

**Difficulty:** hard

**Skills:** local reasoning in subgrids, diagonal propagation, frame-bounded execution

**Scaffold notes:**
- Solve each rectangular frame independently.
- Inside a frame, red seeds send diagonal rays but they cannot cross the frame border or a blocker.
- Recolor only the traversed cells inside each local chamber.

**Written solution:** Detect each gray(5) rectangular frame and treat its interior as a separate subproblem. Inside each frame, every red(2) seed sends rays along the four diagonals, stopping before a blocker(6) or the frame border. Recolor the visited cells cyan(8) while leaving the frame and blockers intact.

**Program solution (Python reference):**
```python
def solve_hard_36_local_diagonal_rays_in_frames(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        ir0, ic0, ir1, ic1 = inside(box)
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                if g[r][c] == 2:
                    for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                        for rr,cc in ray_diag_until_block(g, (r,c), dr, dc, blockers={5,6}, include_start=True, bounds=(ir0,ic0,ir1,ic1)):
                            if g[rr][cc] != 6:
                                out[rr][cc] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5
0 5 0 0 2 6 5 0 5 0 6 6 0 5
0 5 0 6 0 2 5 0 5 0 0 0 2 5
0 5 0 0 0 0 5 0 5 0 0 6 0 5
0 5 5 5 5 5 5 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5
0 5 0 0 8 6 5 0 5 0 6 6 0 5
0 5 0 6 0 8 5 0 5 0 0 0 8 5
0 5 0 0 8 0 5 0 5 0 0 6 0 5
0 5 5 5 5 5 5 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 6 0 2 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 6 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 6 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 5 2 0 2 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 6 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 8 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 6 0 8 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 6 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 6 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 5 8 0 8 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 8 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 8 6 8 5 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 5 0 2 0 6 5
0 0 0 0 0 0 0 0 5 0 0 0 6 5
0 5 5 5 5 5 5 0 5 0 0 0 0 5
0 5 0 0 0 0 5 0 5 0 0 6 0 5
0 5 0 0 0 2 5 0 5 5 5 5 5 5
0 5 0 0 0 0 5 0 0 0 0 0 0 0
0 5 0 6 0 0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 5 0 8 0 6 5
0 0 0 0 0 0 0 0 5 8 0 8 6 5
0 5 5 5 5 5 5 0 5 0 0 0 8 5
0 5 0 0 8 0 5 0 5 0 0 6 0 5
0 5 0 0 0 8 5 0 5 5 5 5 5 5
0 5 0 0 8 0 5 0 0 0 0 0 0 0
0 5 0 6 0 0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0 0
0 0 5 0 2 0 0 5 0 0 5 0 0 2 0 5 0 0
0 0 5 6 0 0 0 5 0 0 5 0 6 0 0 5 0 0
0 0 5 0 6 0 6 5 0 0 5 6 0 0 2 5 0 0
0 0 5 0 0 0 0 5 0 0 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0 0
0 0 5 0 8 0 0 5 0 0 5 0 8 8 0 5 0 0
0 0 5 6 0 8 0 5 0 0 5 0 6 8 8 5 0 0
0 0 5 0 6 0 6 5 0 0 5 6 0 0 8 5 0 0
0 0 5 0 0 0 0 5 0 0 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
5 5 5 5 5 5 0 5 5 5 5 5 0 0 0
5 0 0 0 6 5 0 5 2 0 0 5 0 0 0
5 0 0 0 0 5 0 5 0 2 6 5 0 0 0
5 2 0 0 2 5 0 5 0 6 0 5 0 0 0
5 0 0 0 0 5 0 5 0 6 0 5 0 0 0
5 5 5 5 5 5 0 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 6 6 0 5 0 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0 0 0 0 0 0 0
0 0 5 0 6 2 5 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 5 5 5 5 0 5 5 5 5 5 0 0 0
5 0 8 8 6 5 0 5 8 0 8 5 0 0 0
5 0 8 8 0 5 0 5 0 8 6 5 0 0 0
5 8 0 0 8 5 0 5 8 6 8 5 0 0 0
5 0 8 8 0 5 0 5 0 6 0 5 0 0 0
5 5 5 5 5 5 0 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 5 6 6 0 5 0 0 0 0 0 0 0 0
0 0 5 0 8 0 5 0 0 0 0 0 0 0 0
0 0 5 0 6 8 5 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
```


## Make a Boolean Panel from Two Templates (`hard_37_boolean_panel_from_two_templates`)

**Difficulty:** hard

**Skills:** panel extraction, boolean composition, multi-output gallery

**Scaffold notes:**
- The two framed interiors contain binary templates A and B.
- The top row lists operations: union, intersection, xor.
- Compute each requested boolean combination and pack the results as a strip.

**Written solution:** Read the operation keys on the top row. Extract the two framed templates below, align them cellwise, and for each key compute either the union, intersection, or xor of their occupied cells. Output the requested results as a left-to-right gallery.

**Program solution (Python reference):**
```python
def solve_hard_37_boolean_panel_from_two_templates(g: Grid) -> Grid:
    keys = [v for v in g[0] if v != 0]
    frames = frame_boxes_from_color(g, 5)
    assert len(frames) == 2
    # left frame is A, right frame is B
    frames = sorted(frames, key=lambda b: b[1])
    def interior_pattern(box, color):
        r0,c0,r1,c1 = inside(box)
        pat = zeros(r1-r0+1, c1-c0+1, 0)
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if g[r][c] == color:
                    pat[r-r0][c-c0] = 1
        return pat
    A = interior_pattern(frames[0], 2)
    B = interior_pattern(frames[1], 3)
    assert dims(A) == dims(B)
    h,w = dims(A)
    def op_grid(key):
        out = zeros(h,w,0)
        for r in range(h):
            for c in range(w):
                a = A[r][c] == 1
                b = B[r][c] == 1
                on = False
                if key == 2:
                    on = a or b
                elif key == 3:
                    on = a and b
                elif key == 4:
                    on = (a != b)
                else:
                    raise ValueError(key)
                if on:
                    out[r][c] = 8
        return out
    return gallery_h([op_grid(k) for k in keys], sep=1)
```

**Train 1 input**
```text
4 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 5 5 5 5 5 5 0 0
5 0 0 0 0 5 0 5 0 0 0 3 5 0 0
5 2 0 0 0 5 0 5 0 3 3 3 5 0 0
5 2 2 2 0 5 0 5 0 0 3 3 5 0 0
5 2 2 2 0 5 0 5 0 0 3 3 5 0 0
5 2 2 0 0 5 0 5 0 0 3 3 5 0 0
5 5 5 5 5 5 0 5 5 5 5 5 5 0 0
```

**Train 1 output**
```text
0 0 0 8 0 0 0 0 0
8 8 8 8 0 0 0 0 0
8 8 0 8 0 0 0 8 0
8 8 0 8 0 0 0 8 0
8 8 8 8 0 0 0 0 0
```

**Train 2 input**
```text
3 4 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 5 5 5 5 5 5 0 0
5 2 2 0 0 5 0 5 3 3 3 0 5 0 0
5 2 2 2 0 5 0 5 3 3 3 0 5 0 0
5 2 2 0 0 5 0 5 3 3 3 0 5 0 0
5 0 0 0 0 5 0 5 0 0 0 0 5 0 0
5 0 0 0 0 5 0 5 0 0 0 0 5 0 0
5 5 5 5 5 5 0 5 5 5 5 5 5 0 0
```

**Train 2 output**
```text
8 8 0 0 0 0 0 8 0 0 8 8 8 0
8 8 8 0 0 0 0 0 0 0 8 8 8 0
8 8 0 0 0 0 0 8 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 0 4 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 0 0
5 0 0 0 2 0 5 0 5 3 3 3 3 3 5 0 0
5 0 0 0 2 2 5 0 5 3 3 3 0 3 5 0 0
5 0 0 0 2 2 5 0 5 0 3 3 0 0 5 0 0
5 0 0 0 2 2 5 0 5 0 0 0 0 0 5 0 0
5 0 0 0 2 2 5 0 5 0 0 0 0 0 5 0 0
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 0 0
```

**Train 3 output**
```text
8 8 8 8 8 0 8 8 8 0 8 0 0 0 0 8 0
8 8 8 8 8 0 8 8 8 8 0 0 0 0 0 0 8
0 8 8 8 8 0 0 8 8 8 8 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 8 8 0 0 0 0 0 0
```

**Train 4 input**
```text
4 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 5 0 0
5 0 2 2 2 2 0 5 0 5 0 0 3 3 3 0 5 0 0
5 2 2 2 2 2 0 5 0 5 0 0 0 3 3 3 5 0 0
5 0 2 0 2 2 0 5 0 5 0 0 0 0 0 0 5 0 0
5 0 0 0 0 0 0 5 0 5 0 0 0 0 0 0 5 0 0
5 0 0 0 0 0 0 5 0 5 0 0 0 0 0 0 5 0 0
5 5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 5 0 0
```

**Train 4 output**
```text
0 8 0 0 0 0 0 0 0 8 8 8 0 0 0 8 8 8 8 0
8 8 8 0 0 8 0 0 0 0 8 8 0 0 8 8 8 8 8 8
0 8 0 8 8 0 0 0 0 0 0 0 0 0 0 8 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
2 4 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 5 0 0
5 0 0 2 2 2 2 5 0 5 0 0 0 0 0 0 5 0 0
5 0 0 0 2 2 0 5 0 5 0 0 0 0 0 0 5 0 0
5 0 0 2 2 0 0 5 0 5 0 0 0 0 0 0 5 0 0
5 0 0 0 0 0 0 5 0 5 0 0 3 3 3 0 5 0 0
5 0 0 0 0 0 0 5 0 5 0 0 3 3 3 0 5 0 0
5 5 5 5 5 5 5 5 0 5 5 5 5 5 5 5 5 0 0
```

**Test 1 output**
```text
0 0 8 8 8 8 0 0 0 8 8 8 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 8 8 8 0 0 0 0 0 0 0 0
```


## Overlay Shifted Copies from the Anchor Markers (`hard_38_shifted_overlay_count_map`)

**Difficulty:** hard

**Skills:** template extraction with anchor, translation by markers, count-map rendering

**Scaffold notes:**
- The multi-cell object containing 9 is the template, and its 9-cell is the anchor.
- Every other singleton 9 marks a place where the anchor should move.
- Overlay all translated copies and convert coverage counts into colors.

**Written solution:** Find the connected template object that contains the anchor color 9. For every other singleton 9 in the grid, translate a copy of the template so that the template’s anchor lands on that marker. Count how many translated copies cover each cell and render the count map using 2 for one copy, 3 for two copies, and 4 for three or more.

**Program solution (Python reference):**
```python
def solve_hard_38_shifted_overlay_count_map(g: Grid) -> Grid:
    comps = components4_any(g)
    template_comp = None
    markers = []
    for comp in comps:
        vals = {g[r][c] for r,c in comp}
        if 9 in vals and len(comp) > 1:
            template_comp = comp
        elif len(comp) == 1 and g[comp[0][0]][comp[0][1]] == 9:
            markers.append(comp[0])
    assert template_comp is not None
    # occupancy offsets and anchor
    tr0, tc0, tr1, tc1 = bbox(template_comp)
    occup = []
    anchor = None
    for r,c in template_comp:
        if g[r][c] != 0:
            occup.append((r-tr0, c-tc0))
        if g[r][c] == 9:
            anchor = (r-tr0, c-tc0)
    assert anchor is not None
    h,w = dims(g)
    counts = [[0 for _ in range(w)] for _ in range(h)]
    for mr,mc in markers:
        top = mr - anchor[0]
        left = mc - anchor[1]
        for dr,dc in occup:
            rr,cc = top+dr, left+dc
            if 0 <= rr < h and 0 <= cc < w:
                counts[rr][cc] += 1
    out = zeros(h,w,0)
    for r in range(h):
        for c in range(w):
            if counts[r][c] == 1:
                out[r][c] = 2
            elif counts[r][c] == 2:
                out[r][c] = 3
            elif counts[r][c] >= 3:
                out[r][c] = 4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
2 2 0 0 0 0 0 0 0 2 2 0 0
2 2 0 0 0 0 0 0 0 2 2 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
7 9 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 7 9 0 0 0 0 0 0 0
0 0 9 7 7 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 9 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 9 7 0 0 0 0 9 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Apply Whole-Object Gravity Inside Each Frame (`hard_39_local_object_gravity_in_frames`)

**Difficulty:** hard

**Skills:** local object gravity, frame decomposition, collision-aware simulation

**Scaffold notes:**
- Each gray rectangular frame defines its own local sandbox.
- Within a frame, connected components fall downward as rigid objects.
- Different frames do not interact with one another.

**Written solution:** Detect each gray frame, isolate its interior, and run the rigid-body gravity rule independently inside that local region. Every component falls straight down within its own frame until it hits the floor or another settled object, and then the solved interiors are pasted back into the original grid.

**Program solution (Python reference):**
```python
def solve_hard_39_local_object_gravity_in_frames(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        ir0, ic0, ir1, ic1 = inside(box)
        sub = [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
        dropped = solve_medium_40_drop_whole_components(sub)
        # clear interior
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                out[r][c] = 0
        paste(out, dropped, ir0, ic0, 0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 5 4 4 0 0 0 5
0 5 5 5 5 5 5 5 5 0 5 4 4 0 0 0 5
0 5 4 0 0 1 0 0 5 0 5 0 0 0 0 6 5
0 5 4 0 0 1 1 0 5 0 5 0 0 7 0 6 5
0 5 4 0 0 0 1 0 5 0 5 0 7 7 0 6 5
0 5 0 0 8 0 0 0 5 0 5 5 5 5 5 5 5
0 5 0 8 8 0 0 0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 5
0 5 5 5 5 5 5 5 5 0 5 0 0 0 0 0 5
0 5 0 0 0 0 0 0 5 0 5 4 4 0 0 6 5
0 5 0 0 0 0 0 0 5 0 5 4 4 7 0 6 5
0 5 4 0 0 1 0 0 5 0 5 0 7 7 0 6 5
0 5 4 0 8 1 1 0 5 0 5 5 5 5 5 5 5
0 5 4 8 8 0 1 0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 5 0 0 0 6 5
5 0 2 2 0 0 5 0 0 5 0 0 0 6 5
5 0 0 2 2 0 5 0 0 5 9 9 0 6 5
5 0 0 0 0 0 5 0 0 5 9 9 0 0 5
5 0 0 7 7 7 5 0 0 5 0 0 0 0 5
5 0 0 0 7 0 5 0 0 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 5 0 0 0 0 5
5 0 0 0 0 0 5 0 0 5 0 0 0 0 5
5 0 2 2 0 0 5 0 0 5 0 0 0 6 5
5 0 0 2 2 0 5 0 0 5 9 9 0 6 5
5 0 0 7 7 7 5 0 0 5 9 9 0 6 5
5 0 0 0 7 0 5 0 0 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
5 0 3 0 0 0 5 0 5 5 5 5 5 5 5
5 3 3 0 0 0 5 0 5 6 0 0 3 0 5
5 3 0 0 7 0 5 0 5 6 6 0 3 0 5
5 0 0 0 7 7 5 0 5 0 0 0 3 0 5
5 0 0 0 0 7 5 0 5 0 0 0 0 0 5
5 0 0 0 0 0 5 0 5 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
5 0 0 0 0 0 5 0 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 5 0 0 0 0 0 5
5 0 0 0 0 0 5 0 5 0 0 0 3 0 5
5 0 3 0 7 0 5 0 5 6 0 0 3 0 5
5 3 3 0 7 7 5 0 5 6 6 0 3 0 5
5 3 0 0 0 7 5 0 5 5 5 5 5 5 5
5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 9 0 0 7 5 0 0 0 0 0 0 0
0 0 5 0 9 9 0 7 7 5 0 5 5 5 5 5 5
0 0 5 0 9 0 0 7 0 5 0 5 0 1 1 1 5
0 0 5 5 5 5 5 5 5 5 0 5 0 0 1 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 9 0 0 7 5 0 0 0 0 0 0 0
0 0 5 0 9 9 0 7 7 5 0 5 5 5 5 5 5
0 0 5 0 9 0 0 7 0 5 0 5 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 5 0 1 1 1 5
0 0 0 0 0 0 0 0 0 0 0 5 0 0 1 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 9 0 0 7 5 0 0 0 0 0 0 0
0 0 5 0 9 9 0 7 7 5 0 5 5 5 5 5 5
0 0 5 0 9 0 0 7 0 5 0 5 0 1 1 1 5
0 0 5 5 5 5 5 5 5 5 0 5 0 0 1 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 9 0 0 7 5 0 0 0 0 0 0 0
0 0 5 0 9 9 0 7 7 5 0 5 5 5 5 5 5
0 0 5 0 9 0 0 7 0 5 0 5 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 5 0 1 1 1 5
0 0 0 0 0 0 0 0 0 0 0 5 0 0 1 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 7 7 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Build the Shape-and-Color Relation Matrix (`hard_40_shape_color_relation_matrix`)

**Difficulty:** hard

**Skills:** pairwise comparison, shape matching under rotation, attribute matrix

**Scaffold notes:**
- Order the components top to bottom, then left to right.
- On the diagonal, write each component’s own color.
- Off the diagonal, write 8 for a shape match under rotation, 6 for same color only, and 0 otherwise.

**Written solution:** Extract the components in reading order and compare every pair. The diagonal entries carry each component’s own color. For off-diagonal cells, place 8 when the two shapes match up to rotation, 6 when they merely share the same color, and 0 when neither relation holds.

**Program solution (Python reference):**
```python
def solve_hard_40_shape_color_relation_matrix(g: Grid) -> Grid:
    comps = sorted(components4_any(g), key=lambda comp: (bbox(comp)[0], bbox(comp)[1]))
    n = len(comps)
    colors = [g[comp[0][0]][comp[0][1]] for comp in comps]
    out = zeros(n, n, 0)
    for i, comp_i in enumerate(comps):
        out[i][i] = colors[i]
        for j, comp_j in enumerate(comps):
            if i == j:
                continue
            if shape_match_under_rotation(comp_i, comp_j):
                out[i][j] = 8
            elif colors[i] == colors[j]:
                out[i][j] = 6
            else:
                out[i][j] = 0
    return out
```

**Train 1 input**
```text
0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 8 0 6
8 2 0 0
0 0 7 0
6 0 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 6 0 0 4 4 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 4 4 4
0 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 0 8 6
0 6 0 0
8 0 8 0
6 0 0 4
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 9 9 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 9 9 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0 0
0 2 8 6
0 8 9 0
0 6 0 2
```

**Train 4 input**
```text
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 3 3 0 0 0 0 0 0 0 0
0 0 9 9 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
1 6 0 8
6 1 0 0
0 0 9 0
8 0 0 3
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 4 4 4 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
4 8 6 0
8 2 0 0
6 0 4 0
0 0 0 1
```


## Transform the Legend-Ordered Gallery (`hard_41_legend_ordered_transformed_gallery`)

**Difficulty:** hard

**Skills:** shared transform key, selection by legend, gallery synthesis

**Scaffold notes:**
- The top-left key selects one transform for all chosen components.
- The rest of the top row gives the color order for the gallery.
- Extract those components, transform each one, and pack them left to right.

**Written solution:** Read the transform key in the top-left corner and the color legend across the rest of the top row. In the body of the puzzle, find the component for each legend color, crop it, apply the shared transform selected by the key, and pack the transformed crops into a gallery in legend order.

**Program solution (Python reference):**
```python
def solve_hard_41_legend_ordered_transformed_gallery(g: Grid) -> Grid:
    key = g[0][0]
    legend = [v for v in g[0][1:] if v != 0]
    body = [row[:] for row in g[2:]]
    crops = []
    for color in legend:
        comps = components4_color(body, color)
        assert len(comps) == 1
        crop = crop_bbox(body, bbox(comps[0]))
        crops.append(transform_by_key_grid(crop, key))
    return gallery_h(crops, sep=1)
```

**Train 1 input**
```text
3 7 0 4 0 9 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 7 7 7 0 8 8 0
0 0 0 0 4 4 0 0 0 0 0 0 0 8 0
0 0 0 0 0 4 0 0 0 0 0 0 8 8 0
```

**Train 1 output**
```text
7 7 7 0 4 0 0 9 0 8 8
0 0 0 0 4 4 0 9 0 8 0
0 0 0 0 0 4 0 9 0 8 8
```

**Train 2 input**
```text
2 8 0 7 9 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 7 7 0 0 0
0 0 0 0 9 9 9 0 0 7 0 0 0 0
0 8 0 0 0 9 0 0 0 0 0 4 0 0
0 8 8 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0 7 7 0 0 9 0 0 4 4 4
8 0 0 0 7 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
```

**Train 3 input**
```text
1 3 0 8 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 9 0 0 8 0 0 0 0 3 3 3 0
0 9 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 3 3 0 0 8 0 0 0 0 9
0 0 0 0 8 8 8 0 9 9 9
0 0 0 0 0 8 0 0 0 0 0
```

**Train 4 input**
```text
2 3 0 1 0 6 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 1 0
0 7 7 0 0 0 6 0 0 0 1 1 0
0 7 0 0 0 0 6 0 0 0 1 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 3 0 1 1 0 0 6 6 6 0 7 7 0
3 3 0 0 1 1 0 0 0 0 0 0 7 7
```

**Test 1 input**
```text
4 9 8 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 9 9 9 0 0 0 0
```

**Test 1 output**
```text
9 9 9 0 0 8 0 0 3 3 3
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```


## Solve Elbow Paths Separately in Each Chamber (`hard_42_chamber_elbow_paths`)

**Difficulty:** hard

**Skills:** local routing, frame decomposition, color-paired connection

**Scaffold notes:**
- Each framed chamber is independent.
- Inside a chamber, the two same-colored markers must be connected by an elbow path.
- Use the same vertical-then-horizontal routing rule in every chamber.

**Written solution:** Treat every rectangular frame as an independent chamber. Inside each chamber, find the two markers of the same color and connect them using the vertical-first elbow-path rule. Combine the solved chambers back into the original grid, preserving the frames.

**Program solution (Python reference):**
```python
def solve_hard_42_chamber_elbow_paths(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        ir0, ic0, ir1, ic1 = inside(box)
        pos = defaultdict(list)
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                if g[r][c] != 0:
                    pos[g[r][c]].append((r,c))
        for color, cells in pos.items():
            if len(cells) == 2:
                a,b = sorted(cells)
                for rr,cc in elbow_path(a,b,prefer='vertical_first'):
                    if ir0 <= rr <= ir1 and ic0 <= cc <= ic1:
                        out[rr][cc] = color
    return out
```

**Train 1 input**
```text
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 3 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 3 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 5 0 5 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 7 5 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 0 5 0 0 0
0 5 5 5 5 5 0 0 0 5 7 0 0 0 5 0 0 0
0 5 0 0 0 5 0 0 0 5 5 5 5 5 5 0 0 0
0 5 0 0 9 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 9 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 3 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 3 3 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 5 0 5 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 7 5 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 7 5 0 0 0
0 5 5 5 5 5 0 0 0 5 7 7 7 7 5 0 0 0
0 5 0 0 0 5 0 0 0 5 5 5 5 5 5 0 0 0
0 5 0 0 9 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 9 9 9 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 1 0 5 0 0 0 0 5 5 5 5 5 5
0 0 5 0 0 0 5 0 0 0 0 5 0 0 0 2 5
0 0 5 1 0 0 5 0 0 0 0 5 2 0 0 0 5
0 0 5 0 0 0 5 0 0 0 0 5 0 0 0 0 5
0 0 5 5 5 5 5 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 1 0 5 0 0 0 0 5 5 5 5 5 5
0 0 5 0 1 0 5 0 0 0 0 5 0 0 0 2 5
0 0 5 1 1 0 5 0 0 0 0 5 2 2 2 2 5
0 0 5 0 0 0 5 0 0 0 0 5 0 0 0 0 5
0 0 5 5 5 5 5 0 0 0 0 5 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 0 5 5 5 5 5 5 5 0
5 0 0 4 5 0 0 0 0 5 0 0 2 0 0 5 0
5 4 0 0 5 0 0 0 0 5 0 0 0 0 0 5 0
5 5 5 5 5 0 0 0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 0 0 2 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 0 5 5 5 5 5 5 5 0
5 0 0 4 5 0 0 0 0 5 0 0 2 0 0 5 0
5 4 4 4 5 0 0 0 0 5 0 0 2 0 0 5 0
5 5 5 5 5 0 0 0 0 5 0 0 2 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 2 2 2 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 2 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 2 0 5 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 8 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0
0 0 0 0 0 5 8 0 0 0 0 5 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 2 5 0 0 0 0
0 0 0 0 0 5 0 0 0 2 5 0 0 0 0
0 0 0 0 0 5 0 0 2 2 5 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 8 0 5 0 0 0
0 0 0 0 0 5 0 0 0 8 0 5 0 0 0
0 0 0 0 0 5 8 8 8 8 0 5 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 0 0 0
```

**Test 1 input**
```text
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 5 0 6 0 0 0 5
5 1 0 0 0 0 5 0 5 0 0 0 0 0 5
5 0 0 0 0 1 5 0 5 0 0 6 0 0 5
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 9 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 9 0 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 5 0 6 0 0 0 5
5 1 0 0 0 0 5 0 5 0 6 0 0 0 5
5 1 1 1 1 1 5 0 5 0 6 6 0 0 5
5 5 5 5 5 5 5 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 9 0 0 0 5 0 0 0 0 0
0 0 0 0 5 9 9 9 0 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
