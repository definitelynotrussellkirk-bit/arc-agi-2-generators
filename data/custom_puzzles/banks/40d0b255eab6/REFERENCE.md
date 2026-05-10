# ARC Puzzle Bank — Fifth 21 Puzzles
This fifth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`29`–`35`) so it follows directly after the fourth bundle.
This volume leans harder into diversity: crop/extract tasks, symmetry tasks, counting tasks, keyed transforms, matrix outputs, hole filling, and local-vs-global decomposition. It also introduces a new primitive — **`ray_until_block`** — and uses it across easy, medium, and hard tasks so it becomes a reusable concept rather than a one-off trick.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_fifth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_fifth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_fifth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_29_shoot_rays_to_walls` — **Shoot Rays Until the Walls**
- `easy_30_crop_nonzero_bbox` — **Crop the Nonzero Bounding Box**
- `easy_31_complete_main_diagonal_symmetry` — **Complete the Main-Diagonal Symmetry**
- `easy_32_fill_between_row_endpoints` — **Fill Between Matching Row Endpoints**
- `easy_33_stamp_template_at_marker` — **Stamp the Template at the Marker**
- `easy_34_keep_rarest_color` — **Keep Only the Rarest Color**
- `easy_35_hollow_solid_rectangles` — **Hollow the Solid Rectangles**

### Medium (7)
- `medium_29_directional_rays_by_seed_color` — **Shoot Horizontal or Vertical Rays by Seed Color**
- `medium_30_crop_components_and_pack_left_to_right` — **Crop Components and Pack Them Left to Right**
- `medium_31_scale_key_adjacent_component` — **Scale the Key-Adjacent Component by 2**
- `medium_32_fill_frame_intersections` — **Fill the Marked Intersections Inside the Frame**
- `medium_33_extract_bisymmetric_component` — **Extract the Only Bi-Symmetric Component**
- `medium_34_component_count_columns` — **Build a Component-Count Bar Chart**
- `medium_35_mirror_component_across_pivot` — **Mirror the Component Across the Pivot**

### Hard (7)
- `hard_29_local_rays_in_chambers` — **Solve Rays Separately Inside Each Chamber**
- `hard_30_assemble_transform_panel` — **Assemble a 2x2 Transform Panel**
- `hard_31_boolean_template_combine_by_key` — **Combine Two Templates by a Boolean Key**
- `hard_32_shape_match_matrix` — **Build the Shape-Match Matrix**
- `hard_33_local_transform_gallery_sorted_by_width` — **Make a Local Transform Gallery Sorted by Width**
- `hard_34_overlay_count_map_from_components` — **Build the Overlay Count Map from Normalized Components**
- `hard_35_fill_holed_component_with_key_color` — **Fill the Holed Component with the Key Color**

## Shoot Rays Until the Walls (`easy_29_shoot_rays_to_walls`)

**Difficulty:** easy

**Skills:** invented primitive: ray_until_block, same-size fill, wall-bounded propagation

**Scaffold notes:**
- Treat each red seed as a source cell.
- Extend in the four cardinal directions through empty cells.
- Stop before the first gray wall cell or the grid edge.

**Written solution:** Treat every red(2) seed as a source. Using the new primitive `ray_until_block`, send rays up, down, left, and right until the next gray(5) wall cell or the grid edge. Recolor the seed and every traversed cell to cyan(8), and leave the gray walls alone.

**Program solution (Python reference):**
```python
def solve_easy_29_shoot_rays_to_walls(g: Grid) -> Grid:
    out = clone(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 2:
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    for rr, cc in ray_until_block(g, (r, c), dr, dc, blockers={5}, include_start=True):
                        if g[rr][cc] != 5:
                            out[rr][cc] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 2 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 5 5 5 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 2 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 8 0 0 5 0 0 0 0 0
8 8 8 8 8 5 0 0 0 0 0
0 0 8 0 0 5 0 5 5 5 0
0 0 8 0 0 5 0 0 8 0 0
0 0 8 0 0 5 0 0 8 0 0
0 0 8 0 0 5 0 0 8 0 0
0 0 8 0 0 5 8 8 8 8 8
0 0 8 0 0 5 0 0 8 0 0
0 0 8 0 0 5 0 0 8 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8 0 0 0 0 0 5 0 0
0 8 0 0 0 0 0 5 0 0
8 8 8 8 8 8 8 8 8 8
0 8 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 8 0 0 0
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 8 0 0 0
```

**Train 3 input**
```text
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 2 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 5 5 5 5 5
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8 0 5 0 0 0 0 8 0
0 8 0 5 0 0 0 0 8 0
0 8 0 5 8 8 8 8 8 8
0 8 0 5 0 0 0 0 8 0
0 8 0 5 0 0 0 0 8 0
8 8 8 8 8 8 8 8 8 8
0 8 0 5 0 0 0 0 8 0
0 8 0 5 0 5 5 5 5 5
0 8 0 5 0 0 0 0 0 0
0 8 0 5 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 2 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
```

**Train 4 output**
```text
0 0 0 8 0 0 0 8 0 0 0 0
0 0 0 8 0 0 0 8 5 5 5 5
0 0 0 8 0 0 0 8 0 5 0 0
8 8 8 8 8 8 8 8 8 5 0 0
0 0 0 8 0 0 0 8 0 5 0 0
8 8 8 8 8 8 8 8 8 5 0 0
0 0 0 8 0 0 0 8 0 5 0 0
```

**Test input**
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 2 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 5 5 5 5
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 2 0 0
0 0 0 0 0 0 5 0 0 0 0 0
```

**Test output**
```text
0 0 8 0 0 0 5 0 0 0 0 0
0 0 8 0 0 0 5 0 0 0 0 0
8 8 8 8 8 8 5 0 0 0 0 0
0 0 8 0 0 0 5 0 0 0 0 0
0 0 8 0 0 0 5 0 0 0 0 0
0 0 8 0 0 0 5 0 5 5 5 5
0 0 8 0 0 0 5 0 0 8 0 0
0 0 8 0 0 0 5 8 8 8 8 8
0 0 8 0 0 0 5 0 0 8 0 0
```

## Crop the Nonzero Bounding Box (`easy_30_crop_nonzero_bbox`)

**Difficulty:** easy

**Skills:** size-changing crop, bounding box, preserve colors

**Scaffold notes:**
- Ignore the large black border.
- Find the smallest rectangle containing every nonzero cell.
- Return exactly that crop.

**Written solution:** Find the tight bounding box around all nonzero cells and return that rectangle as the output. Nothing is recolored or rearranged; the task is only to remove the surrounding black background.

**Program solution (Python reference):**
```python
def solve_easy_30_crop_nonzero_bbox(g: Grid) -> Grid:
    return crop_nonzero(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 7 0 0 0 0 0
0 0 0 6 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 7 0
6 7 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 3 3
3 3 0
0 3 4
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 0
5 5
0 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 3 0 0 0 0 0 0
0 0 0 2 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 0 3
0 2 3 3
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 0 0
4 4 4
0 0 4
```

## Complete the Main-Diagonal Symmetry (`easy_31_complete_main_diagonal_symmetry`)

**Difficulty:** easy

**Skills:** same-size symmetry, transpose, color preservation

**Scaffold notes:**
- Read the main diagonal as the mirror axis.
- For every colored cell at (r,c), also color (c,r) the same way.
- Keep cells already on the diagonal unchanged.

**Written solution:** Reflect the colored pattern across the main diagonal of the square grid. Every nonzero cell is copied to its transposed location, so the final grid is symmetric under swapping rows and columns.

**Program solution (Python reference):**
```python
def solve_easy_31_complete_main_diagonal_symmetry(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[c][r] = g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0
0 6 0 0 0
2 0 0 0 0
0 3 0 0 0
4 0 2 0 0
```

**Train 1 output**
```text
0 0 2 0 4
0 6 0 3 0
2 0 0 0 2
0 3 0 0 0
4 0 2 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0
0 0 0 0 0 0
0 0 7 0 0 0
0 2 0 0 0 0
0 2 0 0 0 0
1 0 0 4 0 0
```

**Train 2 output**
```text
0 0 0 0 0 1
0 0 0 2 2 0
0 0 7 0 0 0
0 2 0 0 0 4
0 2 0 0 0 0
1 0 0 4 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 0 0 0 0 0 0
0 6 0 0 0 0 0
0 0 5 0 0 0 0
3 0 0 0 9 0 0
```

**Train 3 output**
```text
0 0 0 2 0 0 3
0 0 0 0 6 0 0
0 0 0 0 0 5 0
2 0 0 0 0 0 0
0 6 0 0 0 0 9
0 0 5 0 0 0 0
3 0 0 0 9 0 0
```

**Train 4 input**
```text
0 0 0 0 0
0 0 0 0 0
4 0 0 0 0
0 0 4 0 0
0 8 0 0 1
```

**Train 4 output**
```text
0 0 4 0 0
0 0 0 0 8
4 0 0 4 0
0 0 4 0 0
0 8 0 0 1
```

**Test input**
```text
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 0
0 0 5 0 0 0
0 7 0 0 0 2
```

**Test output**
```text
0 0 0 5 0 0
0 0 0 0 0 7
0 0 0 0 5 0
5 0 0 0 0 0
0 0 5 0 0 0
0 7 0 0 0 2
```

## Fill Between Matching Row Endpoints (`easy_32_fill_between_row_endpoints`)

**Difficulty:** easy

**Skills:** row-wise reasoning, segment filling, ignore distractors

**Scaffold notes:**
- Work one row at a time.
- Only rows with exactly two nonzero cells of the same color should change.
- Fill the whole inclusive span between those two endpoints.

**Written solution:** Inspect each row independently. If a row contains exactly two colored cells and they have the same color, fill every cell between them with that color. Rows with mismatched colors or extra colored cells stay unchanged.

**Program solution (Python reference):**
```python
def solve_easy_32_fill_between_row_endpoints(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        nz = [(c, g[r][c]) for c in range(w) if g[r][c] != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            c0, col = nz[0]
            c1, _ = nz[1]
            for c in range(min(c0, c1), max(c0, c1)+1):
                out[r][c] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 4 0 0
7 0 0 0 7 0 0 0 0 0
0 0 5 0 5 0 5 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 4 0 0
7 7 7 7 7 0 0 0 0 0
0 0 5 0 5 0 5 0 0 0
```

**Train 2 input**
```text
0 0 6 0 0 0 0 0 0 6 0
0 2 0 0 0 0 5 0 0 0 0
3 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 8
0 0 0 4 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6 6 6 6 6 6 6 6 0
0 2 0 0 0 0 5 0 0 0 0
3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8
0 0 0 4 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0
0 0 1 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 5 0 5 0 0
0 0 0 6 0 0 0 0 6
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0
0 0 1 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 5 0 5 0 0
0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 4 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 7 0
0 0 0 4 0 0 0 0 0 6 0 0
0 0 0 0 0 2 2 2 0 0 0 0
3 0 0 0 0 0 0 0 3 0 0 0
```

**Train 4 output**
```text
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 4 0 0 0 0 0 6 0 0
0 0 0 0 0 2 2 2 0 0 0 0
3 3 3 3 3 3 3 3 3 0 0 0
```

**Test input**
```text
3 0 0 0 0 0 0 4
8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 6 0 6 0 0 6 0
0 0 2 0 0 0 0 2
0 0 0 0 0 0 0 0
```

**Test output**
```text
3 0 0 0 0 0 0 4
8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 6 0 6 0 0 6 0
0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0
```

## Stamp the Template at the Marker (`easy_33_stamp_template_at_marker`)

**Difficulty:** easy

**Skills:** template extraction, translation, same-size stamping

**Scaffold notes:**
- There is one real template object and one marker cell.
- Crop the template tightly.
- Paste a copy with its top-left corner aligned to the marker.

**Written solution:** Take the single non-marker object as the template, crop it tightly, and paste a copy of that crop at the marker location. The original template stays in place; the marker is replaced by the copied template.

**Program solution (Python reference):**
```python
def solve_easy_33_stamp_template_at_marker(g: Grid) -> Grid:
    comps = components4_any([[0 if v == 8 else v for v in row] for row in g])
    template = max(comps, key=len)
    crop = comp_crop(g, template)
    marker = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    out = clone(g)
    out[marker[0]][marker[1]] = 0
    paste(out, crop, marker[0], marker[1])
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0
0 0 6 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0
0 0 6 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 7 0 0
0 0 0 0 0 0 0 0 6 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 3 0 0 0 0 0 0
0 2 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 3 0
0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 3 0 0 0 0 0 0
0 2 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 7 7 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 7 7 0 0
0 7 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 5 0 0
0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 3 3 0 0 0 0 0 0
0 0 3 5 0 0 0 0 0
0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 5 0 0
0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Keep Only the Rarest Color (`easy_34_keep_rarest_color`)

**Difficulty:** easy

**Skills:** global counting, color selection, same-size filtering

**Scaffold notes:**
- Count how many cells each nonzero color occupies.
- Find the unique smallest count.
- Erase every other color.

**Written solution:** Count the number of cells of each nonzero color. Identify the unique rarest color, keep only those cells, and turn every other nonzero cell to black.

**Program solution (Python reference):**
```python
def solve_easy_34_keep_rarest_color(g: Grid) -> Grid:
    cnt = Counter(v for row in g for v in row if v != 0)
    rare = min(cnt, key=lambda k: (cnt[k], k))
    out = zeros(*dims(g))
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == rare:
                out[r][c] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 3 0
0 2 2 0 0 0 0 0 3 0
0 2 0 0 0 0 0 0 3 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
1 0 0 0 0 0 0 0 0
1 0 0 0 0 5 5 0 0
1 0 0 0 0 0 5 0 0
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 9 0
0 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 8 8 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 4 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 7
0 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Hollow the Solid Rectangles (`easy_35_hollow_solid_rectangles`)

**Difficulty:** easy

**Skills:** object detection, rectangle logic, interior clearing

**Scaffold notes:**
- Only the solid color-6 rectangles are transformed.
- Preserve each rectangle border.
- Turn the interior cells black.

**Written solution:** Find each connected color-6 region that forms a completely filled rectangle. Replace that solid rectangle by its border only, turning the interior cells black. Other colors are left alone.

**Program solution (Python reference):**
```python
def solve_easy_35_hollow_solid_rectangles(g: Grid) -> Grid:
    out = clone(g)
    for comp in components4_color(g, 6):
        r0, c0, r1, c1 = bbox(comp)
        area = (r1-r0+1) * (c1-c0+1)
        if len(comp) == area:
            for r in range(r0+1, r1):
                for c in range(c0+1, c1):
                    out[r][c] = 0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 3 0
0 6 6 6 6 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0
3 0 0 0 0 0 0 6 6 6 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 3 0
0 6 6 6 6 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 6 0 6 0 0
3 0 0 0 0 0 0 6 6 6 0 0
```

**Train 2 input**
```text
4 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 6 0 0 0 6 0 0 0
0 0 6 0 0 0 6 0 0 0
0 0 6 0 0 0 6 0 0 0
0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 6 6 6 0 0
0 6 6 6 6 6 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 2
```

**Train 3 output**
```text
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 6 6 6 0 0
0 6 6 6 6 6 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 7 0
0 6 6 6 6 0 0 0 7 7
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 7 0
0 6 6 6 6 0 0 0 7 7
0 6 0 0 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5
```

**Test output**
```text
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5
```

## Shoot Horizontal or Vertical Rays by Seed Color (`medium_29_directional_rays_by_seed_color`)

**Difficulty:** medium

**Skills:** invented primitive: ray_until_block, orientation by color, overlap handling

**Scaffold notes:**
- Red seeds and blue seeds behave differently.
- Red(2) seeds emit horizontal beams; blue(1) seeds emit vertical beams.
- Use a special overlap color where the two beam systems cross.

**Written solution:** Use `ray_until_block` with gray(5) cells as blockers. Every red(2) seed emits a horizontal beam left and right; every blue(1) seed emits a vertical beam up and down. Color horizontal-only beam cells orange(7), vertical-only beam cells cyan(8), and overlaps magenta(6); keep the gray walls unchanged.

**Program solution (Python reference):**
```python
def solve_medium_29_directional_rays_by_seed_color(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    hpaint, vpaint = set(), set()
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 5:
                out[r][c] = 5
            elif v == 2:
                hpaint.update(ray_until_block(g, (r, c), 0, 1, blockers={5}, include_start=True))
                hpaint.update(ray_until_block(g, (r, c), 0, -1, blockers={5}))
            elif v == 1:
                vpaint.update(ray_until_block(g, (r, c), 1, 0, blockers={5}, include_start=True))
                vpaint.update(ray_until_block(g, (r, c), -1, 0, blockers={5}))
    for cell in hpaint | vpaint:
        r, c = cell
        if g[r][c] == 5:
            continue
        if cell in hpaint and cell in vpaint:
            out[r][c] = 6
        elif cell in hpaint:
            out[r][c] = 7
        else:
            out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 1 0
0 2 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 5 5 5 5
0 0 0 0 0 5 0 0 0 0 0
0 0 0 1 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 2 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 8 0 5 0 0 0 8 0
0 0 0 8 0 5 0 0 0 8 0
7 7 7 6 7 5 0 0 0 8 0
0 0 0 8 0 5 0 0 0 8 0
0 0 0 8 0 5 0 5 5 5 5
0 0 0 8 0 5 0 0 0 0 0
0 0 0 8 0 5 0 0 0 0 0
0 0 0 8 0 5 7 7 7 7 7
0 0 0 8 0 5 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 1 0 5 0 0 0
0 2 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 8 0
7 7 7 7 7 7 7 7 7 7 6 7
0 0 0 0 0 0 0 0 0 0 8 0
5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 8 0 5 0 0 0
0 0 0 0 0 0 8 0 5 0 0 0
7 7 7 7 7 7 6 7 5 0 0 0
0 0 0 0 0 0 8 0 5 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 5 0 0 0 0 0 0 1
0 0 5 0 0 0 0 0 0 0
1 0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 5 5 5 5 5
0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 2 0 0 0 0
0 0 5 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0 0 0 0 0 0 0 8
6 7 7 7 7 7 7 7 7 6
8 0 5 0 0 0 0 0 0 8
8 0 5 0 0 0 0 0 0 8
8 0 5 0 0 0 0 0 0 8
8 0 5 0 0 0 0 0 0 8
8 0 5 0 5 5 5 5 5 5
8 0 5 0 0 0 0 0 0 0
8 0 5 7 7 7 7 7 7 7
8 0 5 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 1 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 1
5 5 5 5 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 4 output**
```text
0 0 0 0 0 8 0 5 0 8
0 0 0 0 0 8 0 5 0 8
0 0 0 0 0 8 0 5 0 8
7 7 7 7 7 6 7 5 0 8
0 0 0 0 0 8 0 5 0 8
5 5 5 5 0 8 0 5 0 8
0 0 0 0 0 8 0 5 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
0 0 0 0 5 0 0 0 0
0 0 1 0 5 0 0 0 0
0 0 0 0 5 0 2 0 0
0 0 0 0 5 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
7 7 7 7 7 7 7 6 7
0 0 0 0 0 0 0 8 0
5 5 5 5 5 5 5 5 5
0 0 8 0 5 0 0 0 0
0 0 8 0 5 0 0 0 0
0 0 8 0 5 7 7 7 7
0 0 8 0 5 0 0 0 0
```

## Crop Components and Pack Them Left to Right (`medium_30_crop_components_and_pack_left_to_right`)

**Difficulty:** medium

**Skills:** component extraction, size-changing packing, ordering by position

**Scaffold notes:**
- Separate the disconnected objects.
- Crop each object to its own bounding box.
- Repack them in their original left-to-right order with one blank column between.

**Written solution:** Split the input into connected components, crop each one tightly, sort them by the left edge of their original position, and place the crops next to each other with a one-column black separator.

**Program solution (Python reference):**
```python
def solve_medium_30_crop_components_and_pack_left_to_right(g: Grid) -> Grid:
    comps = components4_any(g)
    comps.sort(key=lambda comp: (bbox(comp)[1], bbox(comp)[0]))
    crops = [comp_crop(g, comp) for comp in comps]
    return pack_horiz_top(crops, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 6 0 7 0 2 3 0 0 0
0 0 0 0 0 6 7 7 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 0 0 6 0 7 0 2 0
0 4 5 0 6 7 7 0 2 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 7 0 0 0 0 0 0 0 0 0 0
0 0 6 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 2 0 0 0 0 9 0 0 0
0 0 0 0 0 0 2 3 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 7 0 2 0 0 9 9 0 9
6 7 7 0 2 3 0 0 9 0 0
```

**Train 3 input**
```text
4 4 0 0 0 0 0 0 0 0 0 0 0
0 4 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 2 0 0 0 9 0 0 0
0 0 0 0 0 2 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 0 0 2 0 0 9 9 0 9
0 4 5 0 2 3 0 0 9 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 0 7 0
2 0 0 0 0 0 0 0 0 0 0 0 6 7 7 0
2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 0 4 4 0 0 6 0 7
2 3 0 0 4 5 0 6 7 7
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 2 0 0 0 0 0 0 0 4 5 0
0 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 0 0 9 9 0 9 0 4 4 0
2 3 0 0 9 0 0 0 0 4 5
```

## Scale the Key-Adjacent Component by 2 (`medium_31_scale_key_adjacent_component`)

**Difficulty:** medium

**Skills:** component selection, adjacency to marker, scaling

**Scaffold notes:**
- The marker identifies which object matters.
- Choose the component touching the marker in the local neighborhood.
- Crop it tightly and scale every cell to a 2x2 block.

**Written solution:** Find the connected component that is adjacent to the marker cell. Crop that target component tightly and enlarge it by a factor of 2 in both directions, replacing each original cell by a 2x2 block of the same color.

**Program solution (Python reference):**
```python
def solve_medium_31_scale_key_adjacent_component(g: Grid) -> Grid:
    marker = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    # components excluding marker
    gg = [[0 if v == 8 else v for v in row] for row in g]
    for comp in components4_any(gg):
        s = set(comp)
        for r, c in comp:
            if max(abs(r-marker[0]), abs(c-marker[1])) <= 1:
                crop = comp_crop(g, comp)
                return scale_grid(crop, 2)
    raise AssertionError("no marked component")
```

**Train 1 input**
```text
0 8 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 5 5 0 0 0 4 4 4 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 0 0
3 3 0 0
3 3 0 0
3 3 0 0
3 3 3 3
3 3 3 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 4 0 0 0
0 0 6 0 0 0 4 4 0 0
0 0 8 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 0 0
6 6 0 0
6 6 6 6
6 6 6 6
0 0 6 6
0 0 6 6
```

**Train 3 input**
```text
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
0 3 3 0 0 0 0 0 0 7 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 5 0 0
5 5 0 0
5 5 5 5
5 5 5 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0
2 0 3 0 0 0 0 0 0 0 0
2 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 0 0
9 9 0 0
9 9 0 0
9 9 0 0
9 9 9 9
9 9 9 9
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 6 0 0 0 0 0 0 0 2 2 2 0 0
0 6 6 0 8 0 0 0 0 0 0 0 0 0
0 0 6 0 6 7 0 0 0 0 0 0 0 0
0 0 0 0 6 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 6 7 7 0 0
6 6 7 7 0 0
6 6 7 7 7 7
6 6 7 7 7 7
```

## Fill the Marked Intersections Inside the Frame (`medium_32_fill_frame_intersections`)

**Difficulty:** medium

**Skills:** frame reasoning, row/column selection, same-size intersection fill

**Scaffold notes:**
- Use the border markers to select rows and columns.
- Row markers sit on the left border; column markers sit on the top border.
- Paint their intersections inside the frame.

**Written solution:** Read the framed rectangle as the working area. The color-2 cells on the left border mark rows, and the color-3 cells on the top border mark columns. Fill every interior crossing of a marked row and a marked column with color 7.

**Program solution (Python reference):**
```python
def solve_medium_32_fill_frame_intersections(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    marked_rows = [r for r in range(r0+1, r1) if g[r][c0] == 2]
    marked_cols = [c for c in range(c0+1, c1) if g[r0][c] == 3]
    out = clone(g)
    for r in marked_rows:
        for c in marked_cols:
            out[r][c] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 3 5 5 3 3 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 3 5 5 3 3 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 2 0 7 0 0 7 7 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 2 0 7 0 0 7 7 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 5 5 3 5 3 5 5 0 0
0 5 0 0 0 0 0 5 0 0
0 2 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 2 0 0 0 0 0 5 0 0
0 5 5 5 5 5 5 5 0 0
```

**Train 2 output**
```text
0 5 5 3 5 3 5 5 0 0
0 5 0 0 0 0 0 5 0 0
0 2 0 7 0 7 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 5 0 0
0 2 0 7 0 7 0 5 0 0
0 5 5 5 5 5 5 5 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 3 5 5 5 3 3 5 0
0 0 0 5 0 0 0 0 0 0 0 5 0
0 0 0 2 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 5 0
0 0 0 2 0 0 0 0 0 0 0 5 0
0 0 0 2 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 3 5 5 5 3 3 5 0
0 0 0 5 0 0 0 0 0 0 0 5 0
0 0 0 2 0 7 0 0 0 7 7 5 0
0 0 0 5 0 0 0 0 0 0 0 5 0
0 0 0 2 0 7 0 0 0 7 7 5 0
0 0 0 2 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 3 5 5 5 3 5 3 5 0
0 2 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 5 0
0 2 0 0 0 0 0 0 0 5 0
0 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 3 5 5 5 3 5 3 5 0
0 2 7 0 0 0 7 0 7 5 0
0 5 0 0 0 0 0 0 0 5 0
0 2 7 0 0 0 7 0 7 5 0
0 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 3 5 3 5 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 3 5 3 5 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 2 0 7 0 7 0 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 2 0 7 0 7 0 5 0 0
0 0 2 0 7 0 7 0 5 0 0
0 0 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Extract the Only Bi-Symmetric Component (`medium_33_extract_bisymmetric_component`)

**Difficulty:** medium

**Skills:** shape analysis, horizontal and vertical symmetry, size-changing selection

**Scaffold notes:**
- Compare the disconnected shapes, not their positions.
- One component is symmetric both left-right and top-bottom.
- Crop and return only that component.

**Written solution:** Among the disconnected objects, find the unique one whose shape is symmetric both horizontally and vertically. Return that component as a tight crop, preserving its original color.

**Program solution (Python reference):**
```python
def solve_medium_33_extract_bisymmetric_component(g: Grid) -> Grid:
    for comp in components4_any(g):
        offs = normalize_offsets(comp)
        if is_h_symmetric_offsets(offs) and is_v_symmetric_offsets(offs):
            return comp_crop(g, comp)
    raise AssertionError("no bisymmetric component")
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 4 4 0 0
0 2 0 0 0 0 0 0 0 0 4 4 0
0 2 2 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6
6 0 6
6 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 3 0 0 0 0 0 0 0 7 0 0
0 3 3 0 0 0 0 0 0 7 7 7
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 0
5 5 5
0 5 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8
8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 7 0 7 0 3 0
0 0 0 0 0 7 7 7 0 3 3
0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 7
7 0 7
7 7 7
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0
0 2 0 0 0 0 0 0 0 0 0 5 5
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 9 0
9 9 9
0 9 0
```

## Build a Component-Count Bar Chart (`medium_34_component_count_columns`)

**Difficulty:** medium

**Skills:** count connected components, size-changing summary output, bottom-aligned bars

**Scaffold notes:**
- Count components separately for each nonzero color.
- Make one column per color, ordered by color value.
- The height of each bar is the number of components of that color.

**Written solution:** For each nonzero color, count how many connected components of that color appear in the input. Build a vertical bar chart with one bar per color in ascending color order, bottom-align the bars, and use the original color for each bar. Put one blank separator column between neighboring bars.

**Program solution (Python reference):**
```python
def solve_medium_34_component_count_columns(g: Grid) -> Grid:
    colors = sorted({v for row in g for v in row if v != 0})
    counts = []
    for color in colors:
        counts.append(len(components4_color(g, color)))
    h = max(counts)
    w = 2 * len(colors) - 1
    out = zeros(h, w)
    for i, (color, count) in enumerate(zip(colors, counts)):
        col = 2 * i
        for k in range(count):
            out[h-1-k][col] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 2 2 2 0
0 1 0 0 0 3 3 0 0 0 0 0
0 1 1 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 1 0 0 0 0 0 0 3 3 0 0
0 1 1 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 0 0 0 3
1 0 2 0 3
```

**Train 2 input**
```text
0 0 0 0 0 0 4 4 4 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 6 0 0 4 4 0
0 2 0 0 6 0 0 0 0 0
0 2 2 0 6 6 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 0 0
2 0 4 0 0
2 0 4 0 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 3 0 0 0
0 3 3 0 0 3 3 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 5 5 0 0 0 0 0 7 7 0 0
0 0 5 5 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 0 0 0
3 0 0 0 0
3 0 5 0 7
```

**Train 4 input**
```text
1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 8 0 0 9 9 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 0 8 0 0
0 9 9 0 0 0 0 0 8 0 0
0 9 9 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 8 0 9
1 0 8 0 9
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 4 4 4 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 2 0 0 0 0 0 0 3 3 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 0 0 0 0
2 0 0 0 4
2 0 3 0 4
```

## Mirror the Component Across the Pivot (`medium_35_mirror_component_across_pivot`)

**Difficulty:** medium

**Skills:** relative coordinates, two-axis mirroring, same-size replication

**Scaffold notes:**
- Treat the marker as a pivot point.
- The visible component is only one quadrant of the final arrangement.
- Reflect it across the pivot horizontally, vertically, and both at once.

**Written solution:** Use the marker cell as the center of a four-way mirror. Keep the original component, then create its reflections across the vertical axis through the pivot, the horizontal axis through the pivot, and both axes together. Preserve the cell colors and keep the pivot marker unchanged.

**Program solution (Python reference):**
```python
def solve_medium_35_mirror_component_across_pivot(g: Grid) -> Grid:
    pivot = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    gg = [[0 if v == 8 else v for v in row] for row in g]
    comp = max(components4_any(gg), key=len)
    out = zeros(*dims(g))
    out[pivot[0]][pivot[1]] = 8
    pr, pc = pivot
    for r, c in comp:
        v = g[r][c]
        for rr, cc in {(r, c), (r, 2*pc-c), (2*pr-r, c), (2*pr-r, 2*pc-c)}:
            if 0 <= rr < len(out) and 0 <= cc < len(out[0]):
                out[rr][cc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 3 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 3 4 0 0 0 4 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 4 0 0 0 4 3 0
0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 6 0 0 0 0 0 0
0 0 5 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 6 0 6 0 5 0 0
0 0 5 6 6 0 6 6 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 0 6 6 5 0 0
0 0 5 0 6 0 6 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 0 7 9 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0
0 0 7 7 0 0 0 7 7 0 0
0 0 0 7 9 0 9 7 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 7 9 0 9 7 0 0 0
0 0 7 7 0 0 0 7 7 0 0
0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 0 0 0 2 1 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 1 2 0 0 0 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 4 5 0 0 0 0 0 0
0 0 5 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 4 5 0 0 0 5 4 0
0 0 5 6 0 6 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 6 0 6 5 0 0
0 4 5 0 0 0 5 4 0
0 0 0 0 0 0 0 0 0
```

## Solve Rays Separately Inside Each Chamber (`hard_29_local_rays_in_chambers`)

**Difficulty:** hard

**Skills:** invented primitive: ray_until_block, local frame decomposition, internal blockers

**Scaffold notes:**
- Treat each framed chamber as its own subproblem.
- Inside a chamber, a red seed means horizontal and a blue seed means vertical.
- The ray stops at local blockers and at the chamber border.

**Written solution:** Process each gray frame independently. Within one chamber, a red(2) seed emits a horizontal beam and a blue(1) seed emits a vertical beam. Use `ray_until_block` inside the chamber only, with both color-4 blockers and the frame border as stopping conditions, and recolor the traversed cells to 7.

**Program solution (Python reference):**
```python
def solve_hard_29_local_rays_in_chambers(g: Grid) -> Grid:
    out = clone(g)
    frames = [comp for comp in components4_color(g, 5) if is_rect_border_component(comp)]
    for frame in frames:
        r0, c0, r1, c1 = bbox(frame)
        bounds = (r0+1, c0+1, r1-1, c1-1)
        seeds = [(r, c, g[r][c]) for r in range(bounds[0], bounds[2]+1) for c in range(bounds[1], bounds[3]+1) if g[r][c] in (1, 2)]
        for r, c, seed in seeds:
            if seed == 2:
                cells = set(ray_until_block(g, (r, c), 0, 1, blockers={4,5}, bounds=bounds, include_start=True))
                cells |= set(ray_until_block(g, (r, c), 0, -1, blockers={4,5}, bounds=bounds))
            else:
                cells = set(ray_until_block(g, (r, c), 1, 0, blockers={4,5}, bounds=bounds, include_start=True))
                cells |= set(ray_until_block(g, (r, c), -1, 0, blockers={4,5}, bounds=bounds))
            for rr, cc in cells:
                out[rr][cc] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 4 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 2 0 4 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 4 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 1 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 4 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 4 0 5 0 0 0 0 0 0 0 0 0 0
0 5 7 7 7 4 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 4 7 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 7 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 4 7 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 5 0 1 0 0 5 0 0 5 0 0 0 4 5 0
0 0 5 0 4 0 0 5 0 0 5 0 2 0 4 5 0
0 0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 1 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 4 0 0 0 5 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 5 0 7 0 0 5 0 0 5 0 0 0 4 5 0
0 0 5 0 4 0 0 5 0 0 5 0 2 0 4 5 0
0 0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 1 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 4 0 0 0 5 0 0 0 0
0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 5 0 0 0 4 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 2 0 4 0 5 0 0 0 5 0 0 1 0 0 5 0
0 5 0 0 0 4 0 5 0 0 0 5 0 0 4 0 0 5 0
0 5 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 2 0 4 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 5 0 0 0 4 0 5 0 0 0 5 0 0 7 0 0 5 0
0 5 7 7 7 4 0 5 0 0 0 5 0 0 7 0 0 5 0
0 5 0 0 0 4 0 5 0 0 0 5 0 0 4 0 0 5 0
0 5 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 7 7 7 4 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 2 0 4 5 0 0 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 5 5 5 5 5 0 0 5 0 2 0 4 5 0
0 5 5 5 5 5 5 0 0 5 0 0 0 4 5 0
0 5 0 0 1 0 5 0 0 5 0 0 0 0 5 0
0 5 0 0 4 0 5 0 0 5 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 2 0 4 5 0 0 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 5 5 5 5 5 0 0 5 7 7 7 4 5 0
0 5 5 5 5 5 5 0 0 5 0 0 0 4 5 0
0 5 0 0 1 0 5 0 0 5 0 0 0 0 5 0
0 5 0 0 4 0 5 0 0 5 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 0 5 0 4 0 0 5 0 0 5 0 0 0 0 5 0
0 0 0 5 0 1 0 0 5 0 0 5 0 2 0 4 5 0
0 0 0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 1 0 4 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 4 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 0 5 0 4 0 0 5 0 0 5 0 0 0 0 5 0
0 0 0 5 0 7 0 0 5 0 0 5 7 7 7 4 5 0
0 0 0 5 0 7 0 0 5 0 0 5 0 0 0 0 5 0
0 0 0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 7 0 4 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 4 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Assemble a 2x2 Transform Panel (`hard_30_assemble_transform_panel`)

**Difficulty:** hard

**Skills:** template extraction, keyed transformations, panel assembly

**Scaffold notes:**
- Extract the single template object.
- Read the four key cells in order from left to right.
- Transform the template four times and place the results in a 2x2 panel.

**Written solution:** Take the main object as the template and read the four key colors on the bottom row from left to right. Each key selects a transform (identity, clockwise rotation, 180-degree rotation, or horizontal flip). Apply those four transforms and place the results into a 2x2 panel, top-left aligning each transformed crop inside an equal-sized quadrant cell.

**Program solution (Python reference):**
```python
def solve_hard_30_assemble_transform_panel(g: Grid) -> Grid:
    keys = [v for v in g[-1] if v in (1,2,3,4)]
    gg = clone(g)
    for c, v in enumerate(gg[-1]):
        if v in (1,2,3,4):
            gg[-1][c] = 0
    template = comp_crop(gg, max(components4_any(gg), key=len))
    trans = [transform_by_key(template, k) for k in keys]
    cell_h = max(dims(t)[0] for t in trans)
    cell_w = max(dims(t)[1] for t in trans)
    out = zeros(cell_h*2+1, cell_w*2+1)
    positions = [(0,0),(0,cell_w+1),(cell_h+1,0),(cell_h+1,cell_w+1)]
    for t, (r, c) in zip(trans, positions):
        paste(out, t, r, c)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 3 0 0 0 0 0 0 0 0
0 2 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 2 0 3 0 4 0 0 0 0
```

**Train 1 output**
```text
2 0 3 0 0 2 2
2 3 3 0 3 3 0
0 3 0 0 0 3 3
0 0 0 0 0 0 0
0 3 0 0 3 0 2
3 3 2 0 3 3 2
3 0 2 0 0 3 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 4 5 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 4 0 1 0 3 0 0 0 0
```

**Train 2 output**
```text
0 0 4 0 0 4 4
5 4 4 0 5 4 0
5 5 0 0 5 5 0
0 0 0 0 0 0 0
4 4 0 0 5 5 0
0 4 5 0 5 4 0
0 5 5 0 0 4 4
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 7 0 0
0 0 0 0 0 0 6 7 0 0 0
0 0 0 0 0 0 6 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 3 0 2 0 1 0 0 0
```

**Train 3 output**
```text
7 0 6 0 7 7 6
0 7 6 0 0 7 6
7 7 6 0 7 0 6
0 0 0 0 0 0 0
6 6 6 0 6 0 7
7 7 0 0 6 7 0
7 0 7 0 6 7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 3 4 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 1 0 4 0 2 0 0 0
```

**Train 4 output**
```text
4 4 0 0 2 2 0
4 3 0 0 0 3 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
0 2 2 0 0 0 2
4 3 0 0 4 3 2
4 4 0 0 4 4 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 6 0 0 0 0 0
0 0 0 0 5 6 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 4 0 1 0 0 0
```

**Test output**
```text
7 5 5 0 7 5 5
7 6 0 0 7 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 5 0 0 5 0 0
6 5 0 0 5 6 0
7 7 0 0 7 7 0
```

## Combine Two Templates by a Boolean Key (`hard_31_boolean_template_combine_by_key`)

**Difficulty:** hard

**Skills:** template normalization, boolean mask operations, key-controlled logic

**Scaffold notes:**
- Normalize the two colored shapes to their own bounding boxes.
- Interpret the key color as OR, AND, or XOR.
- Return the combined mask in a single output color.

**Written solution:** Normalize the color-2 shape and the color-3 shape by cropping them to their own bounding boxes and aligning those crops at the top-left. Then combine the two masks according to the key cell: 4 means union, 6 means intersection, and 8 means exclusive-or. Color the resulting mask with 7.

**Program solution (Python reference):**
```python
def solve_hard_31_boolean_template_combine_by_key(g: Grid) -> Grid:
    key = next(v for row in g for v in row if v in (4,6,8))
    a_cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == 2]
    b_cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == 3]
    a = offsets_to_grid(normalize_offsets(a_cells), color=1)
    b = offsets_to_grid(normalize_offsets(b_cells), color=1)
    h = max(dims(a)[0], dims(b)[0])
    w = max(dims(a)[1], dims(b)[1])
    aa = zeros(h,w); bb = zeros(h,w)
    paste(aa, a, 0, 0); paste(bb, b, 0, 0)
    out = zeros(h,w)
    for r in range(h):
        for c in range(w):
            av = aa[r][c] != 0
            bv = bb[r][c] != 0
            if key == 4:
                ok = av or bv
            elif key == 6:
                ok = av and bv
            else:
                ok = (av != bv)
            if ok:
                out[r][c] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 4 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 0
7 7 7
7 7 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 7 0
7 0 7
0 7 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 0
0 0 7
0 7 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
```

**Train 4 output**
```text
7 7
7 7
```

**Test input**
```text
8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 7 0
7 7 7
7 7 7
```

## Build the Shape-Match Matrix (`hard_32_shape_match_matrix`)

**Difficulty:** hard

**Skills:** meta-reasoning about shapes, pairwise comparison, matrix output

**Scaffold notes:**
- Order the components from left to right.
- Compare shapes up to translation only; ignore their colors.
- Write an 8 wherever two components have the same normalized shape.

**Written solution:** Sort the disconnected components from left to right. Compare every pair of components by normalized shape, ignoring color and absolute position. Output a matrix with 8 where the two compared components have the same shape and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_32_shape_match_matrix(g: Grid) -> Grid:
    comps = components4_any(g)
    comps.sort(key=lambda comp: (bbox(comp)[1], bbox(comp)[0]))
    crops = [offsets_to_grid(nonzero_offsets(comp_crop(g, comp)), color=1) for comp in comps]
    n = len(crops)
    out = zeros(n, n)
    for i in range(n):
        for j in range(n):
            if same_shape(crops[i], crops[j]):
                out[i][j] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 4 0 0 0
0 2 2 0 0 0 3 3 0 0 0 4 4 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 8
0 8 0
8 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 6 0 0 0 7 7 0 0
0 5 5 5 0 0 0 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 3 0 0 0 4 0 0
0 2 0 2 0 0 3 3 3 0 0 4 0 0
0 2 2 2 0 0 0 3 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0
0 8 0
0 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 7 7 0 0 0 0 8 0 0 0
0 6 6 0 0 0 0 0 7 7 0 0 0 8 8 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 8
0 8 0
8 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 0 0 0 4 4 0 0
0 2 2 0 0 0 3 3 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8
8 8 8
8 8 8
```

## Make a Local Transform Gallery Sorted by Width (`hard_33_local_transform_gallery_sorted_by_width`)

**Difficulty:** hard

**Skills:** local key-object binding, transform then sort, size-changing gallery layout

**Scaffold notes:**
- Each key belongs to the component directly below it.
- Transform each local component according to its own key.
- After transforming, sort the crops by descending width and pack them left to right.

**Written solution:** Bind each key cell to the component whose bounding box begins directly beneath it. Transform that local component according to the key, crop the transformed result tightly, sort all transformed crops by descending width, and then pack them left to right with one blank column between them.

**Program solution (Python reference):**
```python
def solve_hard_33_local_transform_gallery_sorted_by_width(g: Grid) -> Grid:
    key_positions = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v in (1,2,3,4)]
    gg = clone(g)
    for r, c, _ in key_positions:
        gg[r][c] = 0
    comps = components4_any(gg)
    items = []
    for kr, kc, key in key_positions:
        target = None
        for comp in comps:
            r0, c0, r1, c1 = bbox(comp)
            if kr == r0 - 1 and kc == c0:
                target = comp
                break
        if target is None:
            raise AssertionError("no target for key")
        crop = comp_crop(g, target)
        crop = transform_by_key(crop, key)
        items.append(crop)
    items.sort(key=lambda crop: (-dims(crop)[1], -dims(crop)[0]))
    return pack_horiz_top(items, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 8 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 7 8 8 0 0 0 0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 0 9 9 0 6 0
8 0 0 9 0 0 6 6
8 8 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 9 0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 7 0 9 0 0 6 6
8 8 7 0 9 9 0 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 7 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 7 7 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 7 0 0 0 1 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 6 0 0 6 0 9 9
0 7 7 0 6 6 0 0 9
7 7 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 7 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 0 0 0 7 0 8 0 0 9
7 7 0 0 7 8 8 0 9 9
0 7 6 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 8 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 7 8 8 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 7 6 0 8 8 7 0 6 6
7 7 0 0 8 0 7 0 6 0
7 0 0 0 0 0 0 0 0 0
```

## Build the Overlay Count Map from Normalized Components (`hard_34_overlay_count_map_from_components`)

**Difficulty:** hard

**Skills:** shape normalization, cellwise aggregation, count-to-color mapping

**Scaffold notes:**
- Normalize every component to the top-left corner of its own bounding box.
- Overlay the normalized masks on top of each other.
- Encode how many shapes cover each cell with a fixed count-to-color palette.

**Written solution:** Crop every connected component tightly and normalize it to the top-left. Overlay those normalized masks into a common canvas and count, cell by cell, how many components cover each position. Convert coverage counts to colors with the palette 1→2, 2→3, 3→4, and 4→6.

**Program solution (Python reference):**
```python
def solve_hard_34_overlay_count_map_from_components(g: Grid) -> Grid:
    crops = [offsets_to_grid(nonzero_offsets(comp_crop(g, comp)), color=1) for comp in components4_any(g)]
    return overlay_counts(crops)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 0
3 4 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 2
4 3
2 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 3 3 3 0 0 0 0
0 2 2 2 0 0 3 0 3 0 4 0 0
0 0 2 0 0 0 3 3 3 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 3 2
4 3 3
2 3 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 3 3 0 0 0 4 4 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 3 0
3 3 2
2 2 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 6 0 0 0 7 7 7 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
3 3 2
3 2 2
2 2 0
```

## Fill the Holed Component with the Key Color (`hard_35_fill_holed_component_with_key_color`)

**Difficulty:** hard

**Skills:** hole detection, component selection, size-changing fill

**Scaffold notes:**
- Only one component contains a true enclosed hole.
- Use the special key color to fill the hole, not the border color.
- Return a tight crop of the repaired component.

**Written solution:** Find the unique connected component that contains an enclosed hole. Crop that component tightly, identify the interior zero region that is not connected to the crop border, and fill that hole with the special key color while keeping the original outer border.

**Program solution (Python reference):**
```python
def solve_hard_35_fill_holed_component_with_key_color(g: Grid) -> Grid:
    key = next(v for row in g for v in row if v in (8,9))
    gg = [[0 if v in (8,9) else v for v in row] for row in g]
    for comp in components4_any(gg):
        crop = comp_crop(g, comp)
        filled = fill_holes_with_key(crop, key)
        if filled != crop:
            return filled
    raise AssertionError("no holed component")
```

**Train 1 input**
```text
8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 2 0 0 0 1 0 0 0 0
0 0 2 2 2 2 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 2
2 8 8 2
2 8 8 2
2 2 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 6 6 0 0 0
0 3 3 3 3 3 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 3 3
3 9 9 9 3
3 3 3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6
6 8 6
6 6 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 5 0 0 0
0 2 0 0 0 0 0 0 5 0 0 5 0 0 0
0 2 2 0 0 0 0 0 5 5 5 5 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 5 5 5
5 9 9 5
5 9 9 5
5 5 5 5
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8
```

**Test output**
```text
4 4 4 4 4
4 8 8 8 4
4 4 4 4 4
```
