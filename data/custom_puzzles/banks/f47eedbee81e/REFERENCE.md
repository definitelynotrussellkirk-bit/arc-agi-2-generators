# ARC Puzzle Bank — Fifteenth 21 Puzzles
This fifteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`99`–`105`) so it follows directly after the fourteenth bundle.
This volume pushes into a different mechanic mix than the last one: diagonal span completion, local ring/X stamping, keyed object transforms, prototype stamping, frame-majority reading, topology-driven hole filling, template-transform decoding, rotation-equivalence matrices, chamber filling from a dot-count legend, overlap count maps, cross-product galleries, and sequential transform composition.
It also introduces and reuses a few convenient primitives for solver work: `main_diagonal_span_fill`, `anchor_stamp_count_map`, `rotation_equiv_matrix`, `chamber_fill_from_count_legend`, and `transform_sequence_apply`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_fifteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_fifteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_fifteenth_21.md` — this human-readable catalog.

## Summary
### Easy (7)
- `easy_99_fill_main_diagonal_spans` — **Fill the Main-Diagonal Spans**
- `easy_100_fill_antidiagonal_spans` — **Fill the Anti-Diagonal Spans**
- `easy_101_stamp_hollow_3x3_rings` — **Stamp Hollow 3×3 Rings**
- `easy_102_stamp_x_shapes_at_markers` — **Stamp X-Shapes at the Markers**
- `easy_103_fill_rectangles_from_opposite_corners` — **Fill Rectangles from Opposite Corners**
- `easy_104_read_singleton_colors_left_to_right` — **Read Singleton Colors Left to Right**
- `easy_105_crop_the_unique_object` — **Crop the Unique Object**

### Medium (7)
- `medium_99_transform_object_by_corner_code` — **Transform the Object by the Corner Code**
- `medium_100_select_object_by_key_and_scale2` — **Select the Keyed Object and Scale It 2×**
- `medium_101_stamp_prototype_at_all_anchors` — **Stamp the Prototype at All Anchors**
- `medium_102_frame_each_object_with_key_color` — **Frame Each Object with the Key Color**
- `medium_103_pack_objects_by_area_descending` — **Pack the Objects by Descending Area**
- `medium_104_read_frame_majorities_into_row` — **Read Frame Majorities into a Row**
- `medium_105_fill_the_hole_of_the_holed_object` — **Fill the Hole of the Holed Object**

### Hard (7)
- `hard_99_decode_template_transform_gallery` — **Decode the Template-Transform Gallery**
- `hard_100_build_rotation_equivalence_matrix` — **Build the Rotation-Equivalence Matrix**
- `hard_101_fill_chambers_by_dot_count_legend` — **Fill Chambers by the Dot-Count Legend**
- `hard_102_select_symmetric_object_rotate_and_scale2` — **Select the Symmetric Object, Rotate It, and Scale It 2×**
- `hard_103_overlay_anchor_stamps_into_count_map` — **Overlay Anchor Stamps into a Count Map**
- `hard_104_build_shape_color_cross_product_gallery` — **Build the Shape-Color Cross-Product Gallery**
- `hard_105_select_by_key_and_apply_transform_sequence` — **Select by Key and Apply the Transform Sequence**

## Fill the Main-Diagonal Spans (`easy_99_fill_main_diagonal_spans`)

**Difficulty:** easy

**Skills:** diagonal grouping, same-color endpoint matching, same-size transform

**Scaffold notes:**
- Group nonzero cells by color and by r-c.
- Within each group, find the two endpoints.
- Fill the diagonal cells between them.

**Written solution:** Cells of the same nonzero color mark the ends of a descending diagonal segment. For each color on each main diagonal, fill every cell between the first endpoint and the last endpoint.

**Program solution (Python reference):**
```python
def solve_easy_99_fill_main_diagonal_spans(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[(v, r-c)].append((r,c))
    for (color, diag), cells in groups.items():
        if len(cells) >= 2:
            rows=sorted(r for r,c in cells)
            r0,r1=rows[0], rows[-1]
            for r in range(r0, r1+1):
                c=r-diag
                if 0 <= c < w:
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 3 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 3 0 0 0
0 2 0 0 0 0 0 3 0 0
0 0 2 0 0 0 0 0 3 0
0 0 0 2 0 0 0 0 0 0
0 0 6 0 2 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 7 0 0 0 0
0 0 0 4 0 0 0 7 0 0 0
0 0 0 0 4 0 0 0 7 0 0
0 8 0 0 0 0 0 0 0 7 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 9 0 0 0 0 0 0 0 5 0 0
0 0 9 0 0 0 0 0 0 0 5 0
0 0 0 9 0 0 0 0 0 0 0 5
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0
6 0 0 0 0 0 0 3 0 0
0 6 0 0 0 0 0 0 0 0
0 0 6 0 0 2 0 0 0 0
0 0 0 6 0 0 2 0 0 0
0 0 0 0 6 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8
0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 0 0 8 0 0 0
0 0 0 0 0 4 0 0 8 0 0
6 0 0 0 0 0 4 0 0 8 0
0 6 0 0 0 0 0 0 0 0 8
0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Fill the Anti-Diagonal Spans (`easy_100_fill_antidiagonal_spans`)

**Difficulty:** easy

**Skills:** anti-diagonal grouping, same-color endpoint matching, same-size transform

**Scaffold notes:**
- Group nonzero cells by color and by r+c.
- Within each group, locate the topmost and bottommost endpoints.
- Fill the anti-diagonal path connecting them.

**Written solution:** Cells of the same nonzero color mark the ends of an ascending diagonal segment. For each color on each anti-diagonal, fill every cell between the two endpoints.

**Program solution (Python reference):**
```python
def solve_easy_100_fill_antidiagonal_spans(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[(v, r+c)].append((r,c))
    for (color, diag), cells in groups.items():
        if len(cells) >= 2:
            rows=sorted(r for r,c in cells)
            r0,r1=rows[0], rows[-1]
            s=diag
            for r in range(r0, r1+1):
                c=s-r
                if 0 <= c < w:
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 5 0 0 0 0 0 0
0 0 5 0 0 0 0 2 0 0
0 5 0 0 0 0 2 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0 7
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 8 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 8 0 0 4 0 0
0 0 0 0 8 0 0 4 0 0 0
0 0 0 8 0 0 4 0 0 0 0
0 0 8 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 9 0 0 0 3 0 0 0
0 0 0 9 0 0 0 3 0 0 0 0
0 0 9 0 0 0 3 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 7 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 2 0
0 0 0 0 6 0 0 2 0 0
0 0 0 6 0 0 2 0 0 0
0 0 6 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0 8
0 0 0 0 0 4 0 0 0 8 0
0 0 6 0 4 0 0 0 8 0 0
0 6 0 0 0 0 0 8 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Stamp Hollow 3×3 Rings (`easy_101_stamp_hollow_3x3_rings`)

**Difficulty:** easy

**Skills:** marker expansion, local stamping, same-size transform

**Scaffold notes:**
- Treat each colored cell as a center point.
- Write the eight surrounding cells of the 3×3 neighborhood.
- Do not keep the center cell.

**Written solution:** Every nonzero singleton is only a marker. Replace it with a hollow 3×3 ring of the same color centered on that marker, leaving the center empty.

**Program solution (Python reference):**
```python
def solve_easy_101_stamp_hollow_3x3_rings(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r][c]
            if color!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if not (dr==0 and dc==0):
                            out[r+dr][c+dc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 5 0
0 0 8 8 8 0 0 0 5 5 5 0
0 0 8 0 8 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 6 6 6 0 0 0 3 3 3 0
0 6 0 6 0 0 0 3 0 3 0
0 6 6 6 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
```

## Stamp X-Shapes at the Markers (`easy_102_stamp_x_shapes_at_markers`)

**Difficulty:** easy

**Skills:** marker expansion, diagonal stamping, same-size transform

**Scaffold notes:**
- Treat each colored cell as a center.
- Place the center and the four diagonal cells.
- Ignore orthogonal neighbors.

**Written solution:** Every nonzero singleton is a marker. Replace it with a 3×3 X-shape of the same color: the center plus the four diagonal neighbors.

**Program solution (Python reference):**
```python
def solve_easy_102_stamp_x_shapes_at_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r][c]
            if color!=0:
                for dr,dc in ((0,0),(-1,-1),(-1,1),(1,-1),(1,1)):
                    out[r+dr][c+dc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 8 0 8 0 0 0 5 0 5 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0
0 6 0 6 0 0 0 3 0 3 0
0 0 6 0 0 0 0 0 3 0 0
0 6 0 6 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

## Fill Rectangles from Opposite Corners (`easy_103_fill_rectangles_from_opposite_corners`)

**Difficulty:** easy

**Skills:** bounding box completion, rectangle filling, same-size transform

**Scaffold notes:**
- Look at each color separately.
- Use the two cells of that color to get a bounding box.
- Fill the entire box, not just the border.

**Written solution:** Each color appears at two opposite corners of an axis-aligned rectangle. Fill the whole rectangle spanned by those corners with that color.

**Program solution (Python reference):**
```python
def solve_easy_103_fill_rectangles_from_opposite_corners(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells) >= 2:
            r0=min(r for r,c in cells)
            r1=max(r for r,c in cells)
            c0=min(c for r,c in cells)
            c1=max(c for r,c in cells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 6 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0 0
6 6 6 6 0 0 0 3 3 3 0
6 6 6 6 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 0
0 8 8 8 0 0 0 0 5 5 5 0
0 8 8 8 0 0 0 0 5 5 5 0
0 8 8 8 0 0 0 0 5 5 5 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 7 7 7 7 0 0
0 0 0 0 7 7 7 7 0 0
0 0 0 0 7 7 7 7 0 0
0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0
0 0 4 4 4 4 4 0 6 6 6
0 0 4 4 4 4 4 0 6 6 6
0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0
```

## Read Singleton Colors Left to Right (`easy_104_read_singleton_colors_left_to_right`)

**Difficulty:** easy

**Skills:** ordering by position, sequence extraction, size-changing transform

**Scaffold notes:**
- Collect all nonzero cells.
- Sort them by column from left to right.
- Emit just their colors as a 1×n strip.

**Written solution:** Ignore the blank canvas. Read the singleton colored cells from left to right and write their colors into a single output row in that order.

**Program solution (Python reference):**
```python
def solve_easy_104_read_singleton_colors_left_to_right(g):
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    cells.sort(key=lambda t:(t[1], t[0]))
    return [[v for r,c,v in cells]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 5 3 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 4 7 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 3 9 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
```

**Train 4 output**
```text
7 2 8 4 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 2 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 7 2 9 5
```

## Crop the Unique Object (`easy_105_crop_the_unique_object`)

**Difficulty:** easy

**Skills:** bounding box extraction, size-changing transform, object isolation

**Scaffold notes:**
- Find the min and max occupied row.
- Find the min and max occupied column.
- Crop to that box.

**Written solution:** There is one nonzero object on a blank canvas. Output only the tight bounding-box crop of that object.

**Program solution (Python reference):**
```python
def solve_easy_105_crop_the_unique_object(g):
    return crop_nonzero(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0
2 0
2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 5
5 0 5
5 5 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0
8 8 0
0 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6
0 6 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 0 0
7 0 0
7 7 7
```

## Transform the Object by the Corner Code (`medium_99_transform_object_by_corner_code`)

**Difficulty:** medium

**Skills:** coded transformation, object cropping, rotation decoding

**Scaffold notes:**
- Separate the control code from the object.
- Crop the nonzero object tightly.
- Apply the rotation dictated by the corner code.

**Written solution:** Read the color in the top-left corner as a transform code: 1 = keep, 2 = rotate 90° clockwise, 3 = rotate 180°, 4 = rotate 270° clockwise. Remove the code cell, crop the remaining object, and output the transformed crop.

**Program solution (Python reference):**
```python
def solve_medium_99_transform_object_by_corner_code(g):
    code=g[0][0]
    h,w=dims(g)
    work=clone(g)
    work[0][0]=0
    obj=crop_nonzero(work)
    return apply_transform_code(obj, code)
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2
2 0 0
```

**Train 2 input**
```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 5 5
5 0 5
5 0 5
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8
0 8 8
8 8 0
```

**Train 4 input**
```text
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6
0 6 0
```

**Test input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7
7 0 0
7 0 0
```

## Select the Keyed Object and Scale It 2× (`medium_100_select_object_by_key_and_scale2`)

**Difficulty:** medium

**Skills:** keyed selection, component extraction, scale doubling

**Scaffold notes:**
- Read the color key from the bottom-left corner.
- Pick the connected component of that color.
- Crop it and replicate every cell into a 2×2 block.

**Written solution:** The bottom-left key cell tells you which color to select. Find the object of that color, crop it, and scale it by a factor of 2 in both directions by duplicating each cell into a 2×2 block.

**Program solution (Python reference):**
```python
def solve_medium_100_select_object_by_key_and_scale2(g):
    h,w=dims(g)
    key=g[h-1][0]
    work=clone(g)
    work[h-1][0]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp:(comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    obj=object_crop_from_component(work, comp)
    return scale2(obj)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 5 0 5 0 0 0
0 2 2 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
4 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 0 0
4 4 0 0
4 4 0 0
4 4 0 0
4 4 4 4
4 4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 5 0 0 0
0 4 0 0 0 0 0 5 0 5 0 0 0
0 4 0 0 0 0 0 5 5 5 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 5 0 0 5 5
5 5 0 0 5 5
5 5 0 0 5 5
5 5 0 0 5 5
5 5 5 5 5 5
5 5 5 5 5 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 6 6 6 0
0 4 4 0 0 0 0 0 0 6 0 0
0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6 6 6 6
6 6 6 6 6 6
0 0 6 6 0 0
0 0 6 6 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 6 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 0 0 3 3
3 3 0 0 3 3
3 3 0 0 3 3
3 3 0 0 3 3
3 3 3 3 3 3
3 3 3 3 3 3
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 3 0 3 0 0 0 0 6 0 0 0
0 3 0 3 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 4 0 0
4 4 0 0
4 4 0 0
4 4 0 0
4 4 4 4
4 4 4 4
```

## Stamp the Prototype at All Anchors (`medium_101_stamp_prototype_at_all_anchors`)

**Difficulty:** medium

**Skills:** prototype extraction, translation, multi-stamp copying

**Scaffold notes:**
- Find the largest non-9 connected component.
- Crop it to get the prototype.
- Stamp that crop at each 9-anchor position.

**Written solution:** The largest non-anchor object is a prototype. Every 9-colored singleton is an anchor telling you where to place another copy of the prototype, aligned by its top-left corner. Keep the original prototype too.

**Program solution (Python reference):**
```python
def solve_medium_101_stamp_prototype_at_all_anchors(g):
    h,w=dims(g)
    out=zeros(h,w)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    comps=connected_components(g, colors=set(range(1,9)))
    proto=max(comps, key=lambda comp: comp["area"])
    proto_obj=object_crop_from_component(g, proto)
    stamp(out, proto_obj, proto["bbox"][0], proto["bbox"][1])
    for r,c in anchors:
        stamp(out, proto_obj, r, c)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 9 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 6 6 6 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 5 0 5 0 0 0 5 0 5 0 0
0 0 5 0 5 0 0 0 5 5 5 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 9 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 8 8 0 0 0
0 0 0 0 8 8 0 0 8 8 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 4 0 0 0 0 4 0 0
0 0 0 4 0 0 0 0 4 4 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 6 6 6 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 6 6 6 0 0
0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Frame Each Object with the Key Color (`medium_102_frame_each_object_with_key_color`)

**Difficulty:** medium

**Skills:** bounding boxes, object-wise processing, key-controlled recoloring

**Scaffold notes:**
- Read the frame color from the top-right corner.
- Ignore that key cell when finding objects.
- For each object's bounding box, draw only the border in the key color.

**Written solution:** The top-right cell gives the frame color. For every other object, draw its tight bounding-box border in that key color while leaving the object itself in place.

**Program solution (Python reference):**
```python
def solve_medium_102_frame_each_object_with_key_color(g):
    h,w=dims(g)
    key=g[0][w-1]
    out=clone(g)
    comps=connected_components(g, ignore_positions={(0,w-1)})
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=key
            out[r1][c]=key
        for r in range(r0,r1+1):
            out[r][c0]=key
            out[r][c1]=key
    out[0][w-1]=key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 7 0 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 6
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 6
0 6 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 5 0 5 0 0
0 0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0
0 0 4 8 4 0 0 0 0 0 0 0
0 0 4 4 4 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Pack the Objects by Descending Area (`medium_103_pack_objects_by_area_descending`)

**Difficulty:** medium

**Skills:** component sorting, cropping, vertical packing

**Scaffold notes:**
- Split the canvas into connected components.
- Crop each component tightly.
- Sort by area and pack them vertically with a one-row spacer.

**Written solution:** Crop every connected object, sort the crops by area from largest to smallest, and stack them top-to-bottom with one blank row between consecutive crops.

**Program solution (Python reference):**
```python
def solve_medium_103_pack_objects_by_area_descending(g):
    comps=sort_components_by_area_desc(connected_components(g))
    crops=[object_crop_from_component(g, comp) for comp in comps]
    width=max(len(crop[0]) for crop in crops)
    height=sum(len(crop) for crop in crops) + (len(crops)-1)
    out=zeros(height, width)
    rr=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[rr+r][c]=v
        rr += len(crop)
        if i != len(crops)-1:
            rr += 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 7 7 0 0 0 2 0 0 0
0 0 0 7 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
5 0 5
5 0 5
5 5 5
0 0 0
2 0 0
2 0 0
2 2 0
0 0 0
7 7 0
7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 0
8 8 0
0 8 8
0 0 0
6 6 6
0 6 0
0 0 0
2 2 0
2 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 7 7 0 3 3 3 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 3
3 0 3
3 3 3
0 0 0
4 0 0
4 0 0
4 4 0
0 0 0
7 7 0
7 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 0
6 6 0
6 0 0
0 0 0
6 6 6
0 6 0
0 0 0
2 2 0
2 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 8 0 0 0 0
0 3 3 3 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
3 0 3
3 0 3
3 3 3
0 0 0
8 0 0
8 8 0
0 8 8
0 0 0
2 2 0
2 0 0
```

## Read Frame Majorities into a Row (`medium_104_read_frame_majorities_into_row`)

**Difficulty:** medium

**Skills:** framed region parsing, color counting, sequence extraction

**Scaffold notes:**
- Detect the 5×5 frames with border color 8.
- Count interior colors in each frame.
- Write the winning colors into one output row in frame order.

**Written solution:** Each 5×5 box with an 8-colored border is a frame. Look at the 3×3 interior of each frame, find the majority nonzero color, and emit those majority colors in a single row ordered left-to-right, breaking ties by top-to-bottom.

**Program solution (Python reference):**
```python
def solve_medium_104_read_frame_majorities_into_row(g):
    h,w=dims(g)
    frames=[]
    for r in range(h-4):
        for c in range(w-4):
            # detect 5x5 frame of 8s
            ok=True
            for k in range(5):
                if g[r][c+k]!=8 or g[r+4][c+k]!=8 or g[r+k][c]!=8 or g[r+k][c+4]!=8:
                    ok=False
                    break
            if ok:
                frames.append((r,c))
    # remove duplicates from overlapping scans
    uniq=[]
    seen=set()
    for rc in frames:
        if rc not in seen:
            uniq.append(rc); seen.add(rc)
    uniq.sort(key=lambda t:(t[1], t[0]))
    out=[]
    for r,c in uniq:
        counts=collections.Counter()
        for rr in range(r+1,r+4):
            for cc in range(c+1,c+4):
                v=g[rr][cc]
                if v!=0:
                    counts[v]+=1
        best=max(counts.items(), key=lambda kv:(kv[1], -kv[0]))[0]
        out.append(best)
    return [out]
```

**Train 1 input**
```text
8 8 8 8 8 0 8 8 8 8 8
8 2 2 0 8 0 8 4 4 4 8
8 2 3 0 8 0 8 0 5 0 8
8 0 0 0 8 0 8 0 0 0 8
8 8 8 8 8 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0
0 0 0 8 6 0 0 8 0 0 0
0 0 0 8 6 6 0 8 0 0 0
0 0 0 8 0 0 7 8 0 0 0
0 0 0 8 8 8 8 8 0 0 0
```

**Train 1 output**
```text
2 6 4
```

**Train 2 input**
```text
0 8 8 8 8 8 0 8 8 8 8 8
0 8 3 3 0 8 0 8 8 8 0 8
0 8 0 3 0 8 0 8 0 8 0 8
0 8 5 0 0 8 0 8 8 0 0 8
0 8 8 8 8 8 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0
8 2 0 2 8 0 0 0 0 0 0 0
8 0 2 0 8 0 0 0 0 0 0 0
8 0 0 2 8 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 3 8
```

**Train 3 input**
```text
8 8 8 8 8 0 0 0 0 0 0
8 4 4 4 8 0 0 0 0 0 0
8 0 5 0 8 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 8 8 8 8 8
8 2 2 0 8 0 8 3 3 0 8
8 2 3 0 8 0 8 0 3 0 8
8 0 0 0 8 0 8 5 0 0 8
8 8 8 8 8 0 8 8 8 8 8
```

**Train 3 output**
```text
4 2 3
```

**Train 4 input**
```text
0 0 8 8 8 8 8 0 8 8 8 8 8
0 0 8 6 0 0 8 0 8 2 0 2 8
0 0 8 6 6 0 8 0 8 0 2 0 8
0 0 8 0 0 7 8 0 8 0 0 2 8
0 0 8 8 8 8 8 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0 0 0
0 0 0 0 0 8 8 8 0 8 0 0 0
0 0 0 0 0 8 0 8 0 8 0 0 0
0 0 0 0 0 8 8 0 0 8 0 0 0
0 0 0 0 0 8 8 8 8 8 0 0 0
```

**Train 4 output**
```text
6 8 2
```

**Test input**
```text
8 8 8 8 8 0 8 8 8 8 8
8 8 8 0 8 0 8 2 2 0 8
8 0 8 0 8 0 8 2 3 0 8
8 8 0 0 8 0 8 0 0 0 8
8 8 8 8 8 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0
0 0 8 4 4 4 8 0 0 0 0
0 0 8 0 5 0 8 0 0 0 0
0 0 8 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0
```

**Test output**
```text
8 4 2
```

## Fill the Hole of the Holed Object (`medium_105_fill_the_hole_of_the_holed_object`)

**Difficulty:** medium

**Skills:** topological selection, hole detection, crop-and-fill

**Scaffold notes:**
- Check each object's cropped binary shape for holes.
- Pick the object that has a hole.
- Fill enclosed zero cells and output the filled crop.

**Written solution:** Among all objects, exactly one has an enclosed hole. Select that object, crop it, and fill its hole with the object's own color.

**Program solution (Python reference):**
```python
def solve_medium_105_fill_the_hole_of_the_holed_object(g):
    comps=connected_components(g)
    holed=[]
    for comp in comps:
        crop=object_crop_from_component(g, comp)
        holes=count_holes_binary(crop)
        if holes>0:
            holed.append((holes, comp, crop))
    holes, comp, crop = max(holed, key=lambda t:(t[0], t[1]["area"]))
    return fill_holes_same_color(crop)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 7 7 0 0 0 2 2 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 4
4 4 4
4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 3
3 3 3 3
3 3 3 3
3 3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 4 0 0
0 0 4 0 0 0 0 4 4 4 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 4
4 4 4
4 4 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 2 2 0 0 0 6 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 3 3
3 3 3 3
3 3 3 3
3 3 3 3
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 0 4 4 4 0 0 0 0 0
0 0 8 8 4 0 4 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 4 4
4 4 4
4 4 4
```

## Decode the Template-Transform Gallery (`hard_99_decode_template_transform_gallery`)

**Difficulty:** hard

**Skills:** library lookup, coded transforms, gallery construction

**Scaffold notes:**
- Read the three templates from the fixed library positions.
- Read one 2×2 grid of template IDs and one 2×2 grid of transform IDs.
- Transform each selected template and place it into the matching output gallery cell.

**Written solution:** The top of the input contains a library of three 4×4 templates. The small 2×2 grid at the lower left chooses which template to use in each output cell, and the 2×2 grid beside it chooses the transform code for that template. Build the 2×2 gallery of transformed templates with one blank row and column between gallery cells.

**Program solution (Python reference):**
```python
def solve_hard_99_decode_template_transform_gallery(g):
    templates = {
        1: [row[0:4] for row in g[0:4]],
        2: [row[5:9] for row in g[0:4]],
        3: [row[10:14] for row in g[0:4]],
    }
    tid = [row[0:2] for row in g[6:8]]
    tcode = [row[3:5] for row in g[6:8]]
    cell_h=4; cell_w=4
    out=zeros(cell_h*2+1, cell_w*2+1)
    for gr in range(2):
        for gc in range(2):
            template=clone(templates[tid[gr][gc]])
            transformed=apply_transform_code(template, tcode[gr][gc])
            top=gr*(cell_h+1)
            left=gc*(cell_w+1)
            stamp(out, transformed, top, left)
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 3 3 0 0 4 4 4 0
2 2 2 0 0 3 3 0 0 0 4 0 0 0
0 0 2 0 0 0 3 0 0 0 4 4 0 0
0 0 2 0 0 0 3 3 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 2 0 1 2 0 0 0 0 0 0 0 0 0
3 1 0 3 4 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 0 0 0 3 0
2 2 2 0 0 3 3 3 3
0 0 2 0 0 3 0 0 3
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0
0 0 4 4 0 0 2 2 2
0 0 0 4 0 0 2 0 0
0 4 4 4 0 2 2 0 0
```

**Train 2 input**
```text
0 0 2 2 0 4 4 4 0 0 0 3 3 0
0 0 2 0 0 4 0 0 0 0 0 0 3 0
2 2 2 0 0 4 4 0 0 0 0 0 3 3
0 0 0 0 0 4 4 4 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 0 2 1 0 0 0 0 0 0 0 0 0
1 2 0 4 3 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 4 0 0 3 3 0
4 4 0 4 0 0 0 3 0
4 0 0 4 0 0 0 3 3
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 4 4 4
2 2 2 0 0 0 0 4 4
0 0 2 0 0 0 0 0 4
0 0 2 0 0 0 4 4 4
```

**Train 3 input**
```text
0 3 3 0 0 0 0 0 0 0 4 4 4 0
3 3 0 0 0 0 2 2 2 0 4 0 0 0
0 3 0 0 0 0 2 0 0 0 4 4 0 0
0 3 3 0 0 2 2 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 1 0 4 3 0 0 0 0 0 0 0 0 0
2 3 0 2 1 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 3 3 0
4 0 0 4 0 0 0 3 0
4 0 4 4 0 0 0 3 3
4 4 4 4 0 0 3 3 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 4 4 4 0
2 2 2 0 0 4 0 0 0
0 0 2 0 0 4 4 0 0
0 0 2 0 0 4 4 4 0
```

**Train 4 input**
```text
4 4 4 0 0 2 0 0 0 0 0 0 3 0
4 0 0 0 0 2 2 2 0 0 3 3 3 3
4 4 0 0 0 0 0 2 0 0 3 0 0 3
4 4 4 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 3 0 3 4 0 0 0 0 0 0 0 0 0
2 1 0 1 2 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 4 4 4 0 0 3 3 0
0 0 4 4 0 3 3 0 0
0 0 0 4 0 0 3 0 0
0 4 4 4 0 0 3 3 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 4 4 4 4
2 2 2 0 0 4 4 0 4
0 0 2 0 0 4 0 0 4
0 0 2 0 0 0 0 0 0
```

**Test input**
```text
2 0 0 0 0 0 3 3 0 0 4 4 4 0
2 2 2 0 0 3 3 0 0 0 4 0 0 0
0 0 2 0 0 0 3 0 0 0 4 4 0 0
0 0 2 0 0 0 3 3 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 1 0 2 4 0 0 0 0 0 0 0 0 0
2 3 0 1 3 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 4 4 4 0 0 0 0 0
4 4 0 4 0 0 2 2 2
4 0 0 4 0 0 2 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 4 4 4
3 3 0 0 0 0 0 4 4
0 3 0 0 0 0 0 0 4
0 3 3 0 0 0 4 4 4
```

## Build the Rotation-Equivalence Matrix (`hard_100_build_rotation_equivalence_matrix`)

**Difficulty:** hard

**Skills:** pairwise relations, shape normalization, rotation comparison

**Scaffold notes:**
- Crop the three objects.
- Compare every pair after normalizing away position.
- Check all four rotations when testing equivalence.

**Written solution:** Extract the three objects in reading order. Output a 3×3 matrix whose diagonal is 1 and whose off-diagonal entry is 2 exactly when the two corresponding objects are the same up to rotation; otherwise write 0.

**Program solution (Python reference):**
```python
def solve_hard_100_build_rotation_equivalence_matrix(g):
    comps=sort_components_reading(connected_components(g))
    objs=[object_crop_from_component(g, comp) for comp in comps]
    n=len(objs)
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=1
            elif same_under_rotation(objs[i], objs[j]):
                out[i][j]=2
            else:
                out[i][j]=0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 5 5 5 0 0 0 0 0
0 2 0 0 0 0 5 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 2 0
2 1 0
0 0 1
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
1 0 0
0 1 0
0 0 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 9 9 0 0
```

**Train 3 output**
```text
1 2 2
2 1 2
2 2 1
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
1 2 0
2 1 0
0 0 1
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 7 7 7 0 0 0 0 0
0 2 0 0 0 0 0 7 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
1 0 2
0 1 0
2 0 1
```

## Fill Chambers by the Dot-Count Legend (`hard_101_fill_chambers_by_dot_count_legend`)

**Difficulty:** hard

**Skills:** chamber detection, legend decoding, count-conditioned filling

**Scaffold notes:**
- Read the count→color legend from the top row.
- Find each enclosed zero chamber below the legend.
- Count the dots touching that chamber and fill the whole chamber with the mapped color.

**Written solution:** The top row is a legend: the color placed in column n is the fill color for chambers containing n dots. Below the legend, each enclosed chamber contains 1–3 dots. Fill every chamber, including its dots, with the color selected by its dot count.

**Program solution (Python reference):**
```python
def solve_hard_101_fill_chambers_by_dot_count_legend(g):
    h,w=dims(g)
    legend={c:v for c,v in enumerate(g[0]) if v!=0}
    out=clone(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==0 and not seen[r][c]:
                dq=collections.deque([(r,c)])
                seen[r][c]=True
                cells=[]
                while dq:
                    rr,cc=dq.popleft()
                    cells.append((rr,cc))
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=rr+dr,cc+dc
                        if 1 <= nr < h and 0 <= nc < w and g[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            dq.append((nr,nc))
                cellset=set(cells)
                dots=[]
                r0=min(rr for rr,cc in cells); r1=max(rr for rr,cc in cells)
                c0=min(cc for rr,cc in cells); c1=max(cc for rr,cc in cells)
                for rr in range(max(1,r0-1), min(h-1,r1+1)+1):
                    for cc in range(max(0,c0-1), min(w-1,c1+1)+1):
                        if g[rr][cc]==1:
                            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                                if (rr+dr,cc+dc) in cellset:
                                    dots.append((rr,cc))
                                    break
                n=len(dots)
                if n in legend:
                    color=legend[n]
                    for rr,cc in cells + dots:
                        out[rr][cc]=color
    return out
```

**Train 1 input**
```text
0 2 4 6 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 1 0 8 0 1 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 1 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 0 1 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
0 2 4 6 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 2 2 2 8 4 4 4 8 6 6 6 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
0 3 5 7 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 1 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
0 3 5 7 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 3 3 3 8 5 5 5 8 7 7 7 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
0 4 8 2 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 1 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
0 4 8 2 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 4 4 4 8 8 8 8 8 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
0 6 3 9 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 1 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 1 0 8 0 0 0 8
8 0 0 0 8 0 0 0 8 0 0 1 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
0 6 3 9 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 6 6 6 8 3 3 3 8 9 9 9 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Test input**
```text
0 5 2 8 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 1 0 8 0 0 0 8
8 0 1 0 8 0 0 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 0 0 0 8 0 1 0 8 0 1 0 8
8 0 0 0 8 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
0 5 2 8 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 5 5 5 8 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

## Select the Symmetric Object, Rotate It, and Scale It 2× (`hard_102_select_symmetric_object_rotate_and_scale2`)

**Difficulty:** hard

**Skills:** symmetry testing, keyed transform, scaling

**Scaffold notes:**
- Test each object for both horizontal and vertical mirror symmetry.
- Use the corner code to choose a rotation.
- Scale the rotated crop by duplicating cells.

**Written solution:** Exactly one object is symmetric both horizontally and vertically. Select that object, read the bottom-right code (1 = rotate 90°, 2 = rotate 180°, 3 = rotate 270°), apply the rotation, and scale the result by 2×.

**Program solution (Python reference):**
```python
def solve_hard_102_select_symmetric_object_rotate_and_scale2(g):
    h,w=dims(g)
    code=g[h-1][w-1]
    work=clone(g)
    work[h-1][w-1]=0
    comps=connected_components(work)
    candidates=[]
    for comp in comps:
        crop=object_crop_from_component(work, comp)
        if crop == hflip(crop) and crop == vflip(crop):
            candidates.append((comp["area"], comp, crop))
    _, comp, crop = max(candidates, key=lambda t:t[0])
    transformed=apply_transform_code(crop, {1:2, 2:3, 3:4}[code])
    return scale2(transformed)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 4 4 0 0 0 5 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1
```

**Train 1 output**
```text
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 4 4
4 4 4 4 4 4
4 4 4 4 4 4
4 4 4 4 4 4
0 0 4 4 0 0
0 0 4 4 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 6 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3
```

**Train 2 output**
```text
0 0 6 6 0 0
0 0 6 6 0 0
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
6 6 6 6 6 6
0 0 6 6 0 0
0 0 6 6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 8 0 0 0
0 3 3 3 3 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 3 output**
```text
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 0 0 0 0 3 3
3 3 0 0 0 0 3 3
3 3 0 0 0 0 3 3
3 3 0 0 0 0 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 8 0 0 0
0 0 7 7 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1
```

**Train 4 output**
```text
0 0 7 7 0 0
0 0 7 7 0 0
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
0 0 7 7 0 0
0 0 7 7 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 3
```

**Test output**
```text
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 4 4
4 4 4 4 4 4
4 4 4 4 4 4
4 4 4 4 4 4
0 0 4 4 0 0
0 0 4 4 0 0
```

## Overlay Anchor Stamps into a Count Map (`hard_103_overlay_anchor_stamps_into_count_map`)

**Difficulty:** hard

**Skills:** prototype extraction, multi-stamp overlay, count map construction

**Scaffold notes:**
- Find and crop the prototype object.
- Turn it into a binary mask.
- Stamp it at every anchor and accumulate overlaps as counts.

**Written solution:** The largest non-anchor object is a prototype mask. Every 9-colored anchor asks you to stamp that mask with its top-left corner at the anchor location. Output a count map showing how many stamped copies cover each cell.

**Program solution (Python reference):**
```python
def solve_hard_103_overlay_anchor_stamps_into_count_map(g):
    h,w=dims(g)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    comps=connected_components(g, colors=set(range(1,9)))
    proto=max(comps, key=lambda comp: comp["area"])
    proto_obj=normalize_shape(object_crop_from_component(g, proto))
    counts=zeros(h,w)
    for r,c in anchors:
        countmap_stamp(counts, proto_obj, r, c, transparent=0)
    return counts
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 1 2 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0
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
0 0 0 0 0 0 1 1 2 1 1 0
0 0 0 0 0 0 0 2 1 2 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 9 0 0 0 0 0
0 4 4 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0
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
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 1 2 1 1 0 0 0
0 0 0 0 0 1 1 2 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Build the Shape-Color Cross-Product Gallery (`hard_104_build_shape_color_cross_product_gallery`)

**Difficulty:** hard

**Skills:** factorized decoding, recoloring, gallery construction

**Scaffold notes:**
- Read the three colors from the top row.
- Normalize the three prototype shapes into binary masks.
- Place every row-shape/column-color combination into the output gallery.

**Written solution:** The top row lists three colors. The bottom part lists three prototype shapes. Build a 3×3 gallery whose row chooses the shape and whose column chooses the color, recoloring each shape with the chosen top-row color.

**Program solution (Python reference):**
```python
def solve_hard_104_build_shape_color_cross_product_gallery(g):
    colors=[v for v in g[0] if v!=0]
    shapes=[
        [row[0:3] for row in g[2:5]],
        [row[4:7] for row in g[2:5]],
        [row[8:11] for row in g[2:5]],
    ]
    masks=[normalize_shape(shape) for shape in shapes]
    cell=3
    out=zeros(cell*3+2, cell*3+2)
    for i,mask in enumerate(masks):
        for j,color in enumerate(colors):
            tile=recolor_mask(mask, color)
            stamp(out, tile, i*(cell+1), j*(cell+1))
    return out
```

**Train 1 input**
```text
2 0 0 0 4 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 1 1 1 0 1 1 0
1 0 0 0 0 1 0 0 0 1 0
1 1 1 0 0 1 0 0 0 1 1
```

**Train 1 output**
```text
2 0 0 0 4 0 0 0 6 0 0
2 0 0 0 4 0 0 0 6 0 0
2 2 2 0 4 4 4 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 4 4 4 0 6 6 6
0 2 0 0 0 4 0 0 0 6 0
0 2 0 0 0 4 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 4 4 0 0 6 6 0
0 2 0 0 0 4 0 0 0 6 0
0 2 2 0 0 4 4 0 0 6 6
```

**Train 2 input**
```text
3 0 0 0 5 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 1 1 0 0 0 1 0
0 1 0 0 0 1 0 0 1 1 1
0 1 0 0 0 1 1 0 0 0 1
```

**Train 2 output**
```text
3 3 3 0 5 5 5 0 7 7 7
0 3 0 0 0 5 0 0 0 7 0
0 3 0 0 0 5 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 5 5 0 0 7 7 0
0 3 0 0 0 5 0 0 0 7 0
0 3 3 0 0 5 5 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 5 0 0 0 7 0
3 3 3 0 5 5 5 0 7 7 7
0 0 3 0 0 0 5 0 0 0 7
```

**Train 3 input**
```text
4 0 0 0 8 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 1 0 0 0 0 1 0
0 1 0 0 1 0 0 0 1 1 1
0 1 1 0 1 1 1 0 0 0 1
```

**Train 3 output**
```text
4 4 0 0 8 8 0 0 2 2 0
0 4 0 0 0 8 0 0 0 2 0
0 4 4 0 0 8 8 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 8 0 0 0 2 0 0
4 0 0 0 8 0 0 0 2 0 0
4 4 4 0 8 8 8 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 8 0 0 0 2 0
4 4 4 0 8 8 8 0 2 2 2
0 0 4 0 0 0 8 0 0 0 2
```

**Train 4 input**
```text
6 0 0 0 3 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 1 1 1 0 1 0 0
1 1 1 0 0 1 0 0 1 0 0
0 0 1 0 0 1 0 0 1 1 1
```

**Train 4 output**
```text
0 6 0 0 0 3 0 0 0 9 0
6 6 6 0 3 3 3 0 9 9 9
0 0 6 0 0 0 3 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 3 3 3 0 9 9 9
0 6 0 0 0 3 0 0 0 9 0
0 6 0 0 0 3 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 3 0 0 0 9 0 0
6 0 0 0 3 0 0 0 9 0 0
6 6 6 0 3 3 3 0 9 9 9
```

**Test input**
```text
5 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 1 0 0 1 1 0
1 0 0 0 1 1 1 0 0 1 0
1 1 1 0 0 0 1 0 0 1 1
```

**Test output**
```text
5 0 0 0 2 0 0 0 8 0 0
5 0 0 0 2 0 0 0 8 0 0
5 5 5 0 2 2 2 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 2 0 0 0 8 0
5 5 5 0 2 2 2 0 8 8 8
0 0 5 0 0 0 2 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0
5 5 0 0 2 2 0 0 8 8 0
0 5 0 0 0 2 0 0 0 8 0
0 5 5 0 0 2 2 0 0 8 8
```

## Select by Key and Apply the Transform Sequence (`hard_105_select_by_key_and_apply_transform_sequence`)

**Difficulty:** hard

**Skills:** keyed object selection, sequential transforms, composition

**Scaffold notes:**
- Use the bottom-left color to select the target object.
- Read the top-row codes from left to right.
- Apply each transform to the cropped object in sequence.

**Written solution:** The bottom-left cell selects the object color. The nonzero cells of the top row form a sequence of transform codes. Crop the keyed object and apply the whole transform sequence in order to produce the output.

**Program solution (Python reference):**
```python
def solve_hard_105_select_by_key_and_apply_transform_sequence(g):
    h,w=dims(g)
    seq=[v for v in g[0] if v!=0]
    key=g[h-1][0]
    work=clone(g)
    work[0]=[0]*w
    work[h-1][0]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp: comp["area"])
    obj=object_crop_from_component(work, comp)
    for code in seq:
        obj=apply_transform_code(obj, {1:2, 2:5, 3:7, 4:6}[code])
    return obj
```

**Train 1 input**
```text
1 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 4 0 0 0 0 0 6 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 3 3 3 0
4 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 0
4 0
4 4
```

**Train 2 input**
```text
3 4 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 5 0 5 0 0 0 0 2 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 5
5 0 5
5 5 5
```

**Train 3 input**
```text
2 1 4 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 6
6 6
0 6
```

**Train 4 input**
```text
4 3 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 7
0 0 7
0 0 7
```

**Test input**
```text
1 3 4 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 0
4 0
4 4
```
