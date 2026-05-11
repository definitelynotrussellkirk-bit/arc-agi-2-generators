# ARC Puzzle Bank — Thirteenth 21 Puzzles
This thirteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`85`–`91`) so it follows directly after the twelfth bundle.
This volume leans into a different spread of mechanics: rectangle outlining, diagonal span filling, row compaction, hollow ring stamping, keyed scaling, legend-driven recoloring, emitter ray-casting, symmetry selection, library decoding, rotation-equivalence matrices, chamber parity fills, hole-aware selection, and overlay count maps.
It also introduces a few reusable solver primitives that fit your pipeline well: `diag_span_fill`, `marker_ring_stamp`, `emitter_raycast`, `rotation_equivalence`, and `overlay_count_map`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_thirteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_thirteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_thirteenth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_85_outline_filled_rectangles` — **Outline the Filled Rectangles**
- `easy_86_fill_diagonal_spans_between_matching_endpoints` — **Fill Diagonal Spans Between Matching Endpoints**
- `easy_87_compact_each_row_left` — **Compact Each Row Left**
- `easy_88_stamp_hollow_3x3_around_markers` — **Stamp a Hollow 3×3 Ring Around Each Marker**
- `easy_89_crop_largest_component` — **Crop the Largest Component**
- `easy_90_fill_hollow_rectangles` — **Fill the Hollow Rectangles**
- `easy_91_complete_missing_rectangle_corner` — **Complete the Missing Rectangle Corner**

### Medium (7)
- `medium_85_scale_keyed_object_2x` — **Scale the Keyed Object 2×**
- `medium_86_recolor_body_via_top_legend` — **Recolor the Body via the Top Legend**
- `medium_87_cast_rays_from_emitters_until_wall` — **Cast Rays from Emitters Until the Walls**
- `medium_88_sort_cropped_objects_by_area_and_pack` — **Sort Cropped Objects by Area and Pack Them**
- `medium_89_boolean_intersection_of_two_halves` — **Take the Boolean Intersection of the Two Halves**
- `medium_90_rotate_cropped_object_by_corner_marker` — **Rotate the Cropped Object by the Corner Marker**
- `medium_91_select_horizontally_symmetric_object_and_recolor` — **Select the Left-Right Symmetric Object and Recolor It**

### Hard (7)
- `hard_85_decode_library_shape_transform_and_recolor` — **Decode a Library Shape, Transform It, and Recolor It**
- `hard_86_build_rotation_equivalence_matrix` — **Build the Rotation-Equivalence Matrix**
- `hard_87_fill_chambers_by_internal_key_parity` — **Fill Chambers by Internal Key Parity**
- `hard_88_select_object_by_holes_and_diag_symmetry_scale2` — **Select the Holed Diagonal-Symmetric Object and Scale It 2×**
- `hard_89_sort_objects_by_holes_then_pack_vertical` — **Sort Objects by Hole Count and Pack Them Vertically**
- `hard_90_decode_sequence_of_library_shapes` — **Decode a Sequence of Library Shapes**
- `hard_91_overlay_three_shapes_to_count_map` — **Overlay Three Shapes into a Count Map**

## Outline the Filled Rectangles (`easy_85_outline_filled_rectangles`)

**Difficulty:** easy

**Skills:** connected components, rectangle bbox detection, same-size transform

**Scaffold notes:**
- Find each same-color connected component.
- Read off the component's bounding box.
- Replace the solid rectangle by just its perimeter.

**Written solution:** Each colored object is a solid axis-aligned rectangle. For every connected component, find its bounding box and keep only the border cells of that box in the same color.

**Program solution (Python reference):**
```python
def solve_easy_85_outline_filled_rectangles(g):
    out=zeros(*dims(g))
    for comp in connected_components(g):
        r0,c0,r1,c1 = comp["bbox"]
        color=comp["color"]
        draw_rect_border(out, r0,c0,r1,c1,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
3 0 0 3 0 0 0 0 0 0
3 0 0 3 0 0 0 0 0 0
3 0 0 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 0 0 2 0 0 0
0 0 0 2 2 2 2 0 0 0
```

**Train 2 input**
```text
0 0 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 1 1 1 1 1 0 0 0
0 0 1 0 0 0 1 0 0 0
0 0 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 2 0 0 0
0 0 0 0 2 0 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 9 9 9 9 9 0 0
0 0 0 9 9 9 9 9 0 0
0 0 0 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 3 3 0 0
```

**Train 3 output**
```text
0 0 0 9 9 9 9 9 0 0
0 0 0 9 0 0 0 9 0 0
0 0 0 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 3 3 3 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 1 1 0
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 1 1 1 0
0 6 6 6 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
9 9 9 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0 0 0
7 7 7 7 7 0 0 8 8 8
7 7 7 7 7 0 0 8 8 8
7 7 7 7 7 0 0 8 8 8
7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
9 9 9 0 0 0 0 0 0 0
9 0 9 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0 0 0
7 0 0 0 7 0 0 8 8 8
7 0 0 0 7 0 0 8 0 8
7 0 0 0 7 0 0 8 8 8
7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Fill Diagonal Spans Between Matching Endpoints (`easy_86_fill_diagonal_spans_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** diagonal reasoning, endpoint pairing, same-size transform

**Scaffold notes:**
- Group the colored cells by color.
- Check which paired cells lie on a perfect diagonal.
- Fill every intermediate diagonal step, inclusive.

**Written solution:** Cells of the same color come in pairs on a shared diagonal. For each color pair, fill the entire diagonal segment between the two endpoints with that color.

**Program solution (Python reference):**
```python
def solve_easy_86_fill_diagonal_spans_between_matching_endpoints(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        dr=r2-r1; dc=c2-c1
        if abs(dr)==abs(dc) and dr!=0:
            sr=1 if dr>0 else -1
            sc=1 if dc>0 else -1
            for k in range(abs(dr)+1):
                out[r1+sr*k][c1+sc*k]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0
0 0 6 0 1 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 3
0 6 0 0 0 0 0 3 0
0 0 6 0 1 0 3 0 0
0 0 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 8 1
0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 9 0 8 0 0
0 0 0 9 0 0 0 8 1
0 0 9 0 0 0 0 1 0
0 9 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 6 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 6 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 6 0 0 0 0 0
0 0 0 0 6 8 0 0 0
0 0 0 0 8 6 0 0 0
0 0 0 8 0 0 6 0 0
0 0 8 4 0 0 0 6 0
0 8 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 1
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 3 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 1
0 0 0 4 0 0 0 1 0
0 0 4 0 0 0 1 0 0
0 4 0 0 3 0 0 0 0
4 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 7 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 6
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 7 0 0 0 0 0 0
0 0 0 7 0 6 0 0 0
0 0 0 0 7 0 6 0 0
0 0 0 0 0 0 3 6 0
0 0 0 0 0 3 0 0 6
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Compact Each Row Left (`easy_87_compact_each_row_left`)

**Difficulty:** easy

**Skills:** row-wise processing, stable ordering, same-size transform

**Scaffold notes:**
- Work one row at a time.
- Ignore the zeros but preserve the order of nonzero cells.
- Write the row back starting at column 0.

**Written solution:** Treat each row independently. Remove the zeros, keep the remaining colors in the same left-to-right order, and slide them flush against the left edge.

**Program solution (Python reference):**
```python
def solve_easy_87_compact_each_row_left(g):
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
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 9 2
0 0 0 0 0 0 0 0 0
1 0 0 7 0 0 4 0 0
0 7 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 9 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 7 4 0 0 0 0 0 0
7 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 0 9 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 9 6 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 9 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
9 6 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 3
0 1 0 0 0 0 0 8 0
0 9 0 6 8 0 0 0 0
0 3 8 0 0 0 6 0 0
1 3 0 0 0 0 0 9 0
0 0 0 0 0 0 8 4 0
1 0 2 0 0 0 0 4 8
0 0 0 0 8 0 6 0 0
```

**Train 3 output**
```text
3 0 0 0 0 0 0 0 0
1 8 0 0 0 0 0 0 0
9 6 8 0 0 0 0 0 0
3 8 6 0 0 0 0 0 0
1 3 9 0 0 0 0 0 0
8 4 0 0 0 0 0 0 0
1 2 4 8 0 0 0 0 0
8 6 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 2 0 0 0 0
2 0 1 0 0 0 0 4 0
7 3 0 0 2 0 0 0 1
6 0 0 8 0 0 0 0 0
0 0 6 3 0 0 0 0 0
0 8 0 0 0 6 0 0 0
0 0 4 0 0 0 0 0 0
0 6 0 0 1 0 3 0 0
```

**Train 4 output**
```text
2 0 0 0 0 0 0 0 0
2 1 4 0 0 0 0 0 0
7 3 2 1 0 0 0 0 0
6 8 0 0 0 0 0 0 0
6 3 0 0 0 0 0 0 0
8 6 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
6 1 3 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 1 8 4 2 0
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0
0 0 0 2 6 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
1 8 4 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
2 6 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Stamp a Hollow 3×3 Ring Around Each Marker (`easy_88_stamp_hollow_3x3_around_markers`)

**Difficulty:** easy

**Skills:** local stamping, neighborhood expansion, same-size transform

**Scaffold notes:**
- Locate each isolated marker.
- Consider the 3×3 square centered on it.
- Fill the border of that square but not the center.

**Written solution:** Every nonzero marker becomes the center of a 3×3 neighborhood. Paint the eight surrounding cells in the marker's color and leave the center empty.

**Program solution (Python reference):**
```python
def solve_easy_88_stamp_hollow_3x3_around_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr==0 and dc==0:
                            continue
                        nr,nc=r+dr,c+dc
                        if 0<=nr<h and 0<=nc<w:
                            out[nr][nc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 2 2 2 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 3 0 3 0 0 0
0 0 0 3 3 3 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 1 0 1 0
0 0 0 0 0 1 1 1 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 9 9 9 0 0
0 0 0 0 9 0 9 0 0
0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 3 0 3 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
1 1 1 0 0 0 0 0 0
1 0 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 3 3 3 0 0 6 6 6
0 3 0 3 0 0 6 0 6
0 3 3 3 0 0 6 6 6
0 0 0 0 0 0 7 7 7
9 9 9 0 0 0 7 0 7
9 0 9 0 0 0 7 7 7
9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Crop the Largest Component (`easy_89_crop_largest_component`)

**Difficulty:** easy

**Skills:** component area comparison, bbox crop, size-changing transform

**Scaffold notes:**
- Enumerate the connected components.
- Compare their sizes.
- Crop the largest one tightly.

**Written solution:** Find all connected colored objects, choose the one with the largest area, and output exactly its bounding-box crop.

**Program solution (Python reference):**
```python
def solve_easy_89_crop_largest_component(g):
    comps=connected_components(g)
    best=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return crop_bbox(g, best["bbox"])
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 4 4 0 8 8 8 0 0 0
4 0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 8 0 0 0
```

**Train 1 output**
```text
8 8 8
8 0 8
8 8 8
```

**Train 2 input**
```text
0 0 7 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 2
2 0 2
2 2 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 9 0 0
0 0 0 0 9 0 0 9 0 0
0 0 0 0 9 0 0 9 0 0
0 0 0 0 9 9 9 9 0 0
0 0 6 0 0 0 0 0 0 0
0 0 6 6 6 0 0 7 7 0
0 0 0 0 6 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 9 9
9 0 0 9
9 0 0 9
9 9 9 9
```

**Train 4 input**
```text
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0
0 4 0 0 8 0 0 8 0 0
4 4 4 0 8 0 0 8 0 0
0 4 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8 8
8 0 0 8
8 0 0 8
8 8 8 8
```

**Test input**
```text
0 0 1 1 1 1 0 0 0 0
0 0 1 0 0 1 0 0 0 0
0 0 1 0 0 1 0 0 0 0
0 0 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 4 0
0 0 0 8 8 0 4 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
```

**Test output**
```text
1 1 1 1
1 0 0 1
1 0 0 1
1 1 1 1
```

## Fill the Hollow Rectangles (`easy_90_fill_hollow_rectangles`)

**Difficulty:** easy

**Skills:** rectangle completion, bbox fill, same-size transform

**Scaffold notes:**
- Detect each hollow rectangle.
- Read its bounding box.
- Fill the entire box with the rectangle's color.

**Written solution:** Each object is a one-cell-thick rectangular frame. Fill the full interior of each frame so it becomes a solid rectangle of the same color.

**Program solution (Python reference):**
```python
def solve_easy_90_fill_hollow_rectangles(g):
    out=zeros(*dims(g))
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        color=comp["color"]
        fill_rect(out, r0,c0,r1,c1,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 1 0 0 1
0 0 0 0 0 0 0 1 0 0 1
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 3 3 3 0
6 0 6 0 0 0 0 3 0 3 0
6 6 6 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 3 3 3 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 3 3 3 0
6 6 6 0 0 0 0 3 3 3 0
6 6 6 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 3 3 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
9 9 9 0 1 1 1 0 0 0 0
9 0 9 0 1 0 1 0 0 0 0
9 0 9 0 1 0 1 0 0 0 0
9 0 9 0 1 1 1 0 0 0 0
9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
9 9 9 0 1 1 1 0 0 0 0
9 9 9 0 1 1 1 0 0 0 0
9 9 9 0 1 1 1 0 0 0 0
9 9 9 0 1 1 1 0 0 0 0
9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0
0 4 4 4 4 0 0 6 0 6 0
0 4 0 0 4 0 0 6 0 6 0
0 4 4 4 4 0 0 6 0 6 0
0 0 0 0 0 0 0 6 6 6 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0
0 4 4 4 4 0 0 6 6 6 0
0 4 4 4 4 0 0 6 6 6 0
0 4 4 4 4 0 0 6 6 6 0
0 0 0 0 0 0 0 6 6 6 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0
0 0 4 0 0 4 0 3 3 3 0
0 0 4 0 0 4 0 3 0 3 0
0 0 4 0 0 4 0 3 0 3 0
0 0 4 4 4 4 0 3 0 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0
0 0 4 4 4 4 0 3 3 3 0
0 0 4 4 4 4 0 3 3 3 0
0 0 4 4 4 4 0 3 3 3 0
0 0 4 4 4 4 0 3 3 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
7 7 7 0 0 3 3 3 3 0 0
7 0 7 0 0 3 0 0 3 0 0
7 7 7 0 0 3 0 0 3 0 0
0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7 0 0 3 3 3 3 0 0
7 7 7 0 0 3 3 3 3 0 0
7 7 7 0 0 3 3 3 3 0 0
0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Complete the Missing Rectangle Corner (`easy_91_complete_missing_rectangle_corner`)

**Difficulty:** easy

**Skills:** corner reasoning, axis-aligned rectangles, same-size transform

**Scaffold notes:**
- Group corner cells by color.
- Use the min/max rows and columns to infer the full rectangle corners.
- Add the absent corner.

**Written solution:** For each color, three of the four corners of an axis-aligned rectangle are present. Add the missing fourth corner in the same color.

**Program solution (Python reference):**
```python
def solve_easy_91_complete_missing_rectangle_corner(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==3:
            rs=sorted(set(r for r,c in cells))
            cs=sorted(set(c for r,c in cells))
            if len(rs)==2 and len(cs)==2:
                for rr in (rs[0], rs[1]):
                    for cc in (cs[0], cs[1]):
                        out[rr][cc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 1 0 3 0 3
0 0 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
```

**Train 1 output**
```text
1 0 0 0 1 0 3 0 3
0 0 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0
0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
9 0 9 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
9 0 9 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0
9 0 9 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 4 0 6 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0
0 0 0 0 3 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 1 0 1
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0
0 0 3 0 3 0 1 0 1
0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 1 0 1
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6
```

## Scale the Keyed Object 2× (`medium_85_scale_keyed_object_2x`)

**Difficulty:** medium

**Skills:** color-keyed selection, bbox crop, scaling

**Scaffold notes:**
- Read the key color from the special cell.
- Find the object with the matching color.
- Crop it and expand each cell to a 2×2 block.

**Written solution:** The top-left cell is a color key. Select the object elsewhere in the grid with that color, crop it to its bounding box, and scale the crop by 2 in both dimensions.

**Program solution (Python reference):**
```python
def solve_medium_85_scale_keyed_object_2x(g):
    key=g[0][0]
    h,w=dims(g)
    g2=clone(g)
    g2[0][0]=0
    comps=connected_components(g2)
    target=[comp for comp in comps if comp["color"]==key][0]
    cropped=crop_bbox(g2, target["bbox"])
    return scale2(cropped)
```

**Train 1 input**
```text
9 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 8 8
0 0 0 9 9 0 0 0 0 0 0 8
0 0 0 0 9 0 0 0 0 0 0 8
```

**Train 1 output**
```text
9 9 0 0
9 9 0 0
9 9 9 9
9 9 9 9
0 0 9 9
0 0 9 9
```

**Train 2 input**
```text
2 0 0 2 2 2 0 0 0 9 0 0
0 0 0 2 0 2 0 0 0 9 9 0
0 0 0 2 2 2 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 3
```

**Train 2 output**
```text
2 2 2 2 2 2
2 2 2 2 2 2
2 2 0 0 2 2
2 2 0 0 2 2
2 2 2 2 2 2
2 2 2 2 2 2
```

**Train 3 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 7 7 7 7
0 0 7 7 7 7
0 0 7 7 0 0
0 0 7 7 0 0
7 7 7 7 0 0
7 7 7 7 0 0
```

**Train 4 input**
```text
4 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
```

**Train 4 output**
```text
4 4 4 4 4 4
4 4 4 4 4 4
4 4 0 0 4 4
4 4 0 0 4 4
4 4 4 4 4 4
4 4 4 4 4 4
```

**Test input**
```text
9 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 6 6 6 0 0 0 9 9 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 9 9 9 9
0 0 9 9 9 9
0 0 9 9 0 0
0 0 9 9 0 0
9 9 9 9 0 0
9 9 9 9 0 0
```

## Recolor the Body via the Top Legend (`medium_86_recolor_body_via_top_legend`)

**Difficulty:** medium

**Skills:** legend parsing, color remapping, size-changing transform

**Scaffold notes:**
- Read aligned color pairs from the top two rows.
- Build the source→target mapping.
- Apply it to the body below and drop the legend rows.

**Written solution:** The first two rows form a color legend: row 0 gives source colors and row 1 gives their replacements in the same columns. Remove the legend and recolor the remaining canvas accordingly.

**Program solution (Python reference):**
```python
def solve_medium_86_recolor_body_via_top_legend(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        old=g[0][c]; new=g[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    body=[row[:] for row in g[2:]]
    out=zeros(len(body), w)
    for r in range(len(body)):
        for c in range(w):
            v=body[r][c]
            out[r][c]=mapping.get(v, 0 if v==0 else v)
    return out
```

**Train 1 input**
```text
0 0 7 0 0 0 0 0 8 4
0 0 3 0 0 0 0 0 2 1
0 4 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 8 8 0 0 0 0 0
0 4 0 7 8 8 7 0 0 0
4 4 4 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 1 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 2 2 0 0 0 0 0
0 1 0 3 2 2 3 0 0 0
1 1 1 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 7 2 9 0 0 0 0 0
0 0 8 6 3 0 0 0 0 0
7 0 0 0 0 9 0 0 0 0
0 0 0 0 9 9 0 0 0 0
0 0 0 0 9 9 0 7 7 7
0 0 2 0 0 0 0 0 7 7
0 2 2 7 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9
```

**Train 2 output**
```text
8 0 0 0 0 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 8 8 8
0 0 6 0 0 0 0 0 8 8
0 6 6 8 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
```

**Train 3 input**
```text
0 8 7 4 0 0 0 0 0 0
0 6 2 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 7 0 0 0 8 0 0 0
7 7 7 0 0 0 8 8 8 0
0 7 7 0 0 0 8 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 2 0 0 0 6 0 0 0
2 2 2 0 0 0 6 6 6 0
0 2 2 0 0 0 6 0 0 0
```

**Train 4 input**
```text
0 6 0 0 3 0 8 0 0 0
0 1 0 0 4 0 2 0 0 0
0 0 0 8 0 0 3 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 3 0 0 6
0 0 0 6 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 6 0 0 0 8 8 0
0 0 0 0 0 0 0 0 8 8
```

**Train 4 output**
```text
0 0 0 2 0 0 4 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 4 0 0 1
0 0 0 1 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 0 0 0 2 2 0
0 0 0 0 0 0 0 0 2 2
```

**Test input**
```text
0 0 1 9 0 0 3 0 0 0
0 0 8 2 0 0 7 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
9 0 0 0 0 0 1 1 1 0
```

**Test output**
```text
0 0 0 0 0 0 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
2 0 0 0 0 0 8 8 8 0
```

## Cast Rays from Emitters Until the Walls (`medium_87_cast_rays_from_emitters_until_wall`)

**Difficulty:** medium

**Skills:** ray casting, blockers, same-size transform

**Scaffold notes:**
- Identify the emitters and the blocking walls.
- Walk outward in four directions from every emitter.
- Paint only empty cells until you hit a blocker or leave the grid.

**Written solution:** Cells with color 2 are emitters and cells with color 5 are walls. From each emitter, cast rays in the four cardinal directions, painting empty cells with color 8 until a wall or the border stops the ray.

**Program solution (Python reference):**
```python
def solve_medium_87_cast_rays_from_emitters_until_wall(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:
                        out[nr][nc]=8
                        nr += dr; nc += dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 5 5 5 5 5 5 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 8 0 8 0 0 8 0
8 8 8 8 8 2 8 8 8 8
0 0 0 8 0 8 0 0 8 0
0 0 0 8 0 8 0 0 8 0
0 0 0 8 0 8 0 0 8 0
8 8 8 2 8 8 8 8 8 8
0 0 5 5 5 5 5 5 8 0
0 5 5 5 5 5 5 8 2 8
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 8 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 0
0 5 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0
8 8 2 8 8 8 8 8 2 8
0 5 8 0 0 0 0 0 8 0
0 5 8 0 0 0 0 0 8 0
0 5 5 5 5 5 5 5 5 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 5 2 0 0
0 0 0 2 5 5 5 0 0 0
0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 8 8 0 0 8 0 0
8 8 8 8 2 8 8 8 8 8
0 0 0 8 8 5 0 8 0 0
0 0 0 8 5 5 0 8 0 0
0 0 0 8 5 5 5 2 8 8
8 8 8 2 5 5 5 8 0 0
0 0 0 8 5 5 5 8 0 0
0 0 0 8 0 5 5 8 0 0
0 0 0 8 0 0 5 8 0 0
0 0 0 8 0 0 0 8 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 2 5 0 0
0 0 0 2 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 8 0 0 8 0 0 0
0 0 0 8 0 0 8 5 0 0
8 8 8 8 8 8 2 5 0 0
8 8 8 2 8 8 8 5 0 0
0 0 0 8 0 0 8 5 0 0
0 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 2 0 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 0 2 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 8 0 0 8 0 0 0
8 8 8 2 8 8 8 8 8 8
0 0 0 8 0 0 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 8 0 0 8 0 0 0
0 0 5 8 8 8 2 8 8 8
0 0 5 8 0 0 8 5 0 0
0 0 5 8 0 0 8 5 0 0
8 8 8 2 8 8 5 5 5 0
0 0 0 8 0 0 0 0 0 0
```

## Sort Cropped Objects by Area and Pack Them (`medium_88_sort_cropped_objects_by_area_and_pack`)

**Difficulty:** medium

**Skills:** component extraction, area sorting, packing

**Scaffold notes:**
- Crop each object individually.
- Compute each crop's area.
- Order the crops from smallest to largest and h-stack them.

**Written solution:** Extract each connected object, crop it tightly, sort the cropped objects by area from smallest to largest, and place them left-to-right with a one-cell gap.

**Program solution (Python reference):**
```python
def solve_medium_88_sort_cropped_objects_by_area_and_pack(g):
    comps=connected_components(g)
    crops=[crop_bbox(g, comp["bbox"]) for comp in comps]
    crops=sorted(crops, key=lambda cg: sum(v!=0 for row in cg for v in row))
    return hstack(crops, gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0
0 0 0 0 0 2 0 0 2 0 0 0
0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 0 0 0 8 0 0 2 2 2 2
1 0 0 8 8 8 0 2 0 0 2
1 1 0 0 8 0 0 2 0 0 2
0 0 0 0 0 0 0 2 2 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 4 0 0 9 9 9 0
0 0 0 0 0 4 0 0 9 0 9 0
0 0 0 0 0 4 4 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 6 6 6 6 0 9 9 9
4 0 0 6 0 0 6 0 9 0 9
4 0 0 6 0 0 6 0 9 9 9
4 4 0 6 6 6 6 0 9 0 9
0 0 0 0 0 0 0 0 9 9 9
```

**Train 3 input**
```text
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7
```

**Train 3 output**
```text
0 8 0 0 6 6 0 0 7 7 7 7
8 8 8 0 6 0 0 0 7 0 0 7
0 8 0 0 6 6 6 0 7 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 0
0 0 0 0 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 4 0
0 0 7 0 0 0 0 0 0 4 4 4
0 0 7 7 0 0 0 0 0 0 4 0
```

**Train 4 output**
```text
7 0 0 0 4 0 0 1 1 1 1
7 0 0 4 4 4 0 1 0 0 1
7 7 0 0 4 0 0 1 0 0 1
0 0 0 0 0 0 0 1 1 1 1
```

**Test input**
```text
0 0 0 0 0 0 4 0 0 0 0 0
0 6 6 6 6 0 4 0 0 0 0 0
0 6 0 0 6 0 4 4 0 0 0 0
0 6 0 0 6 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 8 0
```

**Test output**
```text
4 0 0 0 8 0 0 6 6 6 6
4 0 0 8 8 8 0 6 0 0 6
4 4 0 0 8 0 0 6 0 0 6
0 0 0 0 0 0 0 6 6 6 6
```

## Take the Boolean Intersection of the Two Halves (`medium_89_boolean_intersection_of_two_halves`)

**Difficulty:** medium

**Skills:** panel splitting, boolean overlap, size-changing transform

**Scaffold notes:**
- Find the divider row.
- Compare the top and bottom panels cell by cell.
- Mark only the overlapping occupied cells.

**Written solution:** A full row of color 5 divides the input into a top panel and a bottom panel of the same size. Output a panel where a cell is color 8 exactly when both corresponding panel cells are nonzero.

**Program solution (Python reference):**
```python
def solve_medium_89_boolean_intersection_of_two_halves(g):
    h,w=dims(g)
    divider=None
    for r,row in enumerate(g):
        if all(v==5 for v in row):
            divider=r
            break
    assert divider is not None
    top=g[:divider]
    bottom=g[divider+1:]
    assert len(top)==len(bottom)
    out=zeros(len(top), w)
    for r in range(len(top)):
        for c in range(w):
            if top[r][c]!=0 and bottom[r][c]!=0:
                out[r][c]=8
    return out
```

**Train 1 input**
```text
2 0 2 2 0 0 2 2
0 0 0 2 0 0 2 2
0 2 0 0 2 2 0 2
0 2 0 0 0 0 2 0
0 0 0 2 0 2 2 0
5 5 5 5 5 5 5 5
3 0 0 0 3 0 0 0
3 0 0 0 0 0 0 3
0 3 0 3 3 0 0 0
0 0 3 0 3 0 3 3
0 3 0 3 0 3 0 0
```

**Train 1 output**
```text
8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8
0 8 0 0 8 0 0 0
0 0 0 0 0 0 8 0
0 0 0 8 0 8 0 0
```

**Train 2 input**
```text
0 2 2 0 0 0 2 2
0 0 2 2 2 0 0 0
0 0 2 2 2 0 0 0
0 2 0 2 0 2 0 2
2 0 0 0 0 2 0 2
5 5 5 5 5 5 5 5
0 0 3 3 0 0 0 3
0 0 0 0 0 0 0 0
0 0 3 3 3 0 3 3
0 3 3 0 0 0 0 0
3 0 0 0 3 0 0 3
```

**Train 2 output**
```text
0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0
0 8 0 0 0 0 0 0
8 0 0 0 0 0 0 8
```

**Train 3 input**
```text
2 2 0 0 2 2 0 0
2 0 0 0 0 2 2 0
0 0 0 0 2 0 0 0
0 0 2 0 0 0 2 2
2 0 0 0 0 0 2 0
5 5 5 5 5 5 5 5
0 3 3 3 3 0 0 0
3 0 0 0 0 3 0 0
3 0 3 0 0 0 0 3
3 0 3 0 0 3 3 3
3 3 3 3 3 0 3 3
```

**Train 3 output**
```text
0 8 0 0 8 0 0 0
8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 8
8 0 0 0 0 0 8 0
```

**Train 4 input**
```text
0 2 2 0 0 0 2 2
0 0 2 2 0 2 2 0
0 0 0 0 0 2 0 0
2 0 2 2 0 0 0 2
0 2 2 0 2 0 2 2
5 5 5 5 5 5 5 5
3 3 0 0 0 0 0 3
3 0 0 0 0 3 3 3
0 3 0 3 0 0 0 3
3 0 3 0 0 0 0 3
0 3 0 0 0 0 3 3
```

**Train 4 output**
```text
0 8 0 0 0 0 0 8
0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0
8 0 8 0 0 0 0 8
0 8 0 0 0 0 8 8
```

**Test input**
```text
0 2 2 0 2 2 2 2
2 2 2 0 2 2 2 0
0 0 0 0 2 2 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 2 2 0
5 5 5 5 5 5 5 5
0 3 3 0 3 3 3 3
0 3 0 3 0 0 3 3
3 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3
0 0 0 0 3 3 0 0
```

**Test output**
```text
0 8 8 0 8 8 8 8
0 8 0 0 0 0 8 0
0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0
```

## Rotate the Cropped Object by the Corner Marker (`medium_90_rotate_cropped_object_by_corner_marker`)

**Difficulty:** medium

**Skills:** control markers, rotation, bbox crop

**Scaffold notes:**
- Read the control from the marker's corner position.
- Ignore the marker itself when extracting the object.
- Crop the object tightly and rotate it according to the code.

**Written solution:** A single marker color 9 sits in one corner of the canvas. Its corner position encodes the rotation: top-left = keep, top-right = rotate clockwise, bottom-right = 180°, bottom-left = rotate counterclockwise. Remove the marker, crop the object, and apply the indicated rotation.

**Program solution (Python reference):**
```python
def solve_medium_90_rotate_cropped_object_by_corner_marker(g):
    h,w=dims(g)
    corner_map = {
        (0,0): "id",
        (0,w-1): "cw",
        (h-1,w-1): "180",
        (h-1,0): "ccw",
    }
    marker=None
    for cell,code in corner_map.items():
        r,c=cell
        if g[r][c]==9:
            marker=code
            mr,mc=r,c
            break
    assert marker is not None
    g2=clone(g)
    g2[mr][mc]=0
    obj=crop_nonzero(g2)
    if marker=="id":
        return obj
    if marker=="cw":
        return rotate_cw(obj)
    if marker=="180":
        return rotate_180(obj)
    if marker=="ccw":
        return rotate_ccw(obj)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2
2 2
2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
```

**Train 2 output**
```text
0 6
6 6
6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 0
2 0 0
2 2 2
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 6 0 6 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6
6 0 6
6 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7
7 0 0
```

## Select the Left-Right Symmetric Object and Recolor It (`medium_91_select_horizontally_symmetric_object_and_recolor`)

**Difficulty:** medium

**Skills:** symmetry detection, object selection, recoloring

**Scaffold notes:**
- Crop each object separately.
- Test which crop is mirror-symmetric left-to-right.
- Keep that crop only and recolor it.

**Written solution:** Among the objects, exactly one is symmetric under a left-right mirror of its own crop. Select that object, crop it tightly, and recolor every nonzero cell to 8.

**Program solution (Python reference):**
```python
def solve_medium_91_select_horizontally_symmetric_object_and_recolor(g):
    comps=connected_components(g)
    for comp in comps:
        crop=crop_bbox(g, comp["bbox"])
        if is_vertically_symmetric(crop):
            return recolor(crop, 8)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 3 3 3 3 0 0 0 9 0 0
0 3 0 0 3 0 0 0 0 9 0
0 3 0 0 3 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 2 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 1 1
```

**Train 2 output**
```text
8 8 8
8 0 8
8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 8 8 0 0
0 0 7 0 0 0 8 0 8 0 0
0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8 0
8 8 8
8 0 8
```

**Train 4 input**
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0
```

**Train 4 output**
```text
8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 2 0
```

**Test output**
```text
0 8 0
8 8 8
0 8 0
```

## Decode a Library Shape, Transform It, and Recolor It (`hard_85_decode_library_shape_transform_and_recolor`)

**Difficulty:** hard

**Skills:** library lookup, transform codes, recoloring

**Scaffold notes:**
- Read the three library panels.
- Use the selector color to choose one panel.
- Apply the coded transform, then recolor the result.

**Written solution:** The top row band contains three library panels. The code row supplies a selector color, a transform code, and an output color. Choose the library shape whose panel color matches the selector, crop it, apply the coded transform, and recolor it to the output color.

**Program solution (Python reference):**
```python
def solve_hard_85_decode_library_shape_transform_and_recolor(g):
    # top 5 rows: 3 library panels width 5 separated by gap 1
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g[:5]]) for i in range(3)]
    colors=[]
    for i in range(3):
        panel=[row[i*6:i*6+5] for row in g[:5]]
        col=next(v for row in panel for v in row if v!=0)
        colors.append(col)
    selector, tcode, outcolor = g[6][0], g[6][1], g[6][2]
    idx=colors.index(selector)
    obj=panels[idx]
    transformed=apply_transform(obj, tcode)
    return recolor(transformed, outcolor)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 9 9 9 0 0 0 8 0 0 0
0 6 6 6 0 0 0 9 0 9 0 0 0 8 0 0 0
0 0 0 6 0 0 0 9 9 9 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 2
2 2 2
2 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 3 0 0 0 0 4 0 0 0
0 6 6 6 0 0 0 3 3 3 0 0 0 4 0 0 0
0 6 0 0 0 0 0 0 3 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 5 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 3
0 3
3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 6 0 0 0 0 8 8 8 0
0 7 7 7 0 0 0 0 6 0 0 0 0 8 0 8 0
0 0 7 0 0 0 0 6 6 6 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 1 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3 0
0 3 0
3 3 3
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 8 8 8 0 0 0 3 0 0 0
0 7 0 7 0 0 0 8 0 0 0 0 0 3 3 3 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 5 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6
6 0 6
6 6 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 7 0 0 0 0 0 0 2 0 0
0 8 0 0 0 0 0 7 7 7 0 0 0 2 2 2 0
0 8 8 0 0 0 0 0 0 7 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 5 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 6 0
6 6 6
0 6 0
```

## Build the Rotation-Equivalence Matrix (`hard_86_build_rotation_equivalence_matrix`)

**Difficulty:** hard

**Skills:** panel parsing, rotation-invariant matching, relation matrix

**Scaffold notes:**
- Crop the object from each panel.
- Normalize shapes by ignoring color and checking all four rotations.
- Fill the relation matrix pairwise.

**Written solution:** The input contains four object panels. Compare every pair of cropped shapes while ignoring color and allowing rotations. Output a 4×4 matrix with color 8 where two objects are equivalent up to rotation, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_86_build_rotation_equivalence_matrix(g):
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g]) for i in range(4)]
    rots=[rotations_of_norm(panel) for panel in panels]
    n=4
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if any(shape in rots[j] for shape in rots[i]):
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 0
0 2 2 0 0 0 0 3 3 3 0 0 0 0 4 0 0 0 6 0 0 6 0
0 0 2 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0 6 0 0 6 0
0 0 2 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 0 0 0 0 0 4 0 0 0 0 6 6 0 0
0 2 2 2 0 0 0 3 3 0 0 0 0 4 4 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 3 3 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0 0
8 8 0 0
0 0 8 8
0 0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 3 0 0 0 0 0 4 0 0 0 6 6 6 0
0 2 2 2 0 0 0 0 3 0 0 0 0 4 4 4 0 0 0 6 0 6 0
0 0 0 2 0 0 0 3 3 0 0 0 0 0 0 4 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 3 3 0 0 0 0 4 0 0 0 0 0 6 0 0
0 0 2 0 0 0 0 0 3 0 0 0 0 4 4 0 0 0 0 6 6 0 0
0 2 2 0 0 0 0 3 3 0 0 0 0 4 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 0 0
8 8 0 0
0 0 8 8
0 0 8 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 3 0 0 0 0 4 0 0 0 0 6 0 0 0
0 2 2 2 0 0 0 0 3 0 0 0 0 4 4 0 0 0 0 6 6 0 0
0 0 0 2 0 0 0 3 3 0 0 0 0 4 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

## Fill Chambers by Internal Key Parity (`hard_87_fill_chambers_by_internal_key_parity`)

**Difficulty:** hard

**Skills:** flood fill, region counting, conditional chamber fill

**Scaffold notes:**
- Flood-fill each non-wall chamber.
- Count the key cells inside that chamber.
- Choose the fill color from the parity of the count.

**Written solution:** Walls are color 5 and divide the board into chambers. Count how many key cells of color 2 lie in each chamber. Chambers with one key (or any odd count) fill with 8, chambers with an even positive count fill with 7, and chambers with no keys stay empty; walls remain unchanged.

**Program solution (Python reference):**
```python
def solve_hard_87_fill_chambers_by_internal_key_parity(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=5 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                cells=[]
                keys=0
                while q:
                    rr,cc=q.popleft()
                    cells.append((rr,cc))
                    if g[rr][cc]==2:
                        keys += 1
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and g[nr][nc]!=5 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                fill=0
                if keys>0:
                    fill=8 if keys%2==1 else 7
                for rr,cc in cells:
                    out[rr][cc]=fill
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 2 2 5 0 0 0 0 5
5 5 5 5 5 5 0 0 2 0 5
5 0 0 0 0 5 0 2 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 2 0 0 2 5
5 0 0 0 0 5 0 0 0 0 5
5 2 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 5 5 5 5 5 7 7 7 7 5
5 0 0 0 0 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 5 7 7 7 7 5
5 8 8 8 8 5 7 7 7 7 5
5 8 8 8 8 5 7 7 7 7 5
5 8 8 8 8 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 0 0 0 0 5
5 0 2 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 2 5
5 2 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 2 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 0 0 0 0 5
5 8 8 8 8 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 8 8 8 8 5
5 7 7 7 7 5 8 8 8 8 5
5 7 7 7 7 5 8 8 8 8 5
5 7 7 7 7 5 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 2 0 0 0 5 2 0 0 0 5
5 0 0 2 0 5 0 0 0 0 5
5 5 5 5 5 5 0 0 0 2 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 2 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 5 5 5 5 5 7 7 7 7 5
5 0 0 0 0 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 5 0 0 0 0 5
5 8 8 8 8 5 0 0 0 0 5
5 8 8 8 8 5 0 0 0 0 5
5 8 8 8 8 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 2 0 0 5 0 0 0 2 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 2 0 0 0 5 0 0 2 0 5
5 0 2 0 0 5 0 0 2 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 5 8 8 8 8 5
5 8 8 8 8 5 8 8 8 8 5
5 5 5 5 5 5 8 8 8 8 5
5 0 0 0 0 5 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 2 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 0 0 0 0 5
5 0 0 2 2 5 2 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 7 7 7 7 5
5 0 0 0 0 5 7 7 7 7 5
5 5 5 5 5 5 7 7 7 7 5
5 7 7 7 7 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

## Select the Holed Diagonal-Symmetric Object and Scale It 2× (`hard_88_select_object_by_holes_and_diag_symmetry_scale2`)

**Difficulty:** hard

**Skills:** hole counting, diagonal symmetry, selection + scaling

**Scaffold notes:**
- Crop each candidate object.
- Check both properties: enclosed hole(s) and main-diagonal symmetry.
- Keep the matching object, recolor it, and scale it up.

**Written solution:** Exactly one object both contains at least one enclosed hole and is symmetric under transpose across its own main diagonal. Select that object, crop it, recolor it to 8, and scale it by 2.

**Program solution (Python reference):**
```python
def solve_hard_88_select_object_by_holes_and_diag_symmetry_scale2(g):
    comps=connected_components(g)
    for comp in comps:
        crop=crop_bbox(g, comp["bbox"])
        if count_holes_binary(crop) >= 1 and is_main_diag_symmetric([[1 if v!=0 else 0 for v in row] for row in crop]):
            return scale2(recolor(crop, 8))
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 6 6 0 9 9 9 0 0 0
0 0 0 0 6 0 0 0 9 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 2 2 2 0 0 0 0 7 7 0 0
0 0 2 0 2 0 0 0 0 0 7 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 6 0 6 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 9 9 9 0 0 0
7 7 7 7 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 8 0 0 0 0 8 8
8 8 0 0 0 0 8 8
8 8 0 0 0 0 8 8
8 8 0 0 0 0 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```

## Sort Objects by Hole Count and Pack Them Vertically (`hard_89_sort_objects_by_holes_then_pack_vertical`)

**Difficulty:** hard

**Skills:** topological features, sorting, packing

**Scaffold notes:**
- Count holes inside each cropped object.
- Use area as the tie-breaker among equal hole counts.
- Pack the ordered crops vertically.

**Written solution:** Extract and crop all objects. Sort them first by increasing number of enclosed holes, and break ties by decreasing area. Then stack the cropped objects top-to-bottom with one blank row between them.

**Program solution (Python reference):**
```python
def solve_hard_89_sort_objects_by_holes_then_pack_vertical(g):
    comps=connected_components(g)
    crops=[crop_bbox(g, comp["bbox"]) for comp in comps]
    crops=sorted(crops, key=lambda cg: (count_holes_binary(cg), -sum(v!=0 for row in cg for v in row)))
    return vstack(crops, gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0
0 2 2 2 0 0 1 0 1 0 0 0 0 0
0 2 0 2 0 0 1 1 1 0 0 0 0 0
0 2 2 2 0 0 1 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 9 0 0
0 0 7 0 0 0 0 0 0 0 9 9 9 0
0 7 7 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 7
0 0 7
0 7 7
0 0 0
0 9 0
9 9 9
0 9 0
0 0 0
2 2 2
2 0 2
2 2 2
0 0 0
1 1 1
1 0 1
1 1 1
1 0 1
1 1 1
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 7 0 0
0 0 6 0 6 0 0 0 0 0 7 7 7 0
0 0 6 6 6 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 9 9 9 0 0 0 0 0 1 1 1
0 0 0 9 0 9 0 0 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6
6 0 6
6 6 6
0 0 0
0 7 0
7 7 7
0 7 0
0 0 0
9 9 9
9 0 9
9 9 9
0 0 0
1 1 1
1 0 1
1 1 1
1 0 1
1 1 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 3 0 3 0
0 0 0 2 0 0 0 0 0 0 3 3 3 0
0 2 0 2 0 0 0 0 6 0 0 0 0 0
0 2 2 2 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 2
2 0 2
2 2 2
0 0 0
0 6 0
6 6 6
0 6 0
0 0 0
3 3 3
3 0 3
3 3 3
0 0 0
1 1 1
1 0 1
1 1 1
1 0 1
1 1 1
```

**Train 4 input**
```text
0 0 0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 3 0 2 2 2 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 0
```

**Train 4 output**
```text
0 0 3
3 0 3
3 3 3
0 0 0
0 6 0
6 6 6
0 6 0
0 0 0
2 2 2
2 0 2
2 2 2
0 0 0
4 4 4
4 0 4
4 4 4
4 0 4
4 4 4
```

**Test input**
```text
0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 3 0 0 0 0 0 4 0 4 0 0 0
3 0 3 0 0 0 0 0 4 4 4 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 3 0
0 3 0 3 0
0 3 3 3 0
0 0 0 0 0
0 0 6 0 0
0 6 6 6 0
0 0 6 0 0
0 0 0 0 0
0 4 4 4 0
0 4 0 4 0
0 4 4 4 0
0 0 0 0 0
1 1 1 1 1
1 0 1 0 1
1 1 1 1 1
```

## Decode a Sequence of Library Shapes (`hard_90_decode_sequence_of_library_shapes`)

**Difficulty:** hard

**Skills:** library lookup, multi-step code decoding, packing

**Scaffold notes:**
- Parse the library once.
- Read the code row as repeated selector/transform pairs.
- Decode each item and concatenate the transformed shapes.

**Written solution:** The top library band works like a reusable dictionary of shapes. The code row gives a sequence of selector-color / transform-code pairs. For each pair, select the matching library shape, apply the transform, and place the decoded outputs left-to-right with one-cell gaps.

**Program solution (Python reference):**
```python
def solve_hard_90_decode_sequence_of_library_shapes(g):
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g[:5]]) for i in range(3)]
    colors=[]
    for i in range(3):
        panel=[row[i*6:i*6+5] for row in g[:5]]
        colors.append(next(v for row in panel for v in row if v!=0))
    code_row=g[6]
    items=[]
    c=0
    while c+1 < len(code_row):
        if code_row[c]==0:
            break
        items.append((code_row[c], code_row[c+1]))
        c += 2
    out_items=[]
    for selector, tcode in items:
        idx=colors.index(selector)
        obj=panels[idx]
        out_items.append(apply_transform(obj, tcode))
    return hstack(out_items, gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 3 3 3 0 0 0 0 6 0 0
0 9 0 9 0 0 0 0 3 0 0 0 0 6 6 6 0
0 9 9 9 0 0 0 0 3 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 4 3 4 6 4 3 4 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 6 0 0 3 0 0 0 0 6 0 0 3 0 0
6 6 6 0 3 3 3 0 6 6 6 0 3 3 3
0 6 0 0 3 0 0 0 0 6 0 0 3 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 9 9 9 0 0 0 7 7 0 0
0 2 2 2 0 0 0 9 0 9 0 0 0 0 7 0 0
0 0 0 2 0 0 0 9 9 9 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 2 7 2 2 4 9 4 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
9 9 9 0 0 0 7 0 2 2 2 0 9 9 9
9 0 9 0 7 7 7 0 0 2 0 0 9 0 9
9 9 9 0 0 0 0 0 0 2 0 0 9 9 9
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 9 0 0 0 0 0 4 0 0 0
0 7 0 7 0 0 0 9 9 9 0 0 0 4 0 0 0
0 7 7 7 0 0 0 0 0 9 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 2 4 3 7 4 9 3 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 9 9 0 4 4 0 7 7 7 0 9 0 0
0 9 0 0 0 4 0 7 0 7 0 9 9 9
9 9 0 0 0 4 0 7 7 7 0 0 0 9
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 9 0 0 0 4 4 0 0
0 2 2 2 0 0 0 9 0 9 0 0 0 0 4 0 0
0 0 0 2 0 0 0 9 9 9 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 1 2 2 9 3 2 1 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 9 0 0 2 0 0 9 9 9 0 0 0 2
9 0 9 0 0 2 0 0 9 0 9 0 2 2 2
9 9 9 0 2 2 2 0 9 0 0 0 0 0 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 2 0 0 0 0 0 0 9 9 0
0 7 0 7 0 0 0 2 2 2 0 0 0 0 9 0 0
0 7 0 0 0 0 0 2 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 3 2 4 7 1 7 3 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 9 9 0 0 2 0 0 7 7 7 0 0 0 7
0 9 0 0 0 2 0 0 7 0 7 0 7 0 7
9 9 0 0 2 2 2 0 7 0 0 0 7 7 7
```

## Overlay Three Shapes into a Count Map (`hard_91_overlay_three_shapes_to_count_map`)

**Difficulty:** hard

**Skills:** panel alignment, overlap counting, count-map abstraction

**Scaffold notes:**
- Treat the three panels as aligned layers.
- Count how many layers occupy each cell.
- Map counts 1, 2, and 3 to colors 2, 4, and 8.

**Written solution:** Three aligned panels contain one shape each. Overlay them cellwise while ignoring the original colors. Output 2 where exactly one panel occupies a cell, 4 where exactly two do, and 8 where all three overlap.

**Program solution (Python reference):**
```python
def solve_hard_91_overlay_three_shapes_to_count_map(g):
    panels=[ [row[i*6:i*6+5] for row in g] for i in range(3) ]
    h,w=5,5
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for p in panels if p[r][c]!=0)
            out[r][c]=0 if cnt==0 else {1:2,2:4,3:8}[cnt]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 2 2 2 0 0 0 7 7 0 0
0 4 4 4 0 0 0 0 2 0 0 0 0 7 0 0 0
0 0 4 0 0 0 0 0 2 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0
0 4 8 2 0
0 4 4 2 0
0 2 8 2 0
0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 3 3 3 0 0 0 9 9 9 0
0 7 7 0 0 0 0 3 0 0 0 0 0 9 0 9 0
0 7 7 7 0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0
0 8 4 4 0
0 8 2 2 0
0 4 4 4 0
0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 4 4 4 0 0 0 0 3 0 0
0 2 0 0 0 0 0 0 4 4 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0
0 4 8 4 0
0 4 4 4 0
0 0 2 2 0
0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 1 0 0 0 0 2 2 2 0
0 0 9 0 0 0 0 1 1 1 0 0 0 2 0 2 0
0 9 9 0 0 0 0 0 1 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0
0 2 8 4 0
0 4 4 4 0
0 4 4 0 0
0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 1 1 1 0 0 0 0 8 0 0
0 0 9 0 0 0 0 0 0 1 0 0 0 8 8 8 0
0 0 9 0 0 0 0 0 1 1 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0
0 4 8 4 0
0 2 4 4 0
0 0 8 2 0
0 0 0 0 0
```
