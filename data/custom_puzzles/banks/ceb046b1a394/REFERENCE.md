# ARC Puzzle Bank — Sixteenth 21 Puzzles

This sixteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`106`–`112`) so it follows directly after the fifteenth bundle.
This volume pushes into a different mechanic mix than the last one: span filling, mirror completion, geometry reduction, component-ranked recoloring, ordered elbow routing, chamber gravity, cross-product galleries, scale-normalized shape matching, nearest-seed chamber filling, and library-sequence decoding.
It also introduces and reuses a few convenient primitives for solver work: `ordered_elbow_path`, `scale_normalized_signature`, `nearest_seed_chamber_fill`, and `transform_recolor_cross_product`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_sixteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_sixteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_sixteenth_21.md` — this human-readable catalog.

## Summary
### Easy (7)
- `easy_106_fill_row_or_column_spans` — **Fill the Row/Column Spans**
- `easy_107_complete_vertical_mirror` — **Complete the Vertical Mirror**
- `easy_108_reduce_rectangles_to_corners` — **Reduce Solid Rectangles to Corners**
- `easy_109_left_pack_each_row` — **Left-Pack Each Row**
- `easy_110_keep_centers_of_three_cell_lines` — **Keep the Centers of 3-Cell Lines**
- `easy_111_fill_component_bounding_boxes` — **Fill Each Component's Bounding Box**
- `easy_112_cast_rightward_rays_until_blockers` — **Cast Rightward Rays to the Blockers**

### Medium (7)
- `medium_106_crop_the_only_hollow_rectangle` — **Crop the Only Hollow Rectangle**
- `medium_107_transform_and_recolor_object_by_corner_codes` — **Transform and Recolor the Keyed Object**
- `medium_108_apply_gravity_inside_vertical_chambers` — **Apply Gravity Inside Vertical Chambers**
- `medium_109_recolor_components_by_area_rank` — **Recolor Components by Area Rank**
- `medium_110_select_by_most_frequent_legend_color_and_scale2` — **Scale the Object of the Most Frequent Legend Color**
- `medium_111_connect_same_color_pairs_with_ordered_elbows` — **Connect Same-Color Pairs with Ordered Elbows**
- `medium_112_pack_component_crops_by_width_ascending` — **Pack Component Crops by Width**

### Hard (7)
- `hard_106_build_transform_recolor_cross_product_gallery` — **Build the Transform/Recolor Cross-Product Gallery**
- `hard_107_build_scale_normalized_shape_equivalence_matrix` — **Build the Scale-Normalized Shape-Equivalence Matrix**
- `hard_108_fill_chambers_by_nearest_seed_manhattan` — **Fill Chambers by the Nearest Seed**
- `hard_109_select_shape_class_and_apply_transform_sequence` — **Select the Shape Class and Apply the Transform Sequence**
- `hard_110_overlay_elbow_paths_into_count_map` — **Overlay Elbow Paths into a Count Map**
- `hard_111_decode_library_sequence_into_strip` — **Decode the Library Sequence into a Strip**
- `hard_112_build_pairwise_intersection_gallery` — **Build the Pairwise-Intersection Gallery**

## Fill the Row/Column Spans (`easy_106_fill_row_or_column_spans`)

**Difficulty:** easy

**Skills:** color grouping, axis-aligned span filling, same-size transform

**Scaffold notes:**
- Group the nonzero cells by color.
- Each color appears exactly twice and the two cells share a row or a column.
- Fill the inclusive segment between the two endpoints.

**Written solution:** Each nonzero color marks the two ends of one straight segment. For every color, check whether its two cells lie in the same row or the same column, then fill every cell between them, keeping the color the same.

**Program solution (Python reference):**
```python
def solve_easy_106_fill_row_or_column_spans(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=cells
        if r0==r1:
            for c in range(min(c0,c1), max(c0,c1)+1):
                out[r0][c]=color
        elif c0==c1:
            for r in range(min(r0,r1), max(r0,r1)+1):
                out[r][c0]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 6 6 6 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 5 5 5 5 5 5 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0
0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 3
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 3 3 3 3
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 4 4 4 4 4 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Complete the Vertical Mirror (`easy_107_complete_vertical_mirror`)

**Difficulty:** easy

**Skills:** reflection symmetry, same-size copying, spatial completion

**Scaffold notes:**
- Use the vertical center line of the grid as the mirror axis.
- Every nonzero cell should also appear at its mirrored column.
- Keep the original cells and add the reflected ones.

**Written solution:** The given pattern is only half of a vertically symmetric design. Copy every nonzero cell to the column reflected across the vertical center line, leaving the original half in place.

**Program solution (Python reference):**
```python
def solve_easy_107_complete_vertical_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[r][w-1-c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 4 4 0 0 0 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0
0 2 2 0 0 0 2 2 0
0 0 4 4 0 4 4 0 0
0 0 0 4 4 4 0 0 0
7 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 3 3 3 0 0
0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 6 6 0
0 6 0 0 0 0 0 0 0 6 0
0 0 0 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
5 5 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 5 0 0 0 0 0 5 5
5 5 0 0 0 0 0 5 5
5 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0
0 4 0 0 0 0 0 0 0 4 0
0 4 4 0 0 0 0 0 4 4 0
0 0 4 4 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 2 2 0
0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 6 0 6
6 0 6 0 0 0 6 0 6
6 6 6 0 0 0 6 6 6
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Reduce Solid Rectangles to Corners (`easy_108_reduce_rectangles_to_corners`)

**Difficulty:** easy

**Skills:** object detection, bounding boxes, corner extraction

**Scaffold notes:**
- Each object is a solid rectangle of one color.
- Find the four corners of each rectangle's bounding box.
- Erase every other cell.

**Written solution:** Every nonzero object is already a filled rectangle. For each one, keep only the four corner cells of its bounding box and turn all remaining rectangle cells back to background.

**Program solution (Python reference):**
```python
def solve_easy_108_reduce_rectangles_to_corners(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        color=comp["color"]
        if comp["area"]==(r1-r0+1)*(c1-c0+1):
            out[r0][c0]=color
            out[r0][c1]=color
            out[r1][c0]=color
            out[r1][c1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 6 6 0
0 2 2 2 0 0 0 6 6 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 6 6 0
0 2 0 2 0 0 0 6 6 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 3 3 3 3 0 0 7 7 0
0 0 3 3 3 3 0 0 7 7 0
0 0 3 3 3 3 0 0 7 7 0
5 5 5 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 7 7 0
5 0 5 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 4 4 4
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 4 0 4
```

**Train 4 input**
```text
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0
0 2 2 2 0 0 0 8 8 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 6 0 0
0 0 0 0 6 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0
0 2 0 2 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Left-Pack Each Row (`easy_109_left_pack_each_row`)

**Difficulty:** easy

**Skills:** row-wise compaction, order preservation, same-size transform

**Scaffold notes:**
- Treat each row independently.
- Read the nonzero values from left to right.
- Rewrite that same sequence flush against the left edge.

**Written solution:** Within each row, ignore the zeros and preserve the left-to-right order of the colored cells. Then place that sequence at the far left of the same row and fill the remaining cells with zeros.

**Program solution (Python reference):**
```python
def solve_easy_109_left_pack_each_row(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        vals=[v for v in g[r] if v!=0]
        for c,v in enumerate(vals):
            out[r][c]=v
    return out
```

**Train 1 input**
```text
0 2 0 0 4 0 6 0 0
3 0 0 5 0 0 0 0 0
0 0 7 0 8 0 0 9 0
0 0 0 0 0 0 0 0 0
4 0 2 0 0 6 0 0 8
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 4 6 0 0 0 0 0 0
3 5 0 0 0 0 0 0 0
7 8 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 2 6 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 5 0 2 0 0 0 7 0
4 0 0 0 0 3 0 6 0 0
0 0 0 0 0 0 0 0 0 0
8 0 9 0 0 2 0 0 0 0
0 1 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 2 7 0 0 0 0 0 0 0
4 3 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 9 2 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 6 0 0 0 4 0 2
0 0 0 7 0 0 5 0
3 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0
2 0 9 0 6 0 0 0
```

**Train 3 output**
```text
6 4 2 0 0 0 0 0
7 5 0 0 0 0 0 0
3 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 9 6 0 0 0 0 0
```

**Train 4 input**
```text
0 0 3 0 0 5 0 7 0 0
8 0 0 0 4 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
6 0 1 0 0 0 9 0 0 0
0 5 0 0 3 0 0 0 2 0
```

**Train 4 output**
```text
3 5 7 0 0 0 0 0 0 0
8 4 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 1 9 0 0 0 0 0 0 0
5 3 2 0 0 0 0 0 0 0
```

**Test input**
```text
0 7 0 0 2 0 0 6 0
4 0 0 8 0 0 0 0 0
0 0 3 0 9 0 0 0 0
5 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 2 6 0 0 0 0 0 0
4 8 0 0 0 0 0 0 0
3 9 0 0 0 0 0 0 0
5 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Keep the Centers of 3-Cell Lines (`easy_110_keep_centers_of_three_cell_lines`)

**Difficulty:** easy

**Skills:** component parsing, line detection, center selection

**Scaffold notes:**
- Every object is a 3-cell horizontal or vertical line.
- Find the middle cell of each line.
- Drop the two endpoints.

**Written solution:** Each colored component is a straight line of exactly three cells. Replace every such line by just its center cell, keeping the color unchanged.

**Program solution (Python reference):**
```python
def solve_easy_110_keep_centers_of_three_cell_lines(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        if comp["area"]==3 and ((r1-r0==0 and c1-c0==2) or (r1-r0==2 and c1-c0==0)):
            out[(r0+r1)//2][(c0+c1)//2]=comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 7 7 7 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0
0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Fill Each Component's Bounding Box (`easy_111_fill_component_bounding_boxes`)

**Difficulty:** easy

**Skills:** component segmentation, bounding-box abstraction, same-size transform

**Scaffold notes:**
- Find each connected component separately.
- Compute its minimal bounding rectangle.
- Fill that whole rectangle with the component's color.

**Written solution:** Every object should be replaced by the solid rectangle that spans its extent. For each connected component, compute its bounding box and fill every cell inside that box with the component's color.

**Program solution (Python reference):**
```python
def solve_easy_111_fill_component_bounding_boxes(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        color=comp["color"]
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 6 6 6
0 2 0 0 0 0 0 0 6 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 6 6 6
0 2 2 0 0 0 0 6 6 6
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 7 7 0
0 3 3 0 0 0 0 0 7 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 7 7 0
0 3 3 0 0 0 0 0 7 7 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 2 0 2 0 0
0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 4 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0
0 0 0 0 2 2 2 0 0
0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 4 4 0
```

**Train 4 input**
```text
0 9 9 9 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 0 0 5 5 0
0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9 9 9 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 5 5 5
0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 8 8 0
0 6 6 0 0 0 0 8 0 0
0 6 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 8 8 0
0 6 6 0 0 0 0 8 8 0
0 6 6 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Cast Rightward Rays to the Blockers (`easy_112_cast_rightward_rays_until_blockers`)

**Difficulty:** easy

**Skills:** directed extension, row reasoning, blocker handling

**Scaffold notes:**
- Each active row contains one emitter color and a blocker color 8 to its right.
- Start from the emitter and move right.
- Fill until the cell immediately before the blocker.

**Written solution:** In every active row, a colored emitter sends a horizontal ray toward the right until it reaches the gray blocker. Copy the emitter's color into every background cell between the emitter and the blocker.

**Program solution (Python reference):**
```python
def solve_easy_112_cast_rightward_rays_until_blockers(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        emitter=None
        blocker=None
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=8 and emitter is None:
                emitter=(c,v)
            elif v==8 and emitter is not None:
                blocker=c
                break
        if emitter is not None and blocker is not None:
            c0,color=emitter
            for c in range(c0+1, blocker):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 8
```

**Train 2 output**
```text
3 3 3 3 3 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 2 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 8
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 8
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
6 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
6 6 6 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Crop the Only Hollow Rectangle (`medium_106_crop_the_only_hollow_rectangle`)

**Difficulty:** medium

**Skills:** topology, object selection, cropping

**Scaffold notes:**
- Among several objects, exactly one is a hollow rectangular ring.
- Ignore the distractor shapes.
- Return only the cropped ring.

**Written solution:** The target object is the unique component whose bounding box is a rectangle outline with an empty interior. Find that hollow rectangle and output only its cropped bounding box.

**Program solution (Python reference):**
```python
def solve_medium_106_crop_the_only_hollow_rectangle(g):
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        hh=r1-r0+1
        ww=c1-c0+1
        color=comp["color"]
        if hh>=3 and ww>=3 and comp["area"]==2*hh+2*ww-4:
            ok=True
            for rr in range(r0,r1+1):
                for cc in range(c0,c1+1):
                    border = rr in (r0,r1) or cc in (c0,c1)
                    v=g[rr][cc]
                    if border and v!=color:
                        ok=False
                    if (not border) and v!=0:
                        ok=False
            if ok:
                return crop_bbox(g, comp["bbox"])
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0
4 0 0 0 0 0 0 6 6 0 0
4 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 2
2 0 0 2
2 2 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 3 3 3 0 0 0
0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3
3 0 3
3 0 3
3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8 8
8 0 0 0 8
8 8 8 8 8
```

**Train 4 input**
```text
3 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 5 5 0 0
3 3 0 0 0 0 0 0 5 5 0
0 0 6 6 6 6 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6
6 0 0 6
6 0 0 6
6 6 6 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 4 0 4 0 0
0 2 2 2 0 0 0 4 0 4 0 0
0 0 2 0 0 0 0 4 4 4 0 0
0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 4 4
4 0 4
4 0 4
4 0 4
4 4 4
```

## Transform and Recolor the Keyed Object (`medium_107_transform_and_recolor_object_by_corner_codes`)

**Difficulty:** medium

**Skills:** code decoding, geometric transforms, recoloring

**Scaffold notes:**
- The top-left cell gives the transform code: identity, clockwise, 180°, or counterclockwise.
- The top-right cell gives the final output color.
- Crop the object, transform it, then recolor every nonzero cell.

**Written solution:** Read the transform instruction from the top-left corner and the target color from the top-right corner. Remove the codes, crop the remaining object, apply the indicated rotation, and recolor the transformed object to the target color.

**Program solution (Python reference):**
```python
def solve_medium_107_transform_and_recolor_object_by_corner_codes(g):
    transform_code=g[0][0]
    target_color=g[0][-1]
    work=clone(g)
    work[0][0]=0
    work[0][-1]=0
    obj=crop_nonzero(work)
    obj=apply_transform_code(obj, transform_code)
    return [[target_color if v!=0 else 0 for v in row] for row in obj]
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8
8 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6
6 6
6 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 2 0
2 2 2
```

**Train 4 input**
```text
1 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9
9 9
9 0
```

**Test input**
```text
2 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 5 5
5 5 0
5 0 0
```

## Apply Gravity Inside Vertical Chambers (`medium_108_apply_gravity_inside_vertical_chambers`)

**Difficulty:** medium

**Skills:** gravity simulation, wall handling, column reasoning

**Scaffold notes:**
- The full-height 8-columns are walls.
- Treat each chamber separately and process each column independently.
- Let colored cells fall to the bottom while keeping their order.

**Written solution:** Gray columns split the board into vertical chambers. Inside each chamber, the colored cells in every column fall straight downward to the lowest available positions, while the wall columns stay fixed.

**Program solution (Python reference):**
```python
def solve_medium_108_apply_gravity_inside_vertical_chambers(g):
    h,w=dims(g)
    out=zeros(h,w)
    wall_cols=[c for c in range(w) if all(g[r][c]==8 for r in range(h))]
    for c in wall_cols:
        for r in range(h):
            out[r][c]=8
    boundaries=[-1]+wall_cols+[w]
    for left,right in zip(boundaries, boundaries[1:]):
        for c in range(left+1, right):
            vals=[g[r][c] for r in range(h) if g[r][c] not in (0,8)]
            rr=h-1
            for v in reversed(vals):
                out[rr][c]=v
                rr -= 1
    return out
```

**Train 1 input**
```text
2 0 0 8 0 3 0 8 0 0 0
0 0 6 8 0 0 0 8 7 0 0
0 4 0 8 0 0 0 8 0 0 4
0 0 0 8 0 0 5 8 0 0 0
0 0 0 8 0 0 0 8 0 2 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
```

**Train 1 output**
```text
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
2 4 6 8 0 3 5 8 7 2 4
```

**Train 2 input**
```text
5 0 0 0 8 0 0 0 7 0
0 0 0 0 8 6 0 0 0 0
0 2 0 0 8 0 0 0 0 4
0 0 0 8 8 0 0 0 0 0
0 0 0 0 8 0 3 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
5 2 0 0 8 6 3 0 7 4
```

**Train 3 input**
```text
3 0 8 2 0 0 8 0 0 8 7 0
0 5 8 0 0 0 8 6 0 8 0 0
0 0 8 0 4 0 8 0 0 8 0 2
0 0 8 0 0 0 8 0 8 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
```

**Train 3 output**
```text
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
0 0 8 0 0 0 8 0 0 8 0 0
3 5 8 2 4 0 8 6 0 8 7 2
```

**Train 4 input**
```text
0 9 0 0 0 8 8 0 0 0 0
0 0 0 0 2 8 0 0 0 0 6
0 0 0 0 0 8 0 5 0 0 0
0 0 4 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 3 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 9 4 0 2 8 0 5 0 3 6
```

**Test input**
```text
0 4 0 8 0 0 0 0 8 3 0
2 0 0 8 0 0 5 0 8 0 0
0 0 0 8 0 7 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 6
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
```

**Test output**
```text
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 8 0 0
2 4 0 8 0 7 5 0 8 3 6
```

## Recolor Components by Area Rank (`medium_109_recolor_components_by_area_rank`)

**Difficulty:** medium

**Skills:** component comparison, ranking, palette reassignment

**Scaffold notes:**
- Measure the size of every connected component.
- Sort them from smallest to largest.
- Recolor the ranked components with the fixed palette 2, 4, 6, 8.

**Written solution:** The objects keep their shapes and positions, but their colors are reassigned according to area rank. Sort the connected components from smallest to largest and recolor them in order with 2, then 4, then 6, then 8.

**Program solution (Python reference):**
```python
def solve_medium_109_recolor_components_by_area_rank(g):
    h,w=dims(g)
    out=zeros(h,w)
    comps=sorted(connected_components(g), key=lambda comp: (comp["area"], comp["bbox"][0], comp["bbox"][1]))
    palette=[2,4,6,8]
    for comp,new_color in zip(comps, palette):
        for r,c in comp["cells"]:
            out[r][c]=new_color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
8 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
6 6 0 0 0 0 0 3 3 3 0 0
6 6 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
6 6 0 0 0 0 0 8 8 8 0 0
6 6 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 7 7 0 0
0 9 9 0 0 0 7 7 0 0
0 9 9 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 8 8 0 0
0 6 6 0 0 0 8 8 0 0
0 6 6 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 8 0 0 0 5 5 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 8 0 0 0 6 6 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 7 7 7 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 4 4 4 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Scale the Object of the Most Frequent Legend Color (`medium_110_select_by_most_frequent_legend_color_and_scale2`)

**Difficulty:** medium

**Skills:** frequency counting, keyed selection, cropping and scaling

**Scaffold notes:**
- Count the nonzero colors in the top legend row.
- The most frequent legend color names the target object below.
- Crop that object and scale it by 2 in both dimensions.

**Written solution:** The top row is a legend, and its most frequent nonzero color tells you which object to extract from the body. Find the object of that color, crop its bounding box, and enlarge it by a factor of 2.

**Program solution (Python reference):**
```python
def solve_medium_110_select_by_most_frequent_legend_color_and_scale2(g):
    counts=collections.Counter(v for v in g[0] if v!=0)
    key=max(counts.items(), key=lambda kv: (kv[1], -kv[0]))[0]
    work=[row[:] for row in g[1:]]
    candidates=[comp for comp in connected_components(work) if comp["color"]==key]
    comp=max(candidates, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return scale2(crop_bbox(work, comp["bbox"]))
```

**Train 1 input**
```text
2 5 2 3 2 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 3 3 3 0 0 0
0 2 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0
2 2 0 0
2 2 0 0
2 2 0 0
2 2 2 2
2 2 2 2
```

**Train 2 input**
```text
4 6 4 2 4 6 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0
6 6 0 0 0 0 2 2 0 0 0 0
6 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 4 0 0
4 4 4 4 0 0
0 0 4 4 4 4
0 0 4 4 4 4
```

**Train 3 input**
```text
7 3 7 5 7 7 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 0 0
7 7 0 0
7 7 0 0
7 7 0 0
7 7 7 7
7 7 7 7
```

**Train 4 input**
```text
6 2 6 6 4 6 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
6 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
6 6 0 0
6 6 0 0
```

**Test input**
```text
5 8 5 3 5 2 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 8 8 0
0 0 0 0 0 0 3 0 0 8 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 5 0 0 0 0
5 5 0 0 0 0
5 5 5 5 0 0
5 5 5 5 0 0
0 0 5 5 5 5
0 0 5 5 5 5
```

## Connect Same-Color Pairs with Ordered Elbows (`medium_111_connect_same_color_pairs_with_ordered_elbows`)

**Difficulty:** medium

**Skills:** pairing by color, Manhattan routing, same-size drawing

**Scaffold notes:**
- Each nonzero color appears exactly twice.
- Sort the pair by row so the upper endpoint is first.
- Draw a horizontal segment first, then a vertical segment down to the other endpoint.

**Written solution:** Every color defines one pair of endpoints. For each pair, start from the upper endpoint, move horizontally until you reach the destination column, and then move vertically to the lower endpoint, coloring the whole elbow path.

**Program solution (Python reference):**
```python
def solve_medium_111_connect_same_color_pairs_with_ordered_elbows(g):
    h,w=dims(g)
    out=zeros(h,w)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=sorted(cells)
        step=1 if c1>=c0 else -1
        for c in range(c0, c1+step, step):
            out[r0][c]=color
        step=1 if r1>=r0 else -1
        for r in range(r0, r1+step, step):
            out[r][c1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 4 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 7
```

**Train 1 output**
```text
0 0 0 0 0 0 4 4 4 0
0 2 2 2 2 2 4 0 0 0
0 0 0 0 0 2 4 0 0 0
0 0 0 0 0 2 4 0 0 0
0 0 0 0 0 2 4 0 0 0
0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 4 0 0 7
0 0 0 0 0 0 0 0 0 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 6 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 0 0
3 3 3 3 0 6 0 0 0 0 0
0 0 0 3 0 6 0 0 0 0 0
0 0 0 3 0 6 0 2 2 2 2
0 0 0 3 0 6 0 2 0 0 0
0 0 0 3 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0 0
```

**Train 3 input**
```text
0 0 8 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8 8 8 8 8 0 0
2 2 2 2 0 0 8 0 0
0 0 0 2 4 4 4 4 4
0 0 0 2 4 0 8 0 0
0 0 0 2 4 0 8 0 0
0 0 0 0 4 0 8 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
```

**Train 4 output**
```text
3 3 3 0 0 0 0 0 0 0
0 0 3 0 5 5 5 5 0 0
0 0 3 0 5 0 0 0 0 0
0 0 3 0 5 0 7 7 7 7
0 0 3 0 5 0 7 0 0 0
0 0 3 0 5 0 7 0 0 0
0 0 3 0 5 0 7 0 0 0
0 0 0 0 5 0 7 0 0 0
0 0 0 0 5 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 9 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 2 2 2 2 2 0
0 0 0 0 2 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 0 0 0 2 6 0 0 0 0
0 0 0 0 2 6 0 0 0 0
9 9 9 9 0 6 0 0 0 0
0 0 0 9 0 6 0 0 0 0
0 0 0 9 0 6 0 0 0 0
0 0 0 9 0 0 0 0 0 0
```

## Pack Component Crops by Width (`medium_112_pack_component_crops_by_width_ascending`)

**Difficulty:** medium

**Skills:** cropping, sorting by geometry, gallery packing

**Scaffold notes:**
- Crop every component to its own bounding box.
- Sort the cropped pieces by increasing width.
- Pack them left to right with one blank column between pieces.

**Written solution:** The output is a gallery of the cropped components. Extract each component's bounding box, order the crops from narrowest to widest, and place them side by side with a single zero column between them.

**Program solution (Python reference):**
```python
def solve_medium_112_pack_component_crops_by_width_ascending(g):
    parts=[]
    for comp in connected_components(g):
        part=crop_bbox(g, comp["bbox"])
        parts.append((len(part[0]), len(part), comp["area"], comp["color"], part))
    parts.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
    height=max(t[1] for t in parts)
    width=sum(t[0] for t in parts)+len(parts)-1
    out=zeros(height,width)
    x=0
    for _,_,_,_,part in parts:
        place(out, part, 0, x)
        x += len(part[0]) + 1
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0
2 0 0 4 4 0 0 0 0 0 0 0
2 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 4 4 0 6 6 6 0 8 8 8 8
2 0 4 0 0 0 6 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 7 7 0 0 0
0 3 0 0 0 0 0 0 0 7 7 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 0 5 0 0 7 7 0 0 2 2 2 2
3 0 5 0 0 0 7 7 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 8 0 0 0 0 0 0
4 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 8 8 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 6 6 0 8 0 0 0 3 3 3 3
4 0 6 0 0 8 8 0 0 0 0 0 0
4 0 0 0 0 0 8 8 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 7 7 7 0 0 0 0
5 0 0 0 0 0 0 7 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 0 2 2 0 7 7 7 0 9 9 9 9
5 0 2 2 0 0 7 0 0 0 0 0 0
5 0 2 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
8 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 0 3 3 0 5 5 0 0 2 2 2 2
8 0 3 0 0 0 5 5 0 0 0 0 0
```

## Build the Transform/Recolor Cross-Product Gallery (`hard_106_build_transform_recolor_cross_product_gallery`)

**Difficulty:** hard

**Skills:** legend decoding, cross-product construction, panel galleries

**Scaffold notes:**
- The left-side codes choose transforms and the top codes choose colors.
- The prototype lives in the lower-right 3×3 block.
- Build a gallery whose rows are transforms and whose columns are recolors.

**Written solution:** Read three transform codes from the left and three color codes from the top. For every row/column combination, transform the prototype shape accordingly, recolor it to the chosen top color, and place the result in the corresponding 3×3 gallery panel.

**Program solution (Python reference):**
```python
def solve_hard_106_build_transform_recolor_cross_product_gallery(g):
    transform_codes=[g[r][0] for r in (1,3,5)]
    color_codes=[g[0][c] for c in (1,3,5)]
    proto=[row[4:7] for row in g[4:7]]
    proto_bin=[[1 if v!=0 else 0 for v in row] for row in proto]
    out=zeros(11,11)
    for i,tcode in enumerate(transform_codes):
        transformed=apply_transform_code(proto_bin, tcode)
        for j,color in enumerate(color_codes):
            panel=[[color if v!=0 else 0 for v in row] for row in transformed]
            place(out, panel, 4*i, 4*j)
    return out
```

**Train 1 input**
```text
0 2 0 5 0 8 0
1 0 0 0 0 0 0
0 0 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 1 0 0
4 0 0 0 1 1 1
0 0 0 0 0 0 1
```

**Train 1 output**
```text
2 0 0 0 5 0 0 0 8 0 0
2 2 2 0 5 5 5 0 8 8 8
0 0 2 0 0 0 5 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 5 5 0 0 8 8
0 2 0 0 0 5 0 0 0 8 0
2 2 0 0 5 5 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 5 5 0 0 8 8
0 2 0 0 0 5 0 0 0 8 0
2 2 0 0 5 5 0 0 8 8 0
```

**Train 2 input**
```text
0 4 0 6 0 9 0
2 0 0 0 0 0 0
0 0 0 0 0 0 0
3 0 0 0 0 0 0
0 0 0 0 0 1 0
1 0 0 0 1 1 0
0 0 0 0 1 0 0
```

**Train 2 output**
```text
4 4 0 0 6 6 0 0 9 9 0
0 4 4 0 0 6 6 0 0 9 9
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 6 0 0 0 9
0 4 4 0 0 6 6 0 0 9 9
0 4 0 0 0 6 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 6 0 0 0 9 0
4 4 0 0 6 6 0 0 9 9 0
4 0 0 0 6 0 0 0 9 0 0
```

**Train 3 input**
```text
0 3 0 7 0 2 0
4 0 0 0 0 0 0
0 0 0 0 0 0 0
1 0 0 0 0 0 0
0 0 0 0 1 1 0
3 0 0 0 0 1 0
0 0 0 0 0 1 1
```

**Train 3 output**
```text
0 0 3 0 0 0 7 0 0 0 2
3 3 3 0 7 7 7 0 2 2 2
3 0 0 0 7 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 7 7 0 0 2 2 0
0 3 0 0 0 7 0 0 0 2 0
0 3 3 0 0 7 7 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 7 7 0 0 2 2 0
0 3 0 0 0 7 0 0 0 2 0
0 3 3 0 0 7 7 0 0 2 2
```

**Train 4 input**
```text
0 8 0 5 0 2 0
3 0 0 0 0 0 0
0 0 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 1 0 1
4 0 0 0 1 1 1
0 0 0 0 0 0 1
```

**Train 4 output**
```text
8 0 0 0 5 0 0 0 2 0 0
8 8 8 0 5 5 5 0 2 2 2
8 0 8 0 5 0 5 0 2 0 2
0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 5 5 0 0 2 2
0 8 0 0 0 5 0 0 0 2 0
8 8 8 0 5 5 5 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 5 5 5 0 2 2 2
0 8 0 0 0 5 0 0 0 2 0
8 8 0 0 5 5 0 0 2 2 0
```

**Test input**
```text
0 6 0 3 0 9 0
1 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 0
0 0 0 0 0 1 1
2 0 0 0 1 1 0
0 0 0 0 0 1 0
```

**Test output**
```text
0 6 6 0 0 3 3 0 0 9 9
6 6 0 0 3 3 0 0 9 9 0
0 6 0 0 0 3 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 3 0 0 0 9 0 0
6 6 6 0 3 3 3 0 9 9 9
0 6 0 0 0 3 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 3 0 0 0 9 0
6 6 6 0 3 3 3 0 9 9 9
0 0 6 0 0 0 3 0 0 0 9
```

## Build the Scale-Normalized Shape-Equivalence Matrix (`hard_107_build_scale_normalized_shape_equivalence_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, exact 2× downscaling, relation matrices

**Scaffold notes:**
- The input contains three separate panels.
- Normalize each shape by reducing exact 2× copies back to their smaller binary form.
- Mark matrix entries where the normalized shapes match.

**Written solution:** Compare the three panel objects after stripping color and undoing any exact 2× scaling. Output a 3×3 relation matrix with 8 wherever two panels reduce to the same normalized binary shape.

**Program solution (Python reference):**
```python
def solve_hard_107_build_scale_normalized_shape_equivalence_matrix(g):
    panels=[[row[s:s+6] for row in g] for s in (0,7,14)]
    sigs=[binary_signature_scale_normalized(panel) for panel in panels]
    out=zeros(3,3)
    for i,a in enumerate(sigs):
        for j,b in enumerate(sigs):
            if a==b:
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 2 0 0 0 0 0 3 3 3 0 0
0 0 2 2 0 0 0 0 2 2 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
4 4 4 4 0 0 0 0 4 4 0 0 0 0 0 0 2 0 0 0
0 0 4 4 4 4 0 0 0 4 4 0 0 0 0 0 2 2 0 0
0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 3 3 3 3 3 3 0 0 4 4 0 0 0
0 0 3 0 0 0 0 0 0 3 3 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 4 input**
```text
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3
0 2 2 0 0 0 0 0 3 3 3 0 0 0 3 3 3 3 3 3
0 2 2 0 0 0 0 0 0 3 0 0 0 0 0 0 3 3 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0
0 8 8
0 8 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0 0 0 4 4 4 4 0 0
0 4 4 0 0 0 0 0 2 2 0 0 0 0 4 4 4 4 0 0
0 0 4 4 0 0 0 0 2 2 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 2 2 2 2 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 0 8
0 8 0
8 0 8
```

## Fill Chambers by the Nearest Seed (`hard_108_fill_chambers_by_nearest_seed_manhattan`)

**Difficulty:** hard

**Skills:** chamber segmentation, distance transforms, tie-breaking

**Scaffold notes:**
- Walls are color 8 and split the grid into independent chambers.
- Within each chamber, nonzero non-wall cells are seeds.
- Fill every zero with the color of the nearest seed by Manhattan distance, breaking ties toward the smaller color.

**Written solution:** Treat every wall-bounded chamber separately. In each chamber, colored seed cells radiate outward, and every empty cell takes the color of the closest seed under Manhattan distance; if two seeds are equally close, choose the smaller color.

**Program solution (Python reference):**
```python
def solve_hard_108_fill_chambers_by_nearest_seed_manhattan(g):
    h,w=dims(g)
    out=clone(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==8 or seen[r][c]:
                continue
            seen[r][c]=True
            q=collections.deque([(r,c)])
            cells=[]
            seeds=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                if g[rr][cc] not in (0,8):
                    seeds.append((rr,cc,g[rr][cc]))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]!=8 and not seen[nr][nc]:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            for rr,cc in cells:
                if g[rr][cc]==0 and seeds:
                    best=min(((abs(rr-sr)+abs(cc-sc), color) for sr,sc,color in seeds), key=lambda t: (t[0], t[1]))
                    out[rr][cc]=best[1]
    return out
```

**Train 1 input**
```text
0 0 0 0 8 0 0 0 0
0 2 0 0 8 0 5 0 0
0 0 0 4 8 0 0 3 0
8 8 8 8 8 8 8 8 8
0 0 0 2 8 0 7 0 0
0 6 0 0 8 0 0 4 0
0 0 0 0 8 0 0 0 0
```

**Train 1 output**
```text
2 2 2 4 8 5 5 3 3
2 2 2 4 8 5 5 3 3
2 2 4 4 8 3 3 3 3
8 8 8 8 8 8 8 8 8
6 6 2 2 8 7 7 4 4
6 6 6 2 8 4 4 4 4
6 6 6 2 8 4 4 4 4
```

**Train 2 input**
```text
0 0 0 8 0 0 0 8 0 0
0 3 0 8 0 2 0 8 0 0
0 0 5 8 0 0 0 8 0 0
0 0 0 8 0 0 6 8 0 0
8 8 8 8 8 8 8 8 8 8
0 4 0 8 0 9 0 8 0 0
0 0 7 8 0 0 0 8 2 0
0 0 0 8 0 0 0 8 0 0
```

**Train 2 output**
```text
3 3 3 8 2 2 2 8 0 0
3 3 3 8 2 2 2 8 0 0
3 3 5 8 2 2 6 8 0 0
3 3 5 8 6 6 6 8 0 0
8 8 8 8 8 8 8 8 8 8
4 4 4 8 9 9 9 8 2 2
4 4 7 8 9 9 9 8 2 2
4 4 7 8 9 9 9 8 2 2
```

**Train 3 input**
```text
0 2 0 0 0 8 0 4 0 0
0 0 0 6 0 8 0 0 5 0
8 8 8 8 8 8 8 8 8 8
0 7 0 0 0 8 0 0 0 0
0 0 0 2 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 3 0 0
```

**Train 3 output**
```text
2 2 2 6 6 8 4 4 4 4
2 2 6 6 6 8 4 4 5 5
8 8 8 8 8 8 8 8 8 8
7 7 7 2 2 8 0 0 0 0
7 7 2 2 2 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 3 3 3 3
```

**Train 4 input**
```text
0 0 8 0 0 0 8 0 0
5 0 8 0 7 0 8 0 0
0 2 8 0 0 4 8 0 0
8 8 8 8 8 8 8 8 8
0 0 8 0 0 0 8 0 0
6 0 8 0 0 0 8 2 0
0 3 8 0 0 0 8 0 9
0 0 8 0 0 0 8 0 0
```

**Train 4 output**
```text
5 2 8 7 7 4 8 0 0
5 2 8 7 7 4 8 0 0
2 2 8 4 4 4 8 0 0
8 8 8 8 8 8 8 8 8
6 3 8 0 0 0 8 2 2
6 3 8 0 0 0 8 2 2
3 3 8 0 0 0 8 2 9
3 3 8 0 0 0 8 2 9
```

**Test input**
```text
0 0 0 0 0 8 0 0 0 0 0
0 4 0 0 0 8 0 6 0 0 0
0 0 0 2 0 8 0 0 0 3 0
8 8 8 8 8 8 8 8 8 8 8
0 5 0 0 0 8 0 2 0 0 0
0 0 0 0 7 8 0 0 0 9 0
0 0 0 0 0 8 0 0 0 0 0
```

**Test output**
```text
4 4 4 2 2 8 6 6 6 3 3
4 4 4 2 2 8 6 6 6 3 3
4 4 2 2 2 8 6 6 3 3 3
8 8 8 8 8 8 8 8 8 8 8
5 5 5 5 7 8 2 2 2 9 9
5 5 5 7 7 8 2 2 9 9 9
5 5 5 7 7 8 2 2 9 9 9
```

## Select the Shape Class and Apply the Transform Sequence (`hard_109_select_shape_class_and_apply_transform_sequence`)

**Difficulty:** hard

**Skills:** shape classification, symbolic transform sequences, cropping

**Scaffold notes:**
- The first top-row code names a shape class: L, T, zig, or P.
- The next two top-row codes are transform steps applied in order.
- Find the matching object below, crop it, then run the two-step transform sequence.

**Written solution:** The header specifies both which object class to choose and how to transform it. Match the requested shape class among the body objects, crop that object, and apply the two transform codes in sequence to produce the output.

**Program solution (Python reference):**
```python
def solve_hard_109_select_shape_class_and_apply_transform_sequence(g):
    shape_code, step1, step2 = g[0][0], g[0][1], g[0][2]
    library={
        1: normalize_binary([[1,0],[1,0],[1,1]]),
        2: normalize_binary([[1,1,1],[0,1,0]]),
        3: normalize_binary([[1,1,0],[0,1,1]]),
        4: normalize_binary([[1,1],[1,1],[1,0]]),
    }
    target=library[shape_code]
    work=[row[:] for row in g[1:]]
    for comp in connected_components(work):
        cropped=crop_bbox(work, comp["bbox"])
        if normalize_binary(cropped)==target:
            out=apply_transform_code(cropped, step1)
            out=apply_transform_code(out, step2)
            return out
    return [[0]]
```

**Train 1 input**
```text
1 2 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 4 4 0 0 0
0 2 0 0 0 0 4 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2
0 0 2
```

**Train 2 input**
```text
2 5 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 7 7 7 0 0 0
3 3 0 0 0 0 7 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 5 0 0
```

**Train 2 output**
```text
0 7
7 7
0 7
```

**Train 3 input**
```text
3 4 3 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
4 4 4 0 0 2 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8
8 8
8 0
```

**Train 4 input**
```text
4 2 2 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 6 6 0 0 0 0
3 3 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9
9 9
9 9
```

**Test input**
```text
1 5 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 7 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7
7 0
7 0
```

## Overlay Elbow Paths into a Count Map (`hard_110_overlay_elbow_paths_into_count_map`)

**Difficulty:** hard

**Skills:** path overlay, count accumulation, value remapping

**Scaffold notes:**
- Use the same ordered-elbow routing as in the medium elbow task.
- This time, count how many elbow paths cover each cell.
- Map coverage counts 1→3, 2→6, and 3 or more→9.

**Written solution:** Connect every same-color endpoint pair with the ordered elbow path. Instead of preserving the original colors, count how many paths pass through each cell and convert those counts into the palette 3, 6, and 9.

**Program solution (Python reference):**
```python
def solve_hard_110_overlay_elbow_paths_into_count_map(g):
    h,w=dims(g)
    counts=zeros(h,w)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for cells in groups.values():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=sorted(cells)
        step=1 if c1>=c0 else -1
        for c in range(c0, c1+step, step):
            counts[r0][c]+=1
        step=1 if r1>=r0 else -1
        for r in range(r0, r1+step, step):
            counts[r][c1]+=1
    palette={1:3,2:6}
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if counts[r][c]>=3:
                out[r][c]=9
            elif counts[r][c] in palette:
                out[r][c]=palette[counts[r][c]]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 4 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
```

**Train 1 output**
```text
0 0 0 0 6 3 3 3 3 0
0 3 3 3 6 6 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
3 3 3 3 6 6 6 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 3 6 0 0 0
3 3 3 6 0 0 0 3 0 0 0
0 0 0 3 0 6 3 6 3 3 3
0 0 0 3 0 3 0 3 0 0 0
0 0 0 3 0 3 0 3 0 0 0
0 0 0 3 0 3 0 3 0 0 0
0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
```

**Train 3 output**
```text
3 3 3 3 3 6 0 0 0
0 0 6 3 3 6 3 3 0
0 0 3 0 0 3 0 0 0
0 0 3 0 6 6 3 3 3
0 0 3 0 3 3 0 0 0
0 0 3 0 3 3 0 0 0
0 0 3 0 3 0 0 0 0
0 0 3 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 2 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 6 3 3 3 3 3
0 0 0 0 3 0 0 0 0 0
0 3 3 3 6 3 6 0 0 0
0 0 0 0 3 0 3 0 0 0
3 3 3 6 3 0 3 0 0 0
0 0 0 3 3 0 3 0 0 0
0 0 0 3 3 0 3 0 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 3 0 0 0 0 0 0
```

**Test input**
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
```

**Test output**
```text
3 3 3 3 3 6 0 0 0 0
0 0 0 6 3 6 3 3 3 0
0 0 0 3 0 3 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 0 3 6 6 3 3 3 3
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
```

## Decode the Library Sequence into a Strip (`hard_111_decode_library_sequence_into_strip`)

**Difficulty:** hard

**Skills:** library lookup, sequence decoding, transformed strip assembly

**Scaffold notes:**
- The top area contains three library panels.
- The bottom row is a sequence of (library index, transform code) pairs.
- Emit the chosen transformed library objects left to right as one strip.

**Written solution:** Interpret the bottom-row code pairs as instructions that choose one library panel and one transform for each slot. Apply each instruction to the corresponding 3×3 library object and concatenate the transformed results into a horizontal strip.

**Program solution (Python reference):**
```python
def solve_hard_111_decode_library_sequence_into_strip(g):
    libs=[[row[s:s+3] for row in g[:3]] for s in (0,4,8)]
    seq=[(g[4][0],g[4][1]), (g[4][3],g[4][4]), (g[4][6],g[4][7]), (g[4][9],g[4][10])]
    out=zeros(3,15)
    x=0
    for idx,tcode in seq:
        panel=apply_transform_code(libs[idx-1], tcode)
        place(out, panel, 0, x)
        x += 4
    return out
```

**Train 1 input**
```text
2 0 0 0 0 3 0 0 4 4 0
2 2 2 0 3 3 0 0 0 4 0
0 0 2 0 3 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0
1 1 0 2 2 0 3 4 0 1 3
```

**Train 1 output**
```text
2 0 0 0 3 3 0 0 0 0 4 0 2 0 0
2 2 2 0 0 3 3 0 4 4 4 0 2 2 2
0 0 2 0 0 0 0 0 4 0 0 0 0 0 2
```

**Train 2 input**
```text
5 5 0 0 0 6 6 0 7 0 7
0 5 0 0 6 6 0 0 7 7 7
0 5 5 0 0 6 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
3 2 0 1 4 0 2 1 0 3 3
```

**Train 2 output**
```text
0 7 7 0 0 0 5 0 0 6 6 0 7 0 0
0 7 0 0 5 5 5 0 6 6 0 0 7 7 7
7 7 7 0 5 0 0 0 0 6 0 0 7 0 7
```

**Train 3 input**
```text
8 0 0 0 0 2 0 0 3 3 0
8 8 0 0 2 2 2 0 3 0 0
0 8 8 0 0 0 2 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
2 3 0 3 1 0 1 2 0 2 4
```

**Train 3 output**
```text
2 0 0 0 3 3 0 0 0 8 8 0 0 2 2
2 2 2 0 3 0 0 0 8 8 0 0 2 2 0
0 2 0 0 3 3 0 0 8 0 0 0 0 2 0
```

**Train 4 input**
```text
4 4 4 0 0 5 5 0 6 6 0
0 4 0 0 5 5 0 0 0 6 6
0 4 0 0 0 5 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
1 4 0 2 2 0 3 3 0 1 1
```

**Train 4 output**
```text
4 0 0 0 0 5 0 0 6 0 0 0 4 4 4
4 4 4 0 5 5 5 0 6 6 0 0 0 4 0
4 0 0 0 0 0 5 0 0 6 6 0 0 4 0
```

**Test input**
```text
7 0 0 0 0 8 0 0 2 2 0
7 7 7 0 8 8 8 0 0 2 0
0 0 7 0 0 8 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
2 1 0 3 4 0 1 2 0 2 3
```

**Test output**
```text
0 8 0 0 0 0 2 0 0 7 7 0 0 8 0
8 8 8 0 2 2 2 0 0 7 0 0 8 8 8
0 8 0 0 2 0 0 0 7 7 0 0 0 8 0
```

## Build the Pairwise-Intersection Gallery (`hard_112_build_pairwise_intersection_gallery`)

**Difficulty:** hard

**Skills:** panel parsing, binary boolean operations, cross-product galleries

**Scaffold notes:**
- Two row-shapes live in the left column of panels and two column-shapes live in the top row of panels.
- Align each row shape with each column shape cell-by-cell inside a 3×3 panel.
- Output only the intersection cells, colored 8, in a 2×2 gallery.

**Written solution:** Treat the left-side shapes as row prototypes and the top-side shapes as column prototypes. For each row/column combination, compute the cellwise intersection of the two binary shapes and place that 3×3 result into the corresponding gallery panel using color 8.

**Program solution (Python reference):**
```python
def solve_hard_112_build_pairwise_intersection_gallery(g):
    row_shapes=[
        [[1 if v!=0 else 0 for v in row[0:3]] for row in g[0:3]],
        [[1 if v!=0 else 0 for v in row[0:3]] for row in g[4:7]],
    ]
    col_shapes=[
        [[1 if v!=0 else 0 for v in row[4:7]] for row in g[0:3]],
        [[1 if v!=0 else 0 for v in row[8:11]] for row in g[0:3]],
    ]
    out=zeros(7,7)
    for i,rshape in enumerate(row_shapes):
        for j,cshape in enumerate(col_shapes):
            panel=zeros(3,3)
            for r in range(3):
                for c in range(3):
                    if rshape[r][c] and cshape[r][c]:
                        panel[r][c]=8
            place(out, panel, 4*i, 4*j)
    return out
```

**Train 1 input**
```text
2 0 0 0 4 4 0 0 0 5 0
2 0 0 0 0 4 4 0 5 5 5
2 2 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
8 8 0 0 0 8 0
0 8 0 0 0 8 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
2 2 0 0 4 4 0 0 5 0 0
0 2 2 0 4 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0 0 8 0 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 8 0 0 0 0 0
8 0 0 0 8 8 0
0 0 0 0 0 8 0
```

**Train 3 input**
```text
2 2 0 0 4 0 4 0 5 0 0
2 0 0 0 4 0 4 0 0 5 0
0 0 0 0 4 4 4 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0 0 8 0 0
8 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 8 0 0
8 0 0 0 0 8 0
0 8 8 0 0 0 8
```

**Train 4 input**
```text
2 0 2 0 0 0 4 0 5 5 0
2 0 2 0 0 4 0 0 5 5 0
2 2 2 0 4 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 8 0 8 0 0
0 0 0 0 8 0 0
8 0 0 0 8 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 8 0 0 0 8 0
0 0 0 0 0 0 0
```

**Test input**
```text
0 0 2 0 4 0 0 0 5 5 5
0 2 0 0 4 0 0 0 0 5 0
2 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 8
0 0 0 0 0 8 0
8 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 8 8 0
8 0 0 0 0 8 0
8 0 0 0 0 0 0
```
