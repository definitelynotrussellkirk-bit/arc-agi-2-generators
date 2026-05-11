# ARC Puzzle Bank — Eighteenth 21 Puzzles
This eighteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`120`–`126`) so it follows directly after the seventeenth bundle.
This volume pushes the mechanic mix in a somewhat different direction: vertical mirroring, span-filling, diamond growth, row packing, legend-guided object selection, frame-intersection construction, chamber-local gravity, reflection matching, area ranking, rotation-relation matrices, prototype-library decoding, directed ray count maps, priority-based chamber filling, pairwise XOR galleries, nearest-seed filling, and centered transformed stamp overlays.
It also introduces and reuses a few convenient primitives for solver work: `radius1_diamond_expand`, `directed_raycast_count`, `panel_xor_gallery`, and `centered_transform_stamp`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_eighteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_eighteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_eighteenth_21.md` — this human-readable catalog.

## Easy (7)
- `easy_120_complete_vertical_mirror` — **Complete the Vertical Mirror**
- `easy_121_fill_horizontal_spans_between_matching_endpoints` — **Fill Horizontal Spans Between Matching Endpoints**
- `easy_122_fill_vertical_spans_between_matching_endpoints` — **Fill Vertical Spans Between Matching Endpoints**
- `easy_123_expand_singletons_to_radius1_diamonds` — **Expand Singletons to Radius-1 Diamonds**
- `easy_124_right_pack_each_row_preserving_order` — **Right-Pack Each Row Preserving Order**
- `easy_125_crop_the_nonzero_bounding_box` — **Crop the Nonzero Bounding Box**
- `easy_126_fill_diagonal_segments_between_matching_endpoints` — **Fill Diagonal Segments Between Matching Endpoints**

## Medium (7)
- `medium_120_select_object_by_corner_legend_and_crop` — **Select the Legend-Matched Object and Crop It**
- `medium_121_fill_intersections_from_frame_markers` — **Fill Intersections from Frame Markers**
- `medium_122_apply_gravity_in_each_walled_chamber` — **Apply Gravity in Each Walled Chamber**
- `medium_123_select_reflection_match_and_recolor` — **Find the Reflected Match and Recolor It**
- `medium_124_connect_color_pairs_with_clear_elbows` — **Connect Color Pairs with the Clear Elbow**
- `medium_125_recolor_components_by_area_rank` — **Recolor Components by Area Rank**
- `medium_126_select_ranked_object_and_scale2` — **Select the Ranked Object and Scale It 2x**

## Hard (7)
- `hard_120_build_rotation_equivalence_matrix` — **Build the Rotation Equivalence Matrix**
- `hard_121_decode_library_with_transform_codes` — **Decode the Prototype Library with Transform Codes**
- `hard_122_overlay_rays_until_block_count_map` — **Overlay Directed Rays into a Count Map**
- `hard_123_fill_chambers_by_seed_priority_legend` — **Fill Chambers by Seed Priority Legend**
- `hard_124_build_pairwise_xor_gallery` — **Build the Pairwise XOR Gallery**
- `hard_125_fill_chambers_by_nearest_seed` — **Fill Chambers by Nearest Seed**
- `hard_126_centered_transformed_stamp_count_map` — **Build a Centered Transformed Stamp Count Map**

## Complete the Vertical Mirror (`easy_120_complete_vertical_mirror`)

**Difficulty:** easy

**Skills:** vertical symmetry completion, same-size transform, copying structure


**Scaffold notes:**
- Reflect the grid across its vertical midline.
- Each nonzero cell should also appear in the mirrored column on the other side.
- Keep original cells and add their reflected copies.


**Written solution:** Reflect every nonzero cell across the vertical axis. For each colored cell, copy the same color to the column equally far from the right edge.

**Program solution (Python reference):**
```python
def solve_easy_120_complete_vertical_mirror(g):
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
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 2 0
0 0 0 4 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 7
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 7
0 9 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0
0 0 4 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Fill Horizontal Spans Between Matching Endpoints (`easy_121_fill_horizontal_spans_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** rowwise interval filling, color matching, same-size transform


**Scaffold notes:**
- Look for rows that contain exactly two nonzero cells of the same color.
- Those cells are endpoints of a horizontal segment.
- Fill every cell between them with that same color.


**Written solution:** For each row, if the row contains exactly two matching colored endpoints, fill the entire inclusive horizontal interval between them with that color.

**Program solution (Python reference):**
```python
def solve_easy_121_fill_horizontal_spans_between_matching_endpoints(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        pos=[c for c,v in enumerate(g[r]) if v!=0]
        if len(pos)==2 and g[r][pos[0]]==g[r][pos[1]]:
            color=g[r][pos[0]]
            for c in range(pos[0], pos[1]+1):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 2 0 0 0
0 9 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0
0 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
8 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Fill Vertical Spans Between Matching Endpoints (`easy_122_fill_vertical_spans_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** columnwise interval filling, color matching, same-size transform


**Scaffold notes:**
- Look for columns that contain exactly two nonzero cells of the same color.
- Those two cells define the endpoints of a vertical segment.
- Fill the full inclusive column segment between them.


**Written solution:** For each column, if there are exactly two matching colored endpoints, fill all cells between the top and bottom endpoint with that color.

**Program solution (Python reference):**
```python
def solve_easy_122_fill_vertical_spans_between_matching_endpoints(g):
    h,w=dims(g)
    out=clone(g)
    for c in range(w):
        pos=[r for r in range(h) if g[r][c]!=0]
        if len(pos)==2 and g[pos[0]][c]==g[pos[1]][c]:
            color=g[pos[0]][c]
            for r in range(pos[0], pos[1]+1):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 7 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0
```

**Train 1 output**
```text
0 0 0 0 7 0 0 0
0 2 0 0 7 0 0 0
0 2 0 0 7 0 4 0
0 2 0 0 7 0 4 0
0 2 0 0 7 0 4 0
0 2 0 0 7 0 4 0
0 2 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 7 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 5 0
0 0 0 8 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
3 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 5 0
0 0 0 8 0 0 0 0 5 0
3 0 0 8 0 0 0 0 5 0
3 0 0 8 0 0 0 0 5 0
3 0 0 8 0 0 0 0 5 0
3 0 0 0 0 0 0 0 5 0
3 0 0 0 0 0 0 0 5 0
3 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 2 0
0 0 6 0 0 0 0 2 0
0 0 6 0 0 4 0 2 0
0 0 6 0 0 4 0 2 0
0 0 6 0 0 4 0 0 0
0 0 6 0 0 4 0 0 0
0 0 6 0 0 4 0 0 0
0 0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
```

**Train 4 input**
```text
0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 9 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 7 0
0 9 0 0 3 0 0 0 0 7 0
0 9 0 0 3 0 0 0 0 7 0
0 9 0 0 3 0 0 0 0 7 0
0 9 0 0 0 0 0 0 0 7 0
0 9 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
8 0 0 0 0 0 5 0
8 0 0 0 0 0 5 0
8 0 0 2 0 0 5 0
8 0 0 2 0 0 5 0
8 0 0 2 0 0 5 0
8 0 0 2 0 0 5 0
8 0 0 2 0 0 0 0
8 0 0 2 0 0 0 0
8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
```


## Expand Singletons to Radius-1 Diamonds (`easy_123_expand_singletons_to_radius1_diamonds`)

**Difficulty:** easy

**Skills:** local expansion, diamond neighborhood, same-size transform


**Scaffold notes:**
- Each nonzero cell acts as the center of a small diamond.
- Add its four cardinal neighbors while keeping the center.
- Clip naturally at the borders if a neighbor would fall outside the grid.


**Written solution:** Replace each singleton seed by a radius-1 diamond: keep the center cell and color its up, down, left, and right neighbors with the same color whenever they are in bounds.

**Program solution (Python reference):**
```python
def solve_easy_123_expand_singletons_to_radius1_diamonds(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color!=0:
                for dr,dc in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 4 4 4 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 0 0
0 0 0 8 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 0 1 0 0 9 0
0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 9 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
0 0 8 0 0 3 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
```


## Right-Pack Each Row Preserving Order (`easy_124_right_pack_each_row_preserving_order`)

**Difficulty:** easy

**Skills:** row compaction, order preservation, same-size transform


**Scaffold notes:**
- Treat each row independently.
- Ignore zeros, keep the nonzero sequence in its original left-to-right order.
- Move that sequence flush against the right edge.


**Written solution:** For each row, collect the nonzero entries in order and place them at the far right of the row, leaving zeros on the left.

**Program solution (Python reference):**
```python
def solve_easy_124_right_pack_each_row_preserving_order(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        start=w-len(vals)
        for i,v in enumerate(vals):
            out[r][start+i]=v
    return out
```

**Train 1 input**
```text
0 2 0 3 0 4 0 0
5 0 0 6 0 0 0 0
0 0 7 0 8 0 9 0
0 0 0 0 0 0 0 0
1 0 2 0 0 3 0 0
```

**Train 1 output**
```text
0 0 0 0 0 2 3 4
0 0 0 0 0 0 5 6
0 0 0 0 0 7 8 9
0 0 0 0 0 0 0 0
0 0 0 0 0 1 2 3
```

**Train 2 input**
```text
4 0 0 0 5 0 6
0 7 0 8 0 0 0
9 0 1 0 2 0 3
0 0 0 0 0 4 0
5 6 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 4 5 6
0 0 0 0 0 7 8
0 0 0 9 1 2 3
0 0 0 0 0 0 4
0 0 0 0 0 5 6
```

**Train 3 input**
```text
0 0 3 0 0 4 0 5 0
6 0 0 0 7 0 0 0 8
0 9 0 1 0 2 0 0 0
3 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 3 4 5
0 0 0 0 0 0 6 7 8
0 0 0 0 0 0 9 1 2
0 0 0 0 0 0 0 0 3
```

**Train 4 input**
```text
0 2 0 0 0 0
3 0 4 0 5 0
0 0 0 6 0 7
8 0 0 0 0 0
0 9 1 0 0 2
```

**Train 4 output**
```text
0 0 0 0 0 2
0 0 0 3 4 5
0 0 0 0 6 7
0 0 0 0 0 8
0 0 0 9 1 2
```

**Test 1 input**
```text
1 0 0 2 0 3 0 4 0 0
0 5 0 0 6 0 0 7 0 0
8 0 9 0 0 1 0 0 0 0
0 0 0 0 2 0 3 0 4 0
```

**Test 1 output**
```text
0 0 0 0 0 0 1 2 3 4
0 0 0 0 0 0 0 5 6 7
0 0 0 0 0 0 0 8 9 1
0 0 0 0 0 0 0 2 3 4
```


## Crop the Nonzero Bounding Box (`easy_125_crop_the_nonzero_bounding_box`)

**Difficulty:** easy

**Skills:** bounding box extraction, size change, cropping


**Scaffold notes:**
- Ignore the zero padding around the pattern.
- Find the smallest rectangle containing every nonzero cell.
- Return exactly that cropped rectangle.


**Written solution:** Find the minimal axis-aligned bounding box that contains all nonzero cells and crop the grid to that box.

**Program solution (Python reference):**
```python
def solve_easy_125_crop_the_nonzero_bounding_box(g):
    return crop_nonzero(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0
0 3 3
4 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0
0 5 5 5 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 0 5
5 5 5 0
0 5 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0
7 7
0 7
7 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8
8 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 9 0 0 9 0 0
0 0 0 0 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 9 9 0
9 0 0 9
9 9 9 9
```


## Fill Diagonal Segments Between Matching Endpoints (`easy_126_fill_diagonal_segments_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** diagonal interval filling, 45-degree geometry, same-size transform


**Scaffold notes:**
- Each color appears as a pair of endpoints on a 45-degree diagonal.
- The output fills the cells between those endpoints.
- Work color by color and follow the diagonal step by step.


**Written solution:** For each color that appears exactly twice on a 45-degree diagonal, fill every cell along the inclusive diagonal segment joining those two endpoints.

**Program solution (Python reference):**
```python
def solve_easy_126_fill_diagonal_segments_between_matching_endpoints(g):
    h,w=dims(g)
    out=clone(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        if len(pts)==2:
            (r1,c1),(r2,c2)=pts
            dr,dc=r2-r1,c2-c1
            if abs(dr)==abs(dc):
                sr,sc=sign(dr),sign(dc)
                steps=abs(dr)
                for k in range(steps+1):
                    out[r1+sr*k][c1+sc*k]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 2 7 0 0 0
0 0 0 7 2 0 0 0
0 0 7 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3 0
0 8 0 0 0 0 0 3 0 0
0 0 8 0 0 0 3 0 0 0
0 0 0 8 0 3 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 0 0 0 0
6 0 0 0 4 0 0 0 0 0
0 6 0 4 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 2 0 0 0 0
0 0 0 0 9 0 0 0 2 0 0 0
0 0 0 0 0 9 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 7 0 5 0 0
0 0 0 7 0 0 0 5 0
0 0 7 0 0 0 0 0 5
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## Select the Legend-Matched Object and Crop It (`medium_120_select_object_by_corner_legend_and_crop`)

**Difficulty:** medium

**Skills:** legend lookup, object selection, cropping


**Scaffold notes:**
- The top-left corner cell is a legend telling you which color matters.
- Find the unique connected object of that color elsewhere in the grid.
- Crop the output to that object's bounding box.


**Written solution:** Read the legend color from the top-left cell, locate the connected object with that same color, and return the cropped bounding box of that object.

**Program solution (Python reference):**
```python
def solve_medium_120_select_object_by_corner_legend_and_crop(g):
    legend=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    comps=connected_components(gg)
    target=None
    for cells in comps:
        colors={gg[r][c] for r,c in cells if gg[r][c]!=0}
        if len(colors)==1 and next(iter(colors))==legend:
            target=component_grid(gg, cells)
            break
    return target if target is not None else [[0]]
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 3 0 0 0 0 0 4 0 0 0
0 0 3 0 0 0 0 0 4 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 0 0
3 0 0
3 3 3
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 6 6 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 8 0 0 0 6 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6
6 6
6 0
```

**Train 3 input**
```text
8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 4 0 4 0 0 0 8 0 0 0
0 0 0 4 0 4 0 0 0 8 0 0 0
0 0 0 4 4 4 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0
8 0 0
8 0 0
8 8 8
```

**Train 4 input**
```text
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 4 0 0 0 0 0 2 0
0 4 4 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 4 0
4 4 4
0 4 0
```

**Test 1 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 9 9 9 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 7 7
7 0 0
7 0 0
7 7 7
```


## Fill Intersections from Frame Markers (`medium_121_fill_intersections_from_frame_markers`)

**Difficulty:** medium

**Skills:** frame parsing, row/column selection, intersection construction


**Scaffold notes:**
- The rectangular frame defines the active region.
- Special markers on the top border select columns; markers on the left border select rows.
- Place new cells at every interior intersection of a selected row and selected column.


**Written solution:** Detect the frame, read the marked rows from its left border and the marked columns from its top border, then fill every corresponding interior intersection with the output color.

**Program solution (Python reference):**
```python
def solve_medium_121_fill_intersections_from_frame_markers(g):
    h,w=dims(g)
    out=clone(g)
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c] in (8,2)]
    r0,c0,r1,c1=bbox(frame_cells)
    row_marks=[r for r in range(r0+1,r1) if g[r][c0]==2]
    col_marks=[c for c in range(c0+1,c1) if g[r0][c]==2]
    for r in row_marks:
        for c in col_marks:
            if g[r][c]==0:
                out[r][c]=3
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 2 8 8 2 8 2 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 2 8 8 2 8 2 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 3 0 0 3 0 3 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 3 0 0 3 0 3 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 8 8 2 8 8 2 8 8 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 8 8 0
```

**Train 2 output**
```text
0 8 8 2 8 8 2 8 8 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 3 0 0 3 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 3 0 0 3 0 0 8 0
0 8 0 0 0 0 0 0 0 8 0
0 2 0 3 0 0 3 0 0 8 0
0 8 8 8 8 8 8 8 8 8 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 2 8 2 8 2 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 2 8 2 8 2 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 3 0 3 0 3 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 2 0 0 3 0 3 0 3 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 8 2 8 2 8 8 2 8 0
0 2 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 8 2 8 2 8 8 2 8 0
0 2 3 0 3 0 0 3 8 0
0 8 0 0 0 0 0 0 8 0
0 2 3 0 3 0 0 3 8 0
0 2 3 0 3 0 0 3 8 0
0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 2 8 8 8 2 8 2 8 0
0 0 0 2 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 2 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 2 0 0 0 0 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 2 8 8 8 2 8 2 8 0
0 0 0 2 3 0 0 0 3 0 3 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 2 3 0 0 0 3 0 3 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0
0 0 0 2 3 0 0 0 3 0 3 8 0
0 0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Apply Gravity in Each Walled Chamber (`medium_122_apply_gravity_in_each_walled_chamber`)

**Difficulty:** medium

**Skills:** wall segmentation, local gravity, columnwise motion


**Scaffold notes:**
- Walls split the grid into independent chambers.
- Within each chamber, colored cells fall downward inside their own columns.
- Relative top-to-bottom order in a column is preserved.


**Written solution:** Treat each wall-separated chamber independently. In every chamber column, let the nonzero cells fall to the bottom of the available cells while preserving their order.

**Program solution (Python reference):**
```python
def solve_medium_122_apply_gravity_in_each_walled_chamber(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    regions=find_regions_without_walls(g, wall=5)
    for cells in regions:
        rs=[r for r,c in cells]; cs=[c for r,c in cells]
        r0,r1=min(rs),max(rs)
        c0,c1=min(cs),max(cs)
        cellset=set(cells)
        for c in range(c0,c1+1):
            col_cells=[r for r in range(r0,r1+1) if (r,c) in cellset]
            vals=[g[r][c] for r in col_cells if g[r][c]!=0]
            start=len(col_cells)-len(vals)
            for i,r in enumerate(col_cells):
                out[r][c]=vals[i-start] if i>=start else out[r][c]
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 2 0 5 0 3 0 0 4 5
5 1 0 0 5 0 0 0 2 0 5
5 0 0 3 5 4 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 1 5 0 2 0 3 0 5
5 4 0 0 5 0 0 0 0 0 5
5 0 3 0 5 1 0 4 0 2 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 0 0 5
5 0 0 0 5 0 0 0 0 0 5
5 1 2 3 5 4 3 0 2 4 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 0 0 5
5 0 0 0 5 0 0 0 0 0 5
5 4 3 1 5 1 2 4 3 2 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5 5
5 0 2 0 5 0 3 0 5
5 1 0 4 5 2 0 0 5
5 0 0 0 5 0 1 0 5
5 5 5 5 5 5 5 5 5
5 3 0 0 5 0 4 0 5
5 0 2 0 5 1 0 2 5
5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 3 0 5
5 1 2 4 5 2 1 0 5
5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5
5 3 2 0 5 1 4 2 5
5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5 5 5
5 0 1 0 5 0 2 0 0 5
5 3 0 4 5 0 0 0 1 5
5 0 0 0 5 2 0 3 0 5
5 5 5 5 5 5 5 5 5 5
5 4 0 0 5 0 1 0 2 5
5 0 2 3 5 0 0 4 0 5
5 0 0 0 5 3 0 0 1 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 0 5
5 0 0 0 5 0 0 0 0 5
5 3 1 4 5 2 2 3 1 5
5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 0 5
5 0 0 0 5 0 0 0 2 5
5 4 2 3 5 3 1 4 1 5
5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 0 2 0 5 0 3 0 5 4 0 5
5 1 0 0 5 0 0 1 5 0 0 5
5 0 0 4 5 2 0 0 5 3 0 5
5 5 5 5 5 5 5 5 5 5 5 5
5 0 1 0 5 4 0 0 5 0 2 5
5 3 0 0 5 0 0 2 5 1 0 5
5 0 0 0 5 0 3 0 5 0 4 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 5 0 0 0 5 4 0 5
5 1 2 4 5 2 3 1 5 3 0 5
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 5 0 0 0 5 0 2 5
5 3 1 0 5 4 3 2 5 1 4 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
5 5 5 5 5 5 5 5 5
5 0 1 0 5 0 2 0 5
5 3 0 4 5 0 0 1 5
5 0 2 0 5 4 0 0 5
5 5 5 5 5 5 5 5 5
5 1 0 0 5 0 3 0 5
5 0 4 0 5 2 0 1 5
5 0 0 3 5 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5
5 0 1 0 5 0 0 0 5
5 3 2 4 5 4 2 1 5
5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 1 4 3 5 2 3 1 5
5 5 5 5 5 5 5 5 5
```


## Find the Reflected Match and Recolor It (`medium_123_select_reflection_match_and_recolor`)

**Difficulty:** medium

**Skills:** shape normalization, reflection matching, object recoloring


**Scaffold notes:**
- One object is the prototype; the others are candidates.
- Exactly one candidate is the prototype under a reflection.
- Recolor only that matching candidate.


**Written solution:** Use the color-1 object as the prototype, compare candidate color-2 objects after cropping and binarizing, find the one equal to a reflected version of the prototype, and recolor that candidate to the target color.

**Program solution (Python reference):**
```python
def solve_medium_123_select_reflection_match_and_recolor(g):
    out=clone(g)
    comps=connected_components(g)
    # prototype is the component colored 1
    proto_cells=None
    for cells in comps:
        colors={g[r][c] for r,c in cells}
        if colors=={1}:
            proto_cells=cells
            break
    proto=normalize_binary(component_grid(g, proto_cells))
    reflections=[
        proto,
        hflip(proto),
        vflip(proto),
        rot180(proto),
    ]
    for cells in comps:
        colors={g[r][c] for r,c in cells}
        if colors=={2}:
            cand=normalize_binary(component_grid(g, cells))
            if any(cand==normalize_binary(x) for x in reflections):
                for r,c in cells:
                    out[r][c]=8
                break
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 2 0 0
0 1 0 0 0 0 0 0 0 2 0 0
0 1 1 1 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 2 2 0
0 0 0 2 0 0 0 0 2 2 0 0
0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 8 0 0
0 1 0 0 0 0 0 0 0 8 0 0
0 1 1 1 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 2 2 0
0 0 0 2 0 0 0 0 2 2 0 0
0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 2 0 0 0
0 0 0 1 1 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 2 2 0 0
0 0 2 0 2 0 0 0 0 2 0 0 0
0 0 2 2 2 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 2 0 0 0
0 0 0 1 1 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 8 8 0 0
0 0 2 0 2 0 0 0 0 8 0 0 0
0 0 2 2 2 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 2 0 2 0 0
0 1 1 0 0 0 0 0 0 2 0 2 0 0
0 1 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 2 2 2 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 2 0 2 0 0
0 1 1 0 0 0 0 0 0 2 0 2 0 0
0 1 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 2 2 2 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 2 2 2 0 0
0 1 1 0 0 0 0 0 2 0 0 0
0 1 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 2 2 0 0 0 2 2 0 0 0
0 0 2 2 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 2 2 2 0 0
0 1 1 0 0 0 0 0 2 0 0 0
0 1 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 2 2 0 0 0 8 8 0 0 0
0 0 2 2 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 2 2 0 0
0 0 0 1 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 2 2 0
0 0 2 0 2 0 0 0 2 2 0 0
0 0 2 2 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 2 2 0 0
0 0 0 1 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 8 8 0
0 0 2 0 2 0 0 0 8 8 0 0
0 0 2 2 2 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Connect Color Pairs with the Clear Elbow (`medium_124_connect_color_pairs_with_clear_elbows`)

**Difficulty:** medium

**Skills:** path routing, orthogonal geometry, obstacle avoidance


**Scaffold notes:**
- Each color appears exactly twice as a pair of endpoints.
- There are two possible L-shaped connections between those endpoints.
- Use the corner whose two segments stay clear of blockers and other marks.


**Written solution:** For each colored endpoint pair, test the two possible orthogonal elbow corners. Choose the elbow whose horizontal and vertical segments are unobstructed, then draw the full L-shaped path in that color.

**Program solution (Python reference):**
```python
def solve_medium_124_connect_color_pairs_with_clear_elbows(g):
    h,w=dims(g)
    out=clone(g)
    colors=sorted({v for row in g for v in row if v not in (0,5)})
    for color in colors:
        pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        elbows=[(r1,c2),(r2,c1)]
        def clear_segment(a,b):
            (ra,ca),(rb,cb)=a,b
            if ra==rb:
                step=1 if cb>=ca else -1
                for c in range(ca, cb+step, step):
                    if (ra,c) not in pts and g[ra][c]!=0:
                        return False
                return True
            if ca==cb:
                step=1 if rb>=ra else -1
                for r in range(ra, rb+step, step):
                    if (r,ca) not in pts and g[r][ca]!=0:
                        return False
                return True
            return False
        corner=None
        for elbow in elbows:
            if g[elbow[0]][elbow[1]]==0 and clear_segment((r1,c1), elbow) and clear_segment(elbow, (r2,c2)):
                corner=elbow
                break
        if corner is None:
            continue
        er,ec=corner
        for c in range(min(c1,ec), max(c1,ec)+1):
            out[r1][c]=color
        for r in range(min(r1,er), max(r1,er)+1):
            out[r][ec]=color
        for c in range(min(c2,ec), max(c2,ec)+1):
            out[r2][c]=color
        for r in range(min(r2,er), max(r2,er)+1):
            out[r][ec]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 5 5 5 5 5 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 5 0 0
0 0 7 0 0 0 0 5 0 0
0 0 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 3 0 0
0 8 0 5 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 3 0 0
0 8 0 5 0 0 0 0 3 0 0
0 8 0 5 0 0 0 0 3 0 0
0 8 0 5 0 0 0 0 3 0 0
0 8 0 5 0 0 0 0 3 0 0
0 8 0 0 3 3 3 3 3 0 0
0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 6 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 5 5 5 4 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 5 0 0 0 6 0 0 0 4 0 0
0 5 0 0 0 6 0 0 0 4 0 0
0 5 0 0 0 6 0 0 0 4 0 0
0 5 5 5 5 6 5 5 5 4 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 2 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 9 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 9 0
0 0 0 0 0 0 0 0 0 0 9 0
0 0 5 0 2 0 0 0 0 0 9 0
0 0 5 0 2 0 0 0 0 0 9 0
0 0 5 0 2 0 9 9 9 9 9 0
0 0 5 0 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 5 0 0 0 0 0 8 0
0 0 0 0 8 8 8 8 8 8 8 0
0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Recolor Components by Area Rank (`medium_125_recolor_components_by_area_rank`)

**Difficulty:** medium

**Skills:** connected components, area ranking, recoloring


**Scaffold notes:**
- The objects start in the same color, so shape and connectivity matter.
- Rank the three connected components from smallest to largest by cell count.
- Assign a new color based on rank.


**Written solution:** Find the three connected components, sort them by area, recolor the smallest to 2, the middle to 3, and the largest to 4.

**Program solution (Python reference):**
```python
def solve_medium_125_recolor_components_by_area_rank(g):
    comps=connected_components(g)
    comps=sorted(comps, key=lambda cells: len(cells))
    colors=[2,3,4]
    out=zeros(*dims(g))
    for rank,cells in enumerate(comps):
        color=colors[rank]
        for r,c in cells:
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 7 0 0 0 0
0 7 7 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 7 7 0 0 0
0 0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 4 0 0 0 3 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0
0 7 7 7 0 0 7 7 7 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0 0
0 3 3 3 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 7 7 0
0 0 0 0 0 7 0 0 0 0 7 7 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 2 2 0
0 0 0 0 0 4 0 0 0 0 2 2 0
0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Select the Ranked Object and Scale It 2x (`medium_126_select_ranked_object_and_scale2`)

**Difficulty:** medium

**Skills:** legend decoding, area ranking, cropping and scaling


**Scaffold notes:**
- The top-left legend cell tells you which area rank to select.
- Order the connected objects from smallest to largest.
- Crop the selected object and enlarge it by a factor of two in both dimensions.


**Written solution:** Read the requested rank from the legend cell, sort the connected objects by area, pick that ranked object, crop it, and scale the cropped grid by 2×2 replication.

**Program solution (Python reference):**
```python
def solve_medium_126_select_ranked_object_and_scale2(g):
    rank=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    comps=connected_components(gg)
    comps=sorted(comps, key=lambda cells: len(cells))
    target=comps[rank-1]
    return scale2(component_grid(gg, target))
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 6 0 0 0 0
0 0 6 6 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 6 0 6 0 0 6 6 0 0 0
0 6 0 6 0 0 6 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 6
6 6 6 6
6 6 6 6
6 6 6 6
6 6 0 0
6 6 0 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 0 6 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0
0 0 6 6 6 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6 6 6 6
6 6 6 6 6 6
6 6 0 0 0 0
6 6 0 0 0 0
6 6 0 0 0 0
6 6 0 0 0 0
6 6 6 6 6 6
6 6 6 6 6 6
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 6 6 0
0 0 0 0 0 0 6 6 6 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 6 6 0 0
0 0 6 6 0 0
6 6 6 6 6 6
6 6 6 6 6 6
0 0 6 6 0 0
0 0 6 6 0 0
```

**Test 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 6 6 0 0
6 6 6 6 0 0
0 0 6 6 0 0
0 0 6 6 0 0
0 0 6 6 6 6
0 0 6 6 6 6
```


## Build the Rotation Equivalence Matrix (`hard_120_build_rotation_equivalence_matrix`)

**Difficulty:** hard

**Skills:** panel parsing, rotation equivalence, relation matrix construction


**Scaffold notes:**
- The input contains three separate object panels.
- Compare every object to every other object up to rotation only.
- Write a matrix summarizing those pairwise relations.


**Written solution:** Split the input into its three object panels, crop and binarize each object, and build a 3×3 matrix whose diagonal is 8 and whose off-diagonal entries are 2 exactly when the row object matches the column object under rotation.

**Program solution (Python reference):**
```python
def solve_hard_120_build_rotation_equivalence_matrix(g):
    h,w=dims(g)
    panel_w=5
    sep=1
    panels=[]
    c=0
    while c+panel_w<=w:
        panel=[row[c:c+panel_w] for row in g]
        panels.append(panel)
        c+=panel_w+sep
    n=len(panels)
    out=zeros(n,n)
    norms=[normalize_binary(p) for p in panels]
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=8
            else:
                target=norms[j]
                ok=False
                cur=norms[i]
                for t in [lambda x:x, rot90, rot180, rot270]:
                    if normalize_binary(t(cur))==target:
                        ok=True
                        break
                out[i][j]=2 if ok else 0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 0 0 0 0 0 4 4 4 0
0 2 0 0 0 0 3 0 0 0 0 0 0 0 4 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
5 5 0 0 0 0 0 7 7 0 0 0 0 0 8 0 0
0 5 0 0 0 0 0 0 7 0 0 0 0 0 0 8 0
0 5 5 0 0 0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 3 3 3 0 0 0 4 4 0 0
0 2 2 2 0 0 0 0 3 0 0 0 4 4 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 4 input**
```text
2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0
2 0 0 0 0 0 0 3 0 3 0 0 4 4 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 2
0 8 0
2 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 7 7 0 0 0 2 2 2 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 2 0
2 8 0
0 0 8
```


## Decode the Prototype Library with Transform Codes (`hard_121_decode_library_with_transform_codes`)

**Difficulty:** hard

**Skills:** library lookup, code decoding, panel composition, geometric transforms


**Scaffold notes:**
- The top strip is a small library of prototype panels.
- One code row chooses which prototype to use; the second code row chooses how to transform it.
- The output concatenates the decoded transformed panels.


**Written solution:** Parse the three prototype panels, read the index and transform codes below them, apply the requested transform to each chosen prototype, and place the results in a horizontal strip separated by blank columns.

**Program solution (Python reference):**
```python
def solve_hard_121_decode_library_with_transform_codes(g):
    # top 4 rows: 3 prototype panels of width 4 separated by one zero column
    proto_h=4
    proto_w=4
    sep=1
    prototypes=[]
    c=0
    while c+proto_w<=len(g[0]) and len(prototypes)<3:
        prototypes.append([row[c:c+proto_w] for row in g[:proto_h]])
        c+=proto_w+sep
    idx_row=g[proto_h+1]
    tf_row=g[proto_h+2]
    codes=[(idx_row[c], tf_row[c]) for c in range(len(idx_row)) if idx_row[c]!=0]
    panels=[]
    for idx,tf in codes:
        p=prototypes[idx-1]
        panels.append(transform_by_code(p, tf))
    return panelize_row(panels, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 3 3 3 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0 4 4 0
2 0 0 0 0 0 3 0 0 0 0 0 4 0
2 2 2 0 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 3 2 0 0 0 0 0 0 0 0 0 0 0
1 2 3 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 3 3 3
2 0 0 0 0 0 0 4 0 0 0 0 3 0
2 0 0 0 0 4 4 4 0 0 0 0 3 0
2 2 2 0 0 4 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 5 5 0 0 0 0 0 0 0 0 7 0 0
5 5 0 0 0 6 0 6 0 0 0 0 7 0
5 0 0 0 0 6 0 6 0 0 0 0 0 7
0 0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 1 3 2 0 0 0 0 0 0 0 0 0 0
4 1 2 3 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 0 0 0 5 5 0 0 0 0 0 0 0 0 0 0 0
6 0 6 0 0 5 5 0 0 0 0 0 0 7 0 0 6 0 6
6 0 6 0 0 5 0 0 0 0 0 0 7 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 6 6 6
```

**Train 3 input**
```text
2 2 0 0 0 0 8 0 0 0 0 0 0 0
2 2 0 0 0 8 8 8 0 0 4 4 4 0
2 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 2 1 0 0 0 0 0 0 0 0 0 0 0
1 4 2 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 2 2 2
4 4 4 0 0 0 8 0 0 0 0 0 2 2
0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0
```

**Train 4 input**
```text
3 3 0 0 0 0 6 6 0 0 0 0 0 0
0 3 3 0 0 0 0 6 0 0 2 0 2 0
0 0 3 0 0 0 0 6 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 2 3 0 0 0 0 0 0 0 0 0 0
3 2 1 4 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 3 3 0 0 0 0 3 0 0 6 6 0 0 2 2 2 0
0 3 3 0 0 0 0 3 3 0 0 0 6 0 0 2 0 2 0
0 3 0 0 0 0 3 3 0 0 0 0 6 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
7 0 0 0 0 0 4 4 0 0 0 2 0 0
7 0 0 0 0 4 4 0 0 0 2 2 2 0
7 7 7 0 0 4 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 1 0 0 0 0 0 0 0 0 0 0 0
2 1 4 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 4 4 0 0 0 2 0 0 0 0 0 0 0
0 0 4 4 0 2 2 2 0 0 7 7 7 0
0 0 0 4 0 0 2 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0
```


## Overlay Directed Rays into a Count Map (`hard_122_overlay_rays_until_block_count_map`)

**Difficulty:** hard

**Skills:** ray casting, direction decoding, overlap counting


**Scaffold notes:**
- Emitter colors encode directions.
- Each emitter sends a straight ray until a blocker or the grid edge stops it.
- The output records how many rays cover each cell.


**Written solution:** Interpret colors 1–4 as up, right, down, and left emitters. For every emitter, trace its ray cell by cell until a blocker is reached and increment a count map on every traversed cell.

**Program solution (Python reference):**
```python
def solve_hard_122_overlay_rays_until_block_count_map(g):
    h,w=dims(g)
    out=zeros(h,w)
    dirs={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in dirs:
                dr,dc=dirs[v]
                rr,cc=r,c
                while 0<=rr<h and 0<=cc<w and g[rr][cc]!=5:
                    out[rr][cc]+=1
                    rr+=dr
                    cc+=dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 5 0 4 0
0 0 0 0 0 0 0 0
1 0 0 5 0 0 0 3
0 0 0 0 0 5 0 0
0 4 0 0 2 0 0 0
0 0 0 5 0 0 1 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 0 0 0 0 0 1 0
1 1 1 1 0 1 2 0
1 0 0 0 0 0 1 0
1 0 0 0 0 0 1 1
0 0 0 0 0 0 1 1
1 1 0 0 1 1 2 2
0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 1
```

**Train 2 input**
```text
0 0 1 0 0 0 0 0 0
0 5 0 0 2 0 5 0 0
0 0 0 0 0 0 0 0 4
0 0 5 0 0 0 0 0 0
3 0 0 0 5 0 0 0 0
0 0 0 2 0 0 0 5 0
0 4 0 0 0 0 1 0 0
```

**Train 2 output**
```text
0 0 1 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0
1 1 1 1 1 1 2 1 1
0 0 0 0 0 0 1 0 0
1 0 0 0 0 0 1 0 0
1 0 0 1 1 1 2 0 0
2 1 0 0 0 0 1 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 5 0 0 4 0 0
0 0 0 0 0 0 0 0 3
1 0 0 0 5 0 0 0 0
0 0 5 0 0 0 2 0 0
0 4 0 0 0 5 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 3 0 0 5 0 0
```

**Train 3 output**
```text
1 0 0 0 0 0 0 0 0
1 1 1 0 1 1 1 0 0
1 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 1
0 0 0 0 1 0 1 1 2
1 1 0 0 1 0 0 0 1
0 0 0 0 1 0 0 0 1
0 0 0 1 0 0 0 0 1
```

**Train 4 input**
```text
0 0 0 0 4 0 0 0
0 5 0 0 0 0 5 0
1 0 0 2 0 0 0 0
0 0 0 0 0 5 0 3
0 0 5 0 0 0 0 0
0 2 0 0 1 0 4 0
0 0 0 5 0 0 0 0
3 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 1 1 1 2 0 0 0
1 0 0 0 1 0 0 0
1 0 0 1 2 1 1 1
0 0 0 0 1 0 0 1
0 0 0 0 1 0 0 1
1 2 2 2 3 2 2 2
0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 1
```

**Test 1 input**
```text
0 2 0 0 0 0 4 0 0
0 0 0 5 0 0 0 0 0
1 0 0 0 0 5 0 0 3
0 0 5 0 2 0 0 0 0
0 4 0 0 0 0 5 0 0
0 0 0 1 0 0 0 0 0
3 0 0 0 0 5 0 4 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 2 2 2 2 2 1 1
1 0 0 0 0 0 0 0 0
1 0 0 1 0 0 0 0 1
0 0 0 1 1 1 1 1 2
1 1 0 1 0 0 0 0 1
0 0 0 1 0 0 0 0 1
1 0 0 0 0 0 1 1 1
1 0 0 0 0 0 0 0 1
```


## Fill Chambers by Seed Priority Legend (`hard_123_fill_chambers_by_seed_priority_legend`)

**Difficulty:** hard

**Skills:** legend priority, chamber analysis, seed-based filling


**Scaffold notes:**
- The first row gives a priority order over colors.
- Each wall-separated chamber may contain one or more seed colors from that legend.
- Fill every empty cell in a chamber with the highest-priority seed present in that chamber.


**Written solution:** Read the priority order from the legend row, segment the wall-separated chambers below it, detect which legend colors occur in each chamber, and fill the chamber's zero cells with the highest-priority present seed color.

**Program solution (Python reference):**
```python
def solve_hard_123_fill_chambers_by_seed_priority_legend(g):
    legend=[v for v in g[0] if v not in (0,5)]
    priority={color:i for i,color in enumerate(legend)}
    out=clone(g)
    regions=find_regions_without_walls(g, wall=5, skip_rows=1)
    for cells in regions:
        present=sorted({g[r][c] for r,c in cells if g[r][c] in priority}, key=lambda x: priority[x])
        if not present:
            continue
        fill=present[0]
        for r,c in cells:
            if out[r][c]==0:
                out[r][c]=fill
    return out
```

**Train 1 input**
```text
2 4 1 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
5 2 0 0 5 1 0 4 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
5 1 0 4 5 0 0 0 5
5 0 0 0 5 2 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
2 4 1 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
5 2 2 2 5 1 4 4 5
5 2 2 2 5 4 4 4 5
5 5 5 5 5 5 5 5 5
5 1 4 4 5 2 2 2 5
5 4 4 4 5 2 2 2 5
5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
3 1 4 2 0 0 0 0
5 5 5 5 5 5 5 5
5 0 3 0 5 2 0 5
5 1 0 0 5 0 0 5
5 5 5 5 5 5 5 5
5 4 0 0 5 0 1 5
5 0 0 0 5 3 0 5
5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
3 1 4 2 0 0 0 0
5 5 5 5 5 5 5 5
5 3 3 3 5 2 2 5
5 1 3 3 5 2 2 5
5 5 5 5 5 5 5 5
5 4 4 4 5 3 1 5
5 4 4 4 5 3 3 5
5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
4 2 6 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
5 0 0 4 5 2 0 0 6 5
5 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
5 6 0 0 5 0 4 0 0 5
5 0 0 0 5 2 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
4 2 6 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
5 4 4 4 5 2 2 2 6 5
5 4 4 4 5 2 2 2 2 5
5 5 5 5 5 5 5 5 5 5
5 6 6 6 5 4 4 4 4 5
5 6 6 6 5 2 4 4 4 5
5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
1 8 3 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
5 0 8 0 5 3 0 0 5
5 1 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
5 0 0 0 5 8 0 1 5
5 3 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
1 8 3 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
5 1 8 1 5 3 3 3 5
5 1 1 1 5 3 3 3 5
5 5 5 5 5 5 5 5 5
5 3 3 3 5 8 1 1 5
5 3 3 3 5 1 1 1 5
5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
7 2 9 4 0 0 0 0
5 5 5 5 5 5 5 5
5 0 7 0 5 2 0 5
5 9 0 0 5 0 4 5
5 5 5 5 5 5 5 5
5 4 0 0 5 0 0 5
5 0 0 0 5 7 0 5
5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
7 2 9 4 0 0 0 0
5 5 5 5 5 5 5 5
5 7 7 7 5 2 2 5
5 9 7 7 5 2 4 5
5 5 5 5 5 5 5 5
5 4 4 4 5 7 7 5
5 4 4 4 5 7 7 5
5 5 5 5 5 5 5 5
```


## Build the Pairwise XOR Gallery (`hard_124_build_pairwise_xor_gallery`)

**Difficulty:** hard

**Skills:** panel parsing, boolean shape operations, gallery assembly


**Scaffold notes:**
- Treat each input panel as a binary mask.
- For every ordered pair of panels, compute the XOR of their occupied cells.
- Arrange those pairwise results into a square gallery.


**Written solution:** Split the input into three panels, compare every ordered pair cellwise as binary masks, keep cells that belong to exactly one of the two shapes, and place those XOR panels into a 3×3 gallery separated by blank lines.

**Program solution (Python reference):**
```python
def solve_hard_124_build_pairwise_xor_gallery(g):
    panel_h=4
    panel_w=4
    sep=1
    panels=[]
    c=0
    while c+panel_w<=len(g[0]):
        panels.append([row[c:c+panel_w] for row in g[:panel_h]])
        c+=panel_w+sep
    gallery=[]
    for a in panels:
        row=[]
        for b in panels:
            row.append(xor_panels(a,b,color=7))
        gallery.append(row)
    return gallery_grid(gallery, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 6 6 6 0 0 0 0 0 0
6 0 0 0 0 0 6 0 0 0 0 6 6 0
6 0 0 0 0 0 6 0 0 0 0 0 6 0
6 6 6 0 0 0 0 0 0 0 0 0 6 6
```

**Train 1 output**
```text
0 0 0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 7 7 7 0
0 0 0 0 0 7 7 0 0 0 7 0 7 0
0 0 0 0 0 7 7 7 0 0 7 7 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 7 7 7 0
7 7 0 0 0 0 0 0 0 0 0 0 7 0
7 7 0 0 0 0 0 0 0 0 0 7 7 0
7 7 7 0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0
7 7 7 0 0 0 0 7 0 0 0 0 0 0
7 0 7 0 0 0 7 7 0 0 0 0 0 0
7 7 0 7 0 0 0 7 7 0 0 0 0 0
```

**Train 2 input**
```text
0 6 6 0 0 0 0 0 0 0 0 6 0 0
6 6 0 0 0 6 0 6 0 0 0 0 6 0
6 0 0 0 0 6 0 6 0 0 0 0 0 6
0 0 0 0 0 6 6 6 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 7 7 0 0 0 0 7 0
0 0 0 0 0 0 7 7 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 0 7 0 0 7
0 0 0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 7 0 0
0 7 7 0 0 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 0 0 7 0 7 7
7 7 7 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0 0
7 7 7 0 0 7 0 0 0 0 0 0 0 0
7 0 0 7 0 7 0 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0
```

**Train 3 input**
```text
6 6 0 0 0 0 6 0 0 0 0 0 0 0
6 6 0 0 0 6 6 6 0 0 6 6 6 0
6 0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 7 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 7 0 0 0 0 7 0
0 0 0 0 0 7 7 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
6 6 0 0 0 0 6 6 0 0 0 0 0 0
0 6 6 0 0 0 0 6 0 0 6 0 6 0
0 0 6 0 0 0 0 6 6 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 6 6 6 0
```

**Train 4 output**
```text
0 0 0 0 0 7 0 7 0 0 7 7 0 0
0 0 0 0 0 0 7 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 7 7 0
0 7 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 7 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 7 7 0 0 0 0 0 0
7 7 0 0 0 7 0 0 0 0 0 0 0 0
7 0 0 0 0 7 0 0 7 0 0 0 0 0
7 7 7 0 0 7 7 7 0 0 0 0 0 0
```

**Test 1 input**
```text
6 0 0 0 0 0 6 6 0 0 0 6 0 0
6 0 0 0 0 6 6 0 0 0 6 6 6 0
6 6 6 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 7 7 7 0 0 7 7 0 0
0 0 0 0 0 0 7 0 0 0 0 7 7 0
0 0 0 0 0 0 7 7 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0 0 0 7 0
0 7 7 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 7 0 0 0 0 0 0
0 7 7 0 0 0 0 7 0 0 0 0 0 0
7 0 7 0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Fill Chambers by Nearest Seed (`hard_125_fill_chambers_by_nearest_seed`)

**Difficulty:** hard

**Skills:** distance transform, wall segmentation, nearest-neighbor filling


**Scaffold notes:**
- Walls partition the grid into independent chambers.
- Within a chamber, every empty cell should inherit the color of its nearest seed.
- When distances tie, use the smaller seed color.


**Written solution:** For each wall-separated chamber, collect its seed cells and fill every zero cell with the color of the chamber seed having minimum Manhattan distance; break ties by smaller seed color.

**Program solution (Python reference):**
```python
def solve_hard_125_fill_chambers_by_nearest_seed(g):
    out=clone(g)
    regions=find_regions_without_walls(g, wall=5)
    for cells in regions:
        seeds=[(r,c,g[r][c]) for r,c in cells if g[r][c]!=0]
        if not seeds:
            continue
        for r,c in cells:
            if g[r][c]==0:
                best=min(seeds, key=lambda s: (abs(r-s[0])+abs(c-s[1]), s[2], s[0], s[1]))
                out[r][c]=best[2]
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5
5 1 0 0 5 0 0 2 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
5 0 3 0 5 4 0 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5
5 1 1 1 5 2 2 2 5
5 1 1 1 5 2 2 2 5
5 1 1 1 5 2 2 2 5
5 5 5 5 5 5 5 5 5
5 3 3 3 5 4 4 4 5
5 3 3 3 5 4 4 4 5
5 3 3 3 5 4 4 4 5
5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5
5 1 0 0 5 0 2 5
5 0 0 0 5 0 0 5
5 0 0 0 5 0 0 5
5 5 5 5 5 5 5 5
5 3 0 4 5 0 0 5
5 0 0 0 5 0 0 5
5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5
5 1 1 1 5 2 2 5
5 1 1 1 5 2 2 5
5 1 1 1 5 2 2 5
5 5 5 5 5 5 5 5
5 3 3 4 5 0 0 5
5 3 3 4 5 0 0 5
5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5 5 5
5 1 0 0 5 0 2 0 0 5
5 0 0 0 5 0 0 0 0 5
5 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
5 0 3 0 5 4 0 0 0 5
5 0 0 0 5 0 0 0 0 5
5 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5
5 1 1 1 5 2 2 2 2 5
5 1 1 1 5 2 2 2 2 5
5 1 1 1 5 2 2 2 2 5
5 5 5 5 5 5 5 5 5 5
5 3 3 3 5 4 4 4 4 5
5 3 3 3 5 4 4 4 4 5
5 3 3 3 5 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
5 5 5 5 5 5 5 5 5
5 0 1 0 5 0 2 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
5 0 3 0 5 0 4 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
5 5 5 5 5 5 5 5 5
5 1 1 1 5 2 2 2 5
5 1 1 1 5 2 2 2 5
5 1 1 1 5 2 2 2 5
5 5 5 5 5 5 5 5 5
5 3 3 3 5 4 4 4 5
5 3 3 3 5 4 4 4 5
5 3 3 3 5 4 4 4 5
5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
5 5 5 5 5 5 5 5 5 5
5 1 0 0 0 5 0 0 2 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5
5 0 3 0 0 5 4 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
5 5 5 5 5 5 5 5 5 5
5 1 1 1 1 5 2 2 2 5
5 1 1 1 1 5 2 2 2 5
5 1 1 1 1 5 2 2 2 5
5 5 5 5 5 5 5 5 5 5
5 3 3 3 3 5 4 4 4 5
5 3 3 3 3 5 4 4 4 5
5 3 3 3 3 5 4 4 4 5
5 5 5 5 5 5 5 5 5 5
```


## Build a Centered Transformed Stamp Count Map (`hard_126_centered_transformed_stamp_count_map`)

**Difficulty:** hard

**Skills:** prototype parsing, centered stamping, transform decoding, overlap counting


**Scaffold notes:**
- The small prototype in the corner is the stamp.
- Each marker elsewhere requests a transformed copy of that stamp centered on the marker.
- The output counts how many transformed stamps cover each cell.


**Written solution:** Read the 3×3 prototype, interpret marker colors as transform codes, stamp each transformed prototype centered on its marker, and output the resulting overlap count map.

**Program solution (Python reference):**
```python
def solve_hard_126_centered_transformed_stamp_count_map(g):
    proto=[row[:3] for row in g[:3]]
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in (1,2,3,4) and not (r<3 and c<3):
                obj=transform_by_code(proto, v)
                oh,ow=dims(obj)
                top=r-oh//2
                left=c-ow//2
                count_stamp(out, obj, top, left, transparent=0)
    return out
```

**Train 1 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 1 1 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 1 1 4 1 1 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 1 1 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 6 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 2 2 1 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
6 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 2 1 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 6 6 0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 2 1 0 0 0 0 0
0 0 0 0 0 1 1 0 1 1 0 0 0 0
0 0 0 0 0 2 0 0 0 1 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


