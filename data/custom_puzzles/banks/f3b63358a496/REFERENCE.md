# ARC Puzzle Bank — Tenth 21 Puzzles
This tenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`64`–`70`) so it follows directly after the ninth bundle.
This volume leans into span filling, mirror completion, box abstractions, quadrant summaries, elbow routing, local flood fills, library decoding, relation matrices, ranked scaling, and code-driven mosaics.
It also introduces a few reusable solver primitives that fit your pipeline well: `span_fill`, `gate_flood`, `hole_rank_pack`, and small local `decode_then_transform` routines.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_tenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_tenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_tenth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_64_fill_between_matching_endpoints` — **Fill Between Matching Endpoints**
- `easy_65_complete_vertical_mirror` — **Complete the Vertical Mirror**
- `easy_66_draw_rectangle_borders_from_corner_pairs` — **Draw Rectangle Borders from Corner Pairs**
- `easy_67_move_cropped_object_to_top_left` — **Move the Cropped Object to the Top-Left**
- `easy_68_read_column_markers_as_row` — **Read Column Markers as a Row**
- `easy_69_cast_rightward_rays_until_wall` — **Cast Rightward Rays Until the Wall**
- `easy_70_expand_diagonal_pairs_into_xs` — **Expand Diagonal Pairs into Xs**

### Medium (7)
- `medium_64_stack_crops_by_area` — **Stack Cropped Components by Area**
- `medium_65_transform_object_by_key` — **Transform the Object by the Key Cell**
- `medium_66_build_equality_matrix_from_headers` — **Build the Equality Matrix from Headers**
- `medium_67_summarize_quadrant_majorities` — **Summarize Quadrant Majorities**
- `medium_68_connect_matching_markers_with_elbows` — **Connect Matching Markers with Elbow Paths**
- `medium_69_crop_component_with_most_holes` — **Crop the Component with the Most Holes**
- `medium_70_fill_each_components_bounding_box` — **Fill Each Component's Bounding Box**

### Hard (7)
- `hard_64_fill_local_chambers_from_gates` — **Fill Local Chambers from Gates**
- `hard_65_decode_library_transform_recolor_gallery` — **Decode the Library / Transform / Recolor Gallery**
- `hard_66_build_rotation_invariant_shape_color_relation_matrix` — **Build the Rotation-Invariant Shape / Color Relation Matrix**
- `hard_67_select_ranked_component_scale_and_place` — **Select a Ranked Component, Scale It, and Place It**
- `hard_68_build_template_transform_mosaic` — **Build the Template / Transform Mosaic**
- `hard_69_sort_by_holes_rotate_and_pack` — **Sort by Holes, Rotate, and Pack**
- `hard_70_decode_local_frame_template_codes` — **Decode the Local Frame Template Codes**

## Fill Between Matching Endpoints (`easy_64_fill_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** row spans, same-color endpoints, same-size transform

**Scaffold notes:**
- Work row by row.
- Group cells by color within each row.
- If a color appears twice, fill from its leftmost to its rightmost occurrence.

**Written solution:** Scan each row independently. Whenever the same nonzero color appears as a left and right endpoint, fill the whole horizontal span between them with that color.

**Program solution (Python reference):**
```python
def solve_easy_64_fill_between_matching_endpoints(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        pos=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append(c)
        for color, cols in pos.items():
            if len(cols)>=2:
                a,b=min(cols),max(cols)
                for c in range(a,b+1):
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
9 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Complete the Vertical Mirror (`easy_65_complete_vertical_mirror`)

**Difficulty:** easy

**Skills:** vertical reflection, symmetry completion, same-size transform

**Scaffold notes:**
- Find the mirrored column with `w-1-c`.
- Copy every colored cell to that mirrored position.
- Cells on the center column, if any, stay where they are.

**Written solution:** Reflect every nonzero cell across the vertical axis of the grid, keeping the original cells and adding their mirrored copies.

**Program solution (Python reference):**
```python
def solve_easy_65_complete_vertical_mirror(g):
    return mirror_vertical(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 7
0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 3 0 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 3 0 0 0 0 3 0
0 0 6 0 0 6 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 9
0 2 0 0 0 0 2 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0
0 5 0 0 0 0 0
0 0 1 0 0 0 0
0 0 0 0 0 0 0
7 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
0 5 0 0 0 5 0
0 0 1 0 1 0 0
0 0 0 0 0 0 0
7 0 0 0 0 0 7
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 6 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 4
0 0 7 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 1 0 1 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
```

## Draw Rectangle Borders from Corner Pairs (`easy_66_draw_rectangle_borders_from_corner_pairs`)

**Difficulty:** easy

**Skills:** bounding boxes, rectangle borders, same-color pairing

**Scaffold notes:**
- Group the two cells of each color together.
- Use their min/max rows and columns as the rectangle corners.
- Draw only the border, not a filled rectangle.

**Written solution:** Each color marks two opposite corners of an axis-aligned rectangle. Take the bounding box of each color pair and draw the full rectangle border in that color.

**Program solution (Python reference):**
```python
def solve_easy_66_draw_rectangle_borders_from_corner_pairs(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)>=2:
            r0,c0,r1,c1=bbox(cells)
            draw_rect_border(out,r0,c0,r1,c1,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0
0 2 0 0 0 2 0 7 7 7 0
0 2 0 0 0 2 0 7 0 7 0
0 2 2 2 2 2 0 7 0 7 0
0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 4 4 4 4 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 3
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 3 3 3 3
0 6 6 6 0 0 3 0 0 3
0 6 0 6 0 0 3 0 0 3
0 6 0 6 0 0 3 0 0 3
0 6 0 6 0 0 3 3 3 3
0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 9 9 9 9 9 9 0 5 0 5 0
0 0 9 0 0 0 0 9 0 5 0 5 0
0 0 9 0 0 0 0 9 0 5 0 5 0
0 0 9 0 0 0 0 9 0 5 5 5 0
0 0 9 0 0 0 0 9 0 0 0 0 0
0 0 9 9 9 9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0
2 0 0 0 2 0 0 6 6 6 6 0
2 0 0 0 2 0 0 6 0 0 6 0
2 0 0 0 2 0 0 6 0 0 6 0
2 0 0 0 2 0 0 6 6 6 6 0
2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Move the Cropped Object to the Top-Left (`easy_67_move_cropped_object_to_top_left`)

**Difficulty:** easy

**Skills:** crop to bbox, translation, same-size canvas

**Scaffold notes:**
- Ignore the empty border around the object.
- Crop exactly the nonzero bounding box.
- Paste the crop at row 0, column 0 on a blank canvas.

**Written solution:** Find the bounding box of the whole nonzero object, crop it tightly, and paste that crop into the top-left corner of a blank grid of the same original size.

**Program solution (Python reference):**
```python
def solve_easy_67_move_cropped_object_to_top_left(g):
    obj=crop_nonzero(g)
    h,w=dims(g)
    out=zeros(h,w)
    paste(out,obj,0,0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 3 0 0
0 0 0 0 2 3 3 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 3 0 0 0 0 0 0
2 3 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 1 4 0 0 0
0 0 0 0 0 1 1 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 4 0 0 0 0 0 0 0
1 4 0 0 0 0 0 0 0 0
1 1 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 7 8 8 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 0 0 0 0 0 0 0
7 8 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 8 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0
0 0 5 0 5 0 0 0
0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 5 5 0 0 0 0 0
5 0 5 0 0 0 0 0
5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 0 0 0 3 0
```

**Test output**
```text
2 2 0 0 0 0 0 0 0 0 0
0 2 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Read Column Markers as a Row (`easy_68_read_column_markers_as_row`)

**Difficulty:** easy

**Skills:** column scan, size-changing output, ordering by position

**Scaffold notes:**
- Each useful column has one nonzero marker.
- Read the columns from left to right.
- The output is a single row of the encountered colors.

**Written solution:** Look left to right across the columns. Whenever a column contains a colored marker, emit that color into a 1-row output, preserving the column order.

**Program solution (Python reference):**
```python
def solve_easy_68_read_column_markers_as_row(g):
    h,w=dims(g)
    out=[]
    for c in range(w):
        col=[g[r][c] for r in range(h) if g[r][c]!=0]
        if col:
            out.append(col[0])
    return [out]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
```

**Train 1 output**
```text
2 7 4 9
```

**Train 2 input**
```text
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
```

**Train 2 output**
```text
3 6 8 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 4
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0
5 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 2 7 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
```

**Train 4 output**
```text
9 3 6 8
```

**Test input**
```text
1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
```

**Test output**
```text
1 7 2 5
```

## Cast Rightward Rays Until the Wall (`easy_69_cast_rightward_rays_until_wall`)

**Difficulty:** easy

**Skills:** ray casting, blockers, same-size transform

**Scaffold notes:**
- Treat gray(5) as a blocker.
- Start from each non-gray seed and keep painting to the right while the cells are zero.
- Stop before the first wall or at the boundary.

**Written solution:** Every non-gray seed cell extends horizontally to the right through zero cells until it hits a gray wall or the boundary. Keep the original walls in place.

**Program solution (Python reference):**
```python
def solve_easy_69_cast_rightward_rays_until_wall(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        # seeds are nonzero except 5
        for c,v in enumerate(g[r]):
            if v!=0 and v!=5:
                cc=c+1
                while cc<w and g[r][cc]==0:
                    out[r][cc]=v
                    cc+=1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 5 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 5 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 5 0
0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 3 3 3 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 9 9 9 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0
1 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 5 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 5 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 6 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 9 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Expand Diagonal Pairs into Xs (`easy_70_expand_diagonal_pairs_into_xs`)

**Difficulty:** easy

**Skills:** 3x3 motifs, diagonal completion, same-size transform

**Scaffold notes:**
- Take the bounding box of the two same-colored cells.
- It is always a 3×3 square.
- Fill both diagonals of that square.

**Written solution:** Each color gives two opposite corners of a 3×3 box. Complete that box into a full X by drawing both diagonals in the same color.

**Program solution (Python reference):**
```python
def solve_easy_70_expand_diagonal_pairs_into_xs(g):
    h,w=dims(g)
    out=zeros(h,w)
    pos=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==2:
            r0,c0,r1,c1=bbox(cells)
            # assume square box
            for i in range(r1-r0+1):
                out[r0+i][c0+i]=color
                out[r0+i][c1-i]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 9 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 9 0 0
0 0 5 0 5 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0
1 0 1 0 0 0 7 0 0 0
0 1 0 0 0 7 0 7 0 0
1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Stack Cropped Components by Area (`medium_64_stack_crops_by_area`)

**Difficulty:** medium

**Skills:** connected components, crop to bbox, sorting by area, size-changing output

**Scaffold notes:**
- Find each connected component separately.
- Crop each one to its tight bounding box.
- Sort the crops by area, then stack them top to bottom.

**Written solution:** Split the input into connected components, crop each component to its own bounding box, sort the crops by component area from smallest to largest, and stack them vertically with one blank row between them.

**Program solution (Python reference):**
```python
def solve_medium_64_stack_crops_by_area(g):
    comps=connected_components(g)
    crops=[]
    for comp in comps:
        crops.append((comp['area'], comp['bbox'][0], comp['bbox'][1], crop_bbox(g, comp['bbox'])))
    crops=sorted(crops, key=lambda x:(x[0], x[1], x[2]))
    return vstack([c for _,_,_,c in crops], gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0
2 2 0
0 0 0
4 0 0
4 0 0
4 4 0
0 0 0
7 7 7
0 7 0
0 7 0
```

**Train 2 input**
```text
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 8 0 0 0 0 0 0 6 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 0
8 8 0
0 0 0
0 3 3
3 3 0
0 0 0
6 6 0
6 6 0
6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 0 0
9 9 0
0 0 0
2 0 0
2 0 0
2 2 0
0 0 0
5 0 5
5 0 5
5 5 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 7 0 0 0 8 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 0 0
7 7 0
0 0 0
4 4 4
0 4 0
0 4 0
0 0 0
8 8 0
8 8 0
8 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 9 0 0
0 2 2 0 0 0 0 9 0 9 0 0
2 2 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 0 0
6 0 0
6 6 0
0 0 0
0 2 2
2 2 0
0 0 0
9 0 9
9 0 9
9 9 9
```

## Transform the Object by the Key Cell (`medium_65_transform_object_by_key`)

**Difficulty:** medium

**Skills:** keyed transform, rotation, flip, size-changing output

**Scaffold notes:**
- Read the key at the top-left corner.
- Ignore that key cell when finding the object.
- Crop the object first, then apply the transform.

**Written solution:** The top-left key cell tells you how to transform the only object: 1 means identity, 2 means rotate clockwise, 3 means rotate 180°, and 4 means horizontal flip. Remove the key cell, crop the object, and output the transformed crop.

**Program solution (Python reference):**
```python
def solve_medium_65_transform_object_by_key(g):
    key=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    return apply_transform(obj, {1:1,2:2,3:3,4:4}[key])
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 3 0 0
0 0 0 0 2 3 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 3
2 3 3
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 1 4 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
1 1 0
1 4 4
0 0 4
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0
0 7 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0
8 7
0 7
```

**Train 4 input**
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9 9
5 9 0
```

**Test input**
```text
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
6 6
6 0
0 6
```

## Build the Equality Matrix from Headers (`medium_66_build_equality_matrix_from_headers`)

**Difficulty:** medium

**Skills:** row/column headers, matrix construction, size-changing output

**Scaffold notes:**
- Ignore the top-left corner.
- Compare the row's left header to the column's top header.
- Only matching nonzero colors survive into the output.

**Written solution:** Use the top row and left column as headers. For each interior position, write the header color if the row header and column header are the same nonzero color; otherwise write 0.

**Program solution (Python reference):**
```python
def solve_medium_66_build_equality_matrix_from_headers(g):
    h,w=dims(g)
    top=g[0]
    left=[g[r][0] for r in range(h)]
    out=zeros(h-1,w-1)
    for r in range(1,h):
        for c in range(1,w):
            if left[r]!=0 and left[r]==top[c]:
                out[r-1][c-1]=left[r]
    return out
```

**Train 1 input**
```text
0 2 4 2 7 4
4 0 0 0 0 0
2 0 0 0 0 0
7 0 0 0 0 0
4 0 0 0 0 0
2 0 0 0 0 0
7 0 0 0 0 0
```

**Train 1 output**
```text
0 4 0 0 4
2 0 2 0 0
0 0 0 7 0
0 4 0 0 4
2 0 2 0 0
0 0 0 7 0
```

**Train 2 input**
```text
0 3 6 3 9
9 0 0 0 0
3 0 0 0 0
6 0 0 0 0
3 0 0 0 0
9 0 0 0 0
```

**Train 2 output**
```text
0 0 0 9
3 0 3 0
0 6 0 0
3 0 3 0
0 0 0 9
```

**Train 3 input**
```text
0 8 1 8 5 1
1 0 0 0 0 0
8 0 0 0 0 0
5 0 0 0 0 0
8 0 0 0 0 0
```

**Train 3 output**
```text
0 1 0 0 1
8 0 8 0 0
0 0 0 5 0
8 0 8 0 0
```

**Train 4 input**
```text
0 2 7 7 4 2
7 0 0 0 0 0
2 0 0 0 0 0
4 0 0 0 0 0
7 0 0 0 0 0
2 0 0 0 0 0
4 0 0 0 0 0
```

**Train 4 output**
```text
0 7 7 0 0
2 0 0 0 2
0 0 0 4 0
0 7 7 0 0
2 0 0 0 2
0 0 0 4 0
```

**Test input**
```text
0 6 3 6 8
8 0 0 0 0
6 0 0 0 0
3 0 0 0 0
6 0 0 0 0
8 0 0 0 0
```

**Test output**
```text
0 0 0 8
6 0 6 0
0 3 0 0
6 0 6 0
0 0 0 8
```

## Summarize Quadrant Majorities (`medium_67_summarize_quadrant_majorities`)

**Difficulty:** medium

**Skills:** quadrant analysis, color frequency, size-changing output

**Scaffold notes:**
- Cut the grid in half vertically and horizontally.
- Count only nonzero cells within each quadrant.
- Emit the four majority colors in the same quadrant layout.

**Written solution:** Split the grid into four equal quadrants. In each quadrant, find the most frequent nonzero color and write those four answers into a 2×2 summary grid.

**Program solution (Python reference):**
```python
def solve_medium_67_summarize_quadrant_majorities(g):
    h,w=dims(g)
    hm,wm=h//2,w//2
    quads=[(0,hm,0,wm),(0,hm,wm,w),(hm,h,0,wm),(hm,h,wm,w)]
    vals=[]
    for r0,r1,c0,c1 in quads:
        cell_vals=[g[r][c] for r in range(r0,r1) for c in range(c0,c1)]
        vals.append(majority_nonzero(cell_vals))
    return [[vals[0], vals[1]],[vals[2], vals[3]]]
```

**Train 1 input**
```text
2 2 2 2 4 4 4 4
2 7 0 0 4 4 0 6
0 0 0 0 0 0 0 0
7 7 7 7 9 9 9 9
0 0 0 0 9 0 4 0
2 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 4
7 9
```

**Train 2 input**
```text
3 3 3 3 6 6 6 6
3 3 3 3 6 6 6 0
0 0 6 0 0 3 0 0
0 0 0 0 0 0 0 0
5 5 8 5 8 8 8 8
5 5 5 5 8 8 8 5
5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 6
5 8
```

**Train 3 input**
```text
1 1 1 1 1 7 7 7 7 1
1 1 0 4 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 2 2 2 2 2
4 4 4 0 7 6 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 7
4 2
```

**Train 4 input**
```text
9 9 9 9 9 2 2 2 9 2
9 9 9 9 9 2 2 2 2 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 6 6 6 6 4 4 4 4 4
6 6 6 6 6 4 4 4 4 4
6 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 2
6 4
```

**Test input**
```text
8 8 8 5 5 5
8 0 3 5 5 0
0 0 0 0 8 0
3 5 3 6 6 6
3 3 0 6 0 0
0 0 0 0 0 3
```

**Test output**
```text
8 5
3 6
```

## Connect Matching Markers with Elbow Paths (`medium_68_connect_matching_markers_with_elbows`)

**Difficulty:** medium

**Skills:** pairing, L-paths, same-size transform

**Scaffold notes:**
- Find the two markers of each color.
- Use the upper marker as the bend's starting row.
- Draw one horizontal segment and one vertical segment in the same color.

**Written solution:** Each color appears exactly twice as two markers. Connect each pair with an elbow path: draw horizontally from the upper marker to the target column, then vertically to the lower marker.

**Program solution (Python reference):**
```python
def solve_medium_68_connect_matching_markers_with_elbows(g):
    h,w=dims(g)
    out=zeros(h,w)
    pos=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==2:
            for r,c in path_elbow(cells[0], cells[1]):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 7 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 7 7 7
0 2 2 2 2 0 0 0 0 7
0 0 0 0 2 0 0 0 0 7
0 0 0 0 2 0 0 0 0 7
0 0 0 0 2 0 0 0 0 7
0 0 0 0 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 0
0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 9 0 4 0 0 0
0 0 0 0 0 0 9 0 4 0 0 0
0 0 0 0 0 0 9 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3
```

**Train 3 output**
```text
6 6 6 6 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 3 3 3
6 0 0 0 0 0 0 0 0 0 3
6 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 3
```

**Train 4 input**
```text
5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 5 5 5 5 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0
0 0 8 0 5 0 0 0 0 0
0 0 8 0 5 0 0 0 0 0
0 0 8 0 5 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 0
0 2 2 2 2 2 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Crop the Component with the Most Holes (`medium_69_crop_component_with_most_holes`)

**Difficulty:** medium

**Skills:** hole counting, component selection, crop to bbox

**Scaffold notes:**
- Crop each component to its own bounding box.
- Count zero-regions that are fully enclosed and do not touch the crop border.
- Keep the component with the highest hole count.

**Written solution:** Among all connected components, choose the one whose cropped shape contains the most enclosed holes, and output just that cropped component.

**Program solution (Python reference):**
```python
def solve_medium_69_crop_component_with_most_holes(g):
    comps=connected_components(g)
    best=None
    for comp in comps:
        crop=crop_bbox(g, comp['bbox'])
        holes=hole_count_pattern(crop)
        key=(holes, comp['area'], -comp['bbox'][0], -comp['bbox'][1])  # maximize holes then area; tie top-left earlier maybe not needed
        if best is None or key > best[0]:
            best=(key,crop)
    return best[1]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 4 4 4 0 0
0 2 2 0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 7 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 7 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 7 7 7
7 0 0 0 7
7 7 7 7 7
7 0 0 0 7
7 7 7 7 7
```

**Train 2 input**
```text
3 3 3 0 0 0 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 8 0 0 0 8 0
0 6 0 0 0 0 0 8 8 8 8 8 0
0 6 0 0 0 0 0 8 0 0 0 8 0
0 6 6 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 8
8 0 0 0 8
8 8 8 8 8
8 0 0 0 8
8 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 9 0 9 0 0 0
0 0 2 0 2 0 0 0 0 9 0 9 0 0 0
0 0 2 2 2 0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 5 5 5 5
5 0 0 0 5
5 5 5 5 5
5 0 0 0 5
5 5 5 5 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 6 0 0 0 6 0 0 0
4 0 0 0 6 6 6 6 6 0 0 0
4 0 0 0 6 0 0 0 6 0 0 0
4 4 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6 6
6 0 0 0 6
6 6 6 6 6
6 0 0 0 6
6 6 6 6 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8 8 8
8 0 0 0 8
8 8 8 8 8
8 0 0 0 8
8 8 8 8 8
```

## Fill Each Component's Bounding Box (`medium_70_fill_each_components_bounding_box`)

**Difficulty:** medium

**Skills:** bounding boxes, component abstraction, same-size transform

**Scaffold notes:**
- Find each connected component.
- Take its minimum and maximum row and column.
- Fill that whole rectangle in the component's color.

**Written solution:** Replace each component by the filled rectangle of its bounding box, using the component's own color.

**Program solution (Python reference):**
```python
def solve_medium_70_fill_each_components_bounding_box(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp['bbox']
        color=comp['color']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 4 0 0 0 0 7 7 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0
0 0 4 4 0 0 0 7 7 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 6 0 6 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 2 0 0
0 9 9 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 2 2 0
0 9 9 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 9 0 0 0 0 0 0
0 0 3 3 3 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 9 9 0 0 0 0 0
0 0 3 3 3 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Fill Local Chambers from Gates (`hard_64_fill_local_chambers_from_gates`)

**Difficulty:** hard

**Skills:** framed subproblems, flood fill, internal walls, same-size transform

**Scaffold notes:**
- Treat each frame independently.
- The gate is the only nonzero/non-wall interior seed.
- Flood through zeros only, and never cross gray walls or the frame border.

**Written solution:** Each frame encloses a little chamber puzzle. Inside a frame, start from the colored gate cell and flood only the reachable zero cells inside that frame, stopping at the frame border and the internal gray walls.

**Program solution (Python reference):**
```python
def solve_hard_64_fill_local_chambers_from_gates(g):
    return fill_from_gate_in_frame(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 5 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 5 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 5 5 5 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 5 5 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 5 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 5 5 5 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 2 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 5 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 5 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 5 5 5 2 8 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 2 2 2 2 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 7 7 7 7 7 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 7 5 5 7 7 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 7 7 5 7 7 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 7 7 5 5 5 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 7 7 7 7 7 7 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 5 5 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 5 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 5 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 4 4 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 4 4 5 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 4 4 5 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 4 4 5 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 5 5 5 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 4 4 4 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 9 9 9 9 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 9 5 9 5 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 9 5 9 5 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 9 5 9 9 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 9 9 9 9 9 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 8 8 8 8 8 8 8 8 8 0 0 8 3 0 0 0 0 0 8 0 0
0 8 0 0 0 0 0 0 0 8 0 0 8 0 0 5 5 0 0 8 0 0
0 8 0 0 0 0 5 0 0 8 0 0 8 0 0 0 5 0 0 8 0 0
0 8 0 0 0 0 5 0 0 8 0 0 8 0 0 0 5 0 0 8 0 0
0 8 0 0 5 5 5 0 0 8 0 0 8 0 0 0 5 0 0 8 0 0
0 8 6 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0 8 0 0
0 8 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 8 8 8 8 8 8 8 8 8 0 0 8 3 3 3 3 3 3 8 0 0
0 8 6 6 6 6 6 6 6 8 0 0 8 3 3 5 5 3 3 8 0 0
0 8 6 6 6 6 5 6 6 8 0 0 8 3 3 3 5 3 3 8 0 0
0 8 6 6 6 6 5 6 6 8 0 0 8 3 3 3 5 3 3 8 0 0
0 8 6 6 5 5 5 6 6 8 0 0 8 3 3 3 5 3 3 8 0 0
0 8 6 6 6 6 6 6 6 8 0 0 8 3 3 3 3 3 3 8 0 0
0 8 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 5 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 5 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 5 5 5 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 5 5 5 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 7 7 7 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 5 7 7 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 5 7 7 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 5 5 5 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 7 7 7 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 7 7 7 7 7 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 5 5 5 2 2 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 2 2 5 2 2 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 2 2 5 2 2 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 2 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 5 5 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 5 5 5 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 9 9 9 9 9 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 5 5 5 9 9 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 9 9 5 9 9 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 9 9 5 9 9 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 9 9 9 9 9 9 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 4 4 4 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 5 4 4 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 5 4 4 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 5 4 4 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 5 5 5 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 4 4 4 4 4 4 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0
```

## Decode the Library / Transform / Recolor Gallery (`hard_65_decode_library_transform_recolor_gallery`)

**Difficulty:** hard

**Skills:** library lookup, keyed transforms, recoloring, contact sheet construction

**Scaffold notes:**
- Extract the three library shapes first.
- For each active code column, read template id, transform code, and recolor target.
- Transform, recolor, crop, and append the result to the gallery.

**Written solution:** The top part is a library of three template shapes keyed by colors 1, 2, and 3. The bottom three code rows specify, column by column, which template to take, how to transform it, and what new color to paint it. Execute every code column and pack the resulting shapes into a horizontal gallery.

**Program solution (Python reference):**
```python
def solve_hard_65_decode_library_transform_recolor_gallery(g):
    h,w=dims(g)
    lib_area=[row[:] for row in g[:-3]]
    ids_row=g[-3]
    tf_row=g[-2]
    color_row=g[-1]
    library={}
    for comp in connected_components(lib_area):
        library[comp['color']]=crop_bbox(lib_area, comp['bbox'])
    parts=[]
    for c in range(w):
        tid=ids_row[c]
        if tid!=0:
            part=library[tid]
            transformed=apply_transform(part, tf_row[c])
            recolored=recolor(transformed, color_row[c])
            parts.append(crop_nonzero(recolored))
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 2 2 0 0 3 3 0 0
0 1 1 1 0 0 0 2 2 0 3 0 0 0
0 0 0 0 0 0 0 2 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 2 3 1 0 0 0 0 0 0 0 0 0 0
1 2 4 3 0 0 0 0 0 0 0 0 0 0
7 4 9 2 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 0 7 0 0 0 4 0 9 9 0 2 2 2
7 7 7 0 4 4 4 0 0 9 0 2 0 2
0 0 0 0 0 4 0 0 0 9 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 3 0 3 0
0 0 0 1 1 0 0 2 2 0 0 3 3 3 0
0 0 0 1 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 1 2 0 0 0 0 0 0 0 0 0 0 0 0
2 4 3 0 0 0 0 0 0 0 0 0 0 0 0
6 8 5 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 0 0 8 8 0 0 5
6 0 0 8 8 0 0 0 5
6 6 0 0 8 0 0 5 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 2 0 2 0 3 3 0 0
0 1 0 0 0 2 2 2 0 0 3 3 0
0 1 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 1 3 2 0 0 0 0 0 0 0 0 0
1 2 3 4 0 0 0 0 0 0 0 0 0
4 7 9 2 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 4 0 7 7 7 0 0 9 0 0 2 0 2
4 4 4 0 0 0 7 0 9 9 0 0 2 2 2
0 0 0 0 0 0 0 0 0 9 9 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0
0 1 0 1 0 0 0 2 0 0 0 3 3 0 0 0
0 1 1 1 0 0 0 2 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 2 1 0 0 0 0 0 0 0 0 0 0 0 0 0
4 1 2 0 0 0 0 0 0 0 0 0 0 0 0 0
6 8 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 6 6 0 8 8 0 5 5
6 6 0 0 8 0 0 5 0
0 6 0 0 8 0 0 5 5
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 2 0 2 0 0 3 3 0 0
0 0 1 1 0 0 2 2 2 0 0 3 0 0 0
0 0 1 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 1 2 0 0 0 0 0 0 0 0 0 0 0
2 3 4 1 0 0 0 0 0 0 0 0 0 0 0
9 4 7 5 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
9 9 0 0 4 0 0 7 7 0 5 0 5
9 0 0 0 4 0 7 7 0 0 5 5 5
9 9 0 4 4 0 0 7 0 0 0 0 0
```

## Build the Rotation-Invariant Shape / Color Relation Matrix (`hard_66_build_rotation_invariant_shape_color_relation_matrix`)

**Difficulty:** hard

**Skills:** relation matrix, rotation-invariant shape matching, component comparison

**Scaffold notes:**
- List the components in reading order.
- Normalize each shape up to rotation before comparing.
- Apply the matrix code rules cell by cell.

**Written solution:** Order the components by position. Then compare every pair of components. Put 9 on the diagonal, 6 if two different components have the same shape up to rotation and the same color, 4 if they have the same shape up to rotation but different colors, 2 if they have different shapes but the same color, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_66_build_rotation_invariant_shape_color_relation_matrix(g):
    comps=[]
    for comp in connected_components(g):
        crop=crop_bbox(g, comp['bbox'])
        comps.append((comp['bbox'][0], comp['bbox'][1], comp['color'], normalize_shape_rot(crop)))
    comps.sort(key=lambda x:(x[0],x[1]))
    n=len(comps)
    out=zeros(n,n)
    for i,(_,_,ci,si) in enumerate(comps):
        for j,(_,_,cj,sj) in enumerate(comps):
            if i==j:
                out[i][j]=9
            elif si==sj and ci==cj:
                out[i][j]=6
            elif si==sj and ci!=cj:
                out[i][j]=4
            elif si!=sj and ci==cj:
                out[i][j]=2
            else:
                out[i][j]=0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 2 2 2 0 0 0
0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 7 7 0 0 0
0 0 7 0 0 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
9 6 0 4
6 9 0 4
0 0 9 2
4 4 2 9
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 4 0 0 0 0
0 4 4 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 8 8 0 0
0 0 8 8 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
9 6 0 4
6 9 0 4
0 0 9 2
4 4 2 9
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 6 6 6 0 0
0 3 3 0 0 0 0 0 0 0 0 0 6 6 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 4 2 0
4 9 0 0
2 0 9 4
0 0 4 9
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 5 5 5 0 0
0 0 5 0 5 0 0 0 0 0 5 0 0 0 0
0 0 5 5 5 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 8 8 8 0 0
0 0 8 0 0 0 0 0 0 0 8 0 8 0 0
0 8 8 0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 6 0 4
6 9 0 4
0 0 9 2
4 4 2 9
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 7 7 0 0
0 2 2 0 0 0 0 0 0 7 7 0 0 0
0 0 2 2 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 2 2 0 0 0
0 0 0 2 0 0 0 0 0 0 2 2 0 0
0 0 0 2 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
9 4 2 6
4 9 0 4
2 0 9 2
6 4 2 9
```

## Select a Ranked Component, Scale It, and Place It (`hard_67_select_ranked_component_scale_and_place`)

**Difficulty:** hard

**Skills:** ranking by area, component selection, 2x scaling, placement by marker

**Scaffold notes:**
- Ignore the rank key and the marker when finding components.
- Sort the components by area.
- Scale the chosen crop by 2 and paste it at the marker position on a blank canvas.

**Written solution:** Read the rank key in the top-left corner: 1 means the smallest component, 2 the second-smallest, 3 the largest among the puzzle components. Select that component, scale it by 2 in both directions, and place the enlarged crop so that its top-left corner lands on the special marker cell.

**Program solution (Python reference):**
```python
def solve_hard_67_select_ranked_component_scale_and_place(g):
    rank=g[0][0]  # 1-based ascending by area
    marker=None
    h,w=dims(g)
    gg=clone(g)
    gg[0][0]=0
    for r in range(h):
        for c in range(w):
            if gg[r][c]==9:
                marker=(r,c)
                gg[r][c]=0
    comps=connected_components(gg)
    comps_sorted=sorted(comps, key=lambda comp:(comp['area'], comp['bbox'][0], comp['bbox'][1]))
    chosen=comps_sorted[rank-1]
    crop=crop_bbox(gg, chosen['bbox'])
    big=scale2(crop)
    out=zeros(h,w)
    paste(out,big,marker[0],marker[1])
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 6 6 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Build the Template / Transform Mosaic (`hard_68_build_template_transform_mosaic`)

**Difficulty:** hard

**Skills:** template tiling, code decoding, rotations, size-changing output

**Scaffold notes:**
- Extract the two templates from the top area.
- Decode each code cell into the appropriate template choice.
- Lay the resulting tiles out in the same grid pattern, leaving 1-cell gaps.

**Written solution:** The top area contains two square templates. The bottom code grid tells you which tile to place at each output position: 1 uses template A, 2 uses template B, 3 uses rotated template A, and 4 uses rotated template B. Build the whole tiled mosaic with one blank row and column between neighboring tiles.

**Program solution (Python reference):**
```python
def solve_hard_68_build_template_transform_mosaic(g):
    h,w=dims(g)
    top_area=[row[:] for row in g[:-2]]
    code_grid=[row[:] for row in g[-2:]]
    comps=connected_components(top_area)
    templates={}
    for comp in comps:
        templates[comp['color']]=crop_bbox(top_area, comp['bbox'])
    tile_h, tile_w = dims(next(iter(templates.values())))
    nz_cols=[c for c in range(w) if any(code_grid[r][c]!=0 for r in range(len(code_grid)))]
    if not nz_cols:
        return [[0]]
    c0,c1=min(nz_cols),max(nz_cols)
    cols=c1-c0+1
    rows=len(code_grid)
    out=zeros(rows*tile_h + (rows-1), cols*tile_w + (cols-1))
    for rr,row in enumerate(code_grid):
        for cc,c in enumerate(range(c0,c1+1)):
            code=row[c]
            if code==0: 
                continue
            if code==1: tile=templates[1]
            elif code==2: tile=templates[2]
            elif code==3: tile=rotate_cw(templates[1])
            elif code==4: tile=rotate_cw(templates[2])
            else: 
                continue
            paste(out, tile, rr*(tile_h+1), cc*(tile_w+1))
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 2 2 0 0
0 1 1 0 0 0 0 2 2 0 0 0
0 1 1 1 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 2 3 0 0 0 0 0 0 0 0 0
4 1 2 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 0 0 0 0 2 2 0 1 1 1
1 1 0 0 2 2 0 0 1 1 0
1 1 1 0 2 2 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 1 0 0 0 0 2 2
2 2 2 0 1 1 0 0 2 2 0
0 0 2 0 1 1 1 0 2 2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 2 0 0 0 0
0 1 1 0 0 0 0 0 2 2 0 0 0
0 1 1 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 4 1 0 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
1 1 0 0 2 2 2 0 0 1 1
1 1 1 0 2 2 0 0 1 1 0
0 0 1 0 2 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 1 1 0 0 0 0 0
2 2 0 0 1 1 1 0 0 0 0
2 2 2 0 0 0 1 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 2 2 0 0
0 1 1 0 0 0 0 2 2 0 0 0
0 1 1 1 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 1 4 0 0 0 0 0 0 0 0 0
3 2 1 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 2 2 0 1 0 0 0 2 2 0
2 2 0 0 1 1 0 0 2 2 2
2 2 0 0 1 1 1 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 2 2 0 1 0 0
1 1 0 0 2 2 0 0 1 1 0
1 0 0 0 2 2 0 0 1 1 1
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 2 0 0 0 0
0 0 1 1 0 0 0 0 0 2 2 0 0 0
0 0 1 1 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 3 2 0 0 0 0 0 0 0 0 0 0 0
1 2 4 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 2 0 1 1 0 0 2 0 0
2 2 0 0 1 1 1 0 2 2 0
2 0 0 0 0 0 1 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 2 0 0 0 2 2 2
1 1 0 0 2 2 0 0 2 2 0
1 1 0 0 2 2 2 0 2 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 2 2 0 0
0 1 1 0 0 0 0 0 2 2 0 0 0
0 1 1 1 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 4 2 0 0 0 0 0 0 0 0 0 0
3 1 4 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
1 0 0 0 2 2 0 0 0 2 2
1 1 0 0 2 2 2 0 2 2 0
1 1 1 0 0 0 2 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 1 0 0 0 2 2 0
1 1 0 0 1 1 0 0 2 2 2
1 0 0 0 1 1 1 0 0 0 2
```

## Sort by Holes, Rotate, and Pack (`hard_69_sort_by_holes_rotate_and_pack`)

**Difficulty:** hard

**Skills:** hole counting, sorting, rotation, gallery construction

**Scaffold notes:**
- Crop components tightly before counting holes.
- Sort first by hole count, then by area.
- Rotate each crop clockwise and concatenate them with 1-cell gaps.

**Written solution:** Find every component, count how many enclosed holes its cropped shape has, sort the components by hole count and then by area, rotate each crop clockwise, and pack the rotated crops into a horizontal strip.

**Program solution (Python reference):**
```python
def solve_hard_69_sort_by_holes_rotate_and_pack(g):
    items=[]
    for comp in connected_components(g):
        crop=crop_bbox(g, comp['bbox'])
        holes=hole_count_pattern(crop)
        items.append((holes, comp['area'], comp['bbox'][0], comp['bbox'][1], rotate_cw(crop)))
    items.sort(key=lambda x:(x[0], x[1], x[2], x[3]))
    return hstack([item[-1] for item in items], gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 4 4 4 0 0 0 0
0 2 2 0 0 0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 7 7 7 7 7
2 2 2 0 4 4 4 0 7 0 7 0 7
2 0 0 0 4 0 4 0 7 0 7 0 7
0 0 0 0 4 4 4 0 7 0 7 0 7
0 0 0 0 0 0 0 0 7 7 7 7 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 8 0 0
0 6 0 6 0 0 0 0 0 0 8 8 8 8 8 0 0
0 6 0 6 0 0 0 0 0 0 8 0 0 0 8 0 0
0 6 6 6 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 8 8 8 8 8
6 6 6 0 3 3 3 0 8 0 8 0 8
6 0 0 0 3 0 3 0 8 0 8 0 8
6 6 6 0 3 3 3 0 8 0 8 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 5 5 5 5 5
9 9 9 0 2 2 2 0 5 0 5 0 5
9 0 0 0 2 0 2 0 5 0 5 0 5
0 0 0 0 2 2 2 0 5 0 5 0 5
0 0 0 0 0 0 0 0 5 5 5 5 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 6 6 6 6 6
7 7 7 0 4 4 4 0 6 0 6 0 6
7 0 0 0 4 0 4 0 6 0 6 0 6
7 7 7 0 4 4 4 0 6 0 6 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 3 0 0 0 0 0 0 0 8 0 0 0 8 0 0
0 0 3 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 3 3 0 0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 8 8 8 8 8
3 3 3 0 6 6 6 0 8 0 8 0 8
3 0 0 0 6 0 6 0 8 0 8 0 8
0 0 0 0 6 6 6 0 8 0 8 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8
```

## Decode the Local Frame Template Codes (`hard_70_decode_local_frame_template_codes`)

**Difficulty:** hard

**Skills:** framed subproblems, local template selection, local transform codes, recoloring, packing

**Scaffold notes:**
- Treat each frame as its own little coded puzzle.
- Read the selector and transform code from the frame's bottom interior row.
- Choose the matching candidate, transform it, recolor it to the frame border color, and append it to the gallery.

**Written solution:** Each frame contains two candidate templates, a selector code, and a transform code. Use the selector to choose the left or right candidate, apply the local transform, recolor the result to the frame border's color, and pack the chosen outputs from all frames into a horizontal gallery.

**Program solution (Python reference):**
```python
def solve_hard_70_decode_local_frame_template_codes(g):
    h,w=dims(g)
    # frames are rectangular borders of colors >=7
    frame_grid=[[v if v>=7 else 0 for v in row] for row in g]
    comps=connected_components(frame_grid)
    frames=sorted([(comp['bbox'][0], comp['bbox'][1], comp['bbox'][2], comp['bbox'][3], comp['color']) for comp in comps], key=lambda x:(x[0],x[1]))
    parts=[]
    for r0,c0,r1,c1,bcolor in frames:
        # interior coordinates
        bottom=r1-1
        sel=g[bottom][c0+1]
        tf=g[bottom][c0+2]
        # candidate A color 1, candidate B color 2 above bottom row within interior
        sub=[[g[r][c] if r<bottom else 0 for c in range(c0+1,c1)] for r in range(r0+1,r1)]
        # Actually crop candidates by color in upper interior excluding bottom row
        upper=[[g[r][c] if r<bottom else 0 for c in range(c0+1,c1)] for r in range(r0+1,r1)]
        # build left/right objects manually by color
        cand_grid=[[g[r][c] if r<bottom and g[r][c]==sel else 0 for c in range(c0+1,c1)] for r in range(r0+1,r1)]
        # This selects by sel color but may include selection cell if same row? excluded by r<bottom.
        chosen=crop_nonzero(cand_grid)
        transformed=apply_transform(chosen, {3:1,4:2,5:3,6:4}[tf])
        parts.append(recolor(transformed, bcolor))
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 0 0 8 8 8 8 8 8 8 8 8 0
0 7 1 0 0 0 2 2 0 7 0 0 8 1 1 0 0 2 2 0 8 0
0 7 1 1 0 2 2 0 0 7 0 0 8 0 1 1 0 2 0 0 8 0
0 7 0 0 0 0 0 0 0 7 0 0 8 0 0 0 0 2 0 0 8 0
0 7 0 0 0 0 0 0 0 7 0 0 8 0 0 0 0 0 0 0 8 0
0 7 1 4 0 0 0 0 0 7 0 0 8 0 0 0 0 0 0 0 8 0
0 7 7 7 7 7 7 7 7 7 0 0 8 2 5 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 0 0 8
7 0 0 0 8
0 0 0 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 1 1 0 2 0 0 9 0 0 7 7 7 7 7 7 7 7 7 0 0
0 9 1 1 0 0 2 2 0 9 0 0 7 1 1 0 2 2 0 0 7 0 0
0 9 0 0 0 0 0 0 0 9 0 0 7 1 0 0 0 2 2 0 7 0 0
0 9 0 0 0 0 0 0 0 9 0 0 7 1 0 0 0 0 0 0 7 0 0
0 9 0 0 0 0 0 0 0 9 0 0 7 0 0 0 0 0 0 0 7 0 0
0 9 2 3 0 0 0 0 0 9 0 0 7 1 6 0 0 0 0 0 7 0 0
0 9 9 9 9 9 9 9 9 9 0 0 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
9 0 0 7 7
9 9 0 0 7
0 0 0 0 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 1 1 0 0 2 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 1 1 0 2 2 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 8 0 0 9 9 9 9 9 9 9 9 9 0 0
0 0 8 0 0 0 0 0 0 0 8 0 0 9 0 1 1 0 2 2 0 9 0 0
0 0 8 1 5 0 0 0 0 0 8 0 0 9 1 1 0 0 2 0 0 9 0 0
0 0 8 8 8 8 8 8 8 8 8 0 0 9 0 0 0 0 2 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 2 4 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0 0 9 9 9
0 8 8 0 0 0 9
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 0
0 7 7 7 7 7 7 7 7 7 0 0 8 1 0 0 2 2 0 0 8 0
0 7 1 1 0 0 2 2 0 7 0 0 8 1 1 0 0 2 2 0 8 0
0 7 1 0 0 2 2 0 0 7 0 0 8 0 0 0 0 0 0 0 8 0
0 7 1 0 0 0 0 0 0 7 0 0 8 0 0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0 0 7 0 0 8 1 3 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0 0 7 0 0 8 8 8 8 8 8 8 8 8 0
0 7 2 6 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0 7 7 0
8 8 0 0 7 7
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 1 1 0 2 2 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 1 1 0 0 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 2 0 0 9 0 0 7 7 7 7 7 7 7 7 7 0 0
0 9 0 0 0 0 0 0 0 9 0 0 7 1 1 0 0 2 0 0 7 0 0
0 9 1 4 0 0 0 0 0 9 0 0 7 0 1 1 0 2 2 0 7 0 0
0 9 9 9 9 9 9 9 9 9 0 0 7 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 2 5 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
9 0 0 7 7
9 9 0 0 7
0 9 0 0 0
```