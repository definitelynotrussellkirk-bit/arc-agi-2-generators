# ARC Puzzle Bank — Eleventh 21 Puzzles
This eleventh bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`71`–`77`) so it follows directly after the tenth bundle.
This volume leans into diagonal fills, local expansions, object cropping, frame-local row/column crosses, border-cast rays, library lookup transforms, boolean shape logic, hole-based selection, chamber fills, relation matrices, rank-based packing, and cross-product galleries.
It also introduces a few reusable solver primitives that fit your pipeline well: `diag_span_fill`, `border_inward_ray`, `panel_library_decode`, and `intersection_gallery`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_eleventh_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_eleventh_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_eleventh_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_71_fill_diagonal_between_matching_endpoints` — **Fill Diagonal Between Matching Endpoints**
- `easy_72_expand_singletons_to_plus` — **Expand Singletons to Plus Shapes**
- `easy_73_crop_nonzero_bounding_box` — **Crop the Nonzero Bounding Box**
- `easy_74_compact_nonzero_rows_up` — **Compact Nonzero Rows Upward**
- `easy_75_fill_hollow_rectangles` — **Fill Hollow Rectangles**
- `easy_76_cast_vertical_rays_downward` — **Cast Vertical Rays Downward**
- `easy_77_mirror_across_main_diagonal` — **Mirror Across the Main Diagonal**

### Medium (7)
- `medium_71_marker_selects_component_to_crop` — **Marker Selects the Matching Component**
- `medium_72_frame_gate_cross_fill` — **Fill Row-and-Column Crosses Inside Frames**
- `medium_73_rotate_source_by_control_color` — **Rotate the Source by the Control Color**
- `medium_74_scale_smallest_component_and_recolor` — **Scale the Smallest Component and Recolor It**
- `medium_75_quadrant_majority_summary` — **Quadrant Majority Summary**
- `medium_76_recover_rectangles_from_three_corners` — **Recover Rectangles from Three Corners**
- `medium_77_border_rays_until_block` — **Cast Rays Inward from the Border Until a Block**

### Hard (7)
- `hard_71_library_lookup_transform_gallery` — **Library Lookup Transform Gallery**
- `hard_72_boolean_operation_by_marker` — **Boolean Operation by Marker**
- `hard_73_choose_most_holes_scale2_recolor` — **Choose the Most-Holed Component, Scale, and Recolor**
- `hard_74_fill_keyed_chambers_inside_frames` — **Fill the Keyed Chambers Inside Frames**
- `hard_75_rotational_equivalence_matrix` — **Rotational Equivalence Matrix**
- `hard_76_rank_components_by_area_and_stack` — **Rank Components by Area and Stack Them**
- `hard_77_cross_product_intersection_gallery` — **Cross-Product Intersection Gallery**

## Fill Diagonal Between Matching Endpoints (`easy_71_fill_diagonal_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** diagonal spans, same-color endpoint pairing, same-size transform

**Scaffold notes:**
- Group nonzero cells by color.
- Each color appears exactly twice.
- Walk from one endpoint to the other with a unit diagonal step and fill the path.

**Written solution:** For each color, find its two endpoints. If they lie on a diagonal, fill every cell along that diagonal segment with the same color.

**Program solution (Python reference):**
```python
def solve_easy_71_fill_diagonal_between_matching_endpoints(g):
    out=clone(g)
    h,w=dims(g)
    pos=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        dr=r2-r1
        dc=c2-c1
        if abs(dr)!=abs(dc):
            continue
        sr=1 if dr>0 else -1
        sc=1 if dc>0 else -1
        for k in range(abs(dr)+1):
            out[r1+sr*k][c1+sc*k]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 2 0 0 0 7 0
0 0 0 2 0 7 0 0
0 0 0 0 7 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 8 0 3 0 0
0 0 0 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 6 0 0 4 0 0
0 0 0 6 0 0 4 0 0 0
0 0 6 0 0 4 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0
0 0 0 9 0 0 1 0 0 0 0
0 0 0 0 9 0 0 1 0 0 0
0 0 0 0 0 9 0 0 1 0 0
0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Expand Singletons to Plus Shapes (`easy_72_expand_singletons_to_plus`)

**Difficulty:** easy

**Skills:** local expansion, single-cell detection, same-size transform

**Scaffold notes:**
- Look for nonzero cells whose four orthogonal neighbors are blank.
- Do not remove the original center.
- Add one same-colored arm in each cardinal direction.

**Written solution:** Every isolated colored cell grows into a plus: keep the center and paint its four cardinal neighbors with the same color.

**Program solution (Python reference):**
```python
def solve_easy_72_expand_singletons_to_plus(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v==0:
                continue
            nbrs=[g[r-1][c],g[r+1][c],g[r][c-1],g[r][c+1]]
            if all(x==0 for x in nbrs):
                out[r-1][c]=v
                out[r+1][c]=v
                out[r][c-1]=v
                out[r][c+1]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 7 0 0
0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 3 3 3 0 0 0
0 0 0 3 0 6 0 0
0 0 0 0 6 6 6 0
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 1 0 4 0 0
0 0 0 0 1 1 1 0 0 0
0 0 8 0 0 1 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 9 0 0 5 5 5 0
0 0 0 9 9 9 0 0 5 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 6 7 7 7
0 0 0 0 0 6 6 6 7 0
0 0 2 0 0 0 6 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Crop the Nonzero Bounding Box (`easy_73_crop_nonzero_bounding_box`)

**Difficulty:** easy

**Skills:** bounding boxes, size-changing output, object extraction

**Scaffold notes:**
- Find all nonzero cells.
- Take their minimum and maximum row and column.
- Return exactly that bounding box.

**Written solution:** Ignore the surrounding blank space. Crop the grid down to the smallest rectangle that contains every nonzero cell.

**Program solution (Python reference):**
```python
def solve_easy_73_crop_nonzero_bounding_box(g):
    return crop_nonzero(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 3 3 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0
2 3 3
0 3 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 6 0
6 0 0 6
6 6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0
8 8
0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 5 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 0
0 4 5
0 5 5
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 0 7
0 7 0
7 0 0
```

## Compact Nonzero Rows Upward (`easy_74_compact_nonzero_rows_up`)

**Difficulty:** easy

**Skills:** row filtering, order preservation, same-size transform

**Scaffold notes:**
- Decide which rows are entirely blank.
- Preserve the content and order of the nonblank rows.
- Pack them at the top and pad the bottom with zero rows.

**Written solution:** Keep only the rows that contain at least one colored cell, preserve their order, and slide them to the top. Fill the remaining rows with zeros.

**Program solution (Python reference):**
```python
def solve_easy_74_compact_nonzero_rows_up(g):
    h,w=dims(g)
    rows=[row[:] for row in g if any(v!=0 for v in row)]
    while len(rows)<h:
        rows.append([0]*w)
    return rows
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0
```

**Train 1 output**
```text
0 2 2 0 0 0 0 0
0 0 0 5 5 5 0 0
7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0
```

**Train 2 output**
```text
3 3 0 0 0 0 0 0 0
0 0 6 0 6 0 6 0 0
0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
1 0 1 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 0 3 0 3 0
```

**Train 4 output**
```text
1 0 1 0 0 0 0
0 0 0 2 2 0 0
0 3 0 3 0 3 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0
```

**Test 1 output**
```text
0 0 5 5 0 0 0 0
2 0 2 0 2 0 0 0
0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Fill Hollow Rectangles (`easy_75_fill_hollow_rectangles`)

**Difficulty:** easy

**Skills:** rectangle detection, interior filling, same-size transform

**Scaffold notes:**
- Treat each color component as a rectangle border.
- Use its bounding box.
- Fill every cell inside the box with the rectangle color.

**Written solution:** Each colored object is a hollow axis-aligned rectangle. Fill the entire interior so every rectangle becomes solid.

**Program solution (Python reference):**
```python
def solve_easy_75_fill_hollow_rectangles(g):
    out=clone(g)
    comps=connected_components(g)
    for comp in comps:
        color=comp['color']
        r0,c0,r1,c1=comp['bbox']
        ok=True
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                border=(r in (r0,r1) or c in (c0,c1))
                if border and g[r][c]!=color:
                    ok=False
                if not border and g[r][c]!=0:
                    ok=False
        if ok:
            fill_rect(out, r0,c0,r1,c1, color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 0 0 2 0 7 7 7 0
0 2 0 0 2 0 7 0 7 0
0 2 2 2 2 0 7 0 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 7 7 7 0
0 2 2 2 2 0 7 7 7 0
0 2 2 2 2 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0
0 0 3 0 0 0 0 3 0 8 8 0
0 0 3 0 0 0 0 3 0 8 8 0
0 0 3 3 3 3 3 3 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0
0 0 3 3 3 3 3 3 0 8 8 0
0 0 3 3 3 3 3 3 0 8 8 0
0 0 3 3 3 3 3 3 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
4 4 4 4 0 0 0 0 0
4 0 0 4 0 0 0 0 0
4 0 0 4 0 6 6 6 6
4 4 4 4 0 6 0 0 6
0 0 0 0 0 6 0 0 6
0 0 0 0 0 6 0 0 6
0 0 0 0 0 6 6 6 6
```

**Train 3 output**
```text
4 4 4 4 0 0 0 0 0
4 4 4 4 0 0 0 0 0
4 4 4 4 0 6 6 6 6
4 4 4 4 0 6 6 6 6
0 0 0 0 0 6 6 6 6
0 0 0 0 0 6 6 6 6
0 0 0 0 0 6 6 6 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0
0 9 0 0 0 9 0 5 5 5 0
0 9 0 0 0 9 0 5 0 5 0
0 9 9 9 9 9 0 5 0 5 0
0 0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0
0 9 9 9 9 9 0 5 5 5 0
0 9 9 9 9 9 0 5 5 5 0
0 9 9 9 9 9 0 5 5 5 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 2 2 2
0 0 7 0 0 0 7 0 2 0 2
0 0 7 7 7 7 7 0 2 0 2
0 0 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0
0 0 7 7 7 7 7 0 2 2 2
0 0 7 7 7 7 7 0 2 2 2
0 0 7 7 7 7 7 0 2 2 2
0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
```

## Cast Vertical Rays Downward (`easy_76_cast_vertical_rays_downward`)

**Difficulty:** easy

**Skills:** column propagation, same-color painting, same-size transform

**Scaffold notes:**
- Keep each seed cell.
- Extend its color only in the same column.
- Continue to the bottom of the grid.

**Written solution:** Every colored seed paints straight downward in its own column, all the way to the bottom edge.

**Program solution (Python reference):**
```python
def solve_easy_76_cast_vertical_rays_downward(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for rr in range(r,h):
                    out[rr][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 7 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 7 0 0
0 2 0 0 0 7 0 0
0 2 0 0 0 7 0 0
0 2 0 0 0 7 0 0
0 2 0 0 0 7 0 0
0 2 0 0 0 7 0 0
0 2 0 0 0 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 3 0 0 9 0 0 0
0 0 3 0 0 9 0 0 0
0 0 3 0 0 9 0 6 0
0 0 3 0 0 9 0 6 0
0 0 3 0 0 9 0 6 0
0 0 3 0 0 9 0 6 0
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 8 0 0 0 0 0
4 0 0 0 8 0 0 0 0 0
4 0 0 0 8 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 1
0 0 0 5 0 0 1
0 0 0 5 0 0 1
0 0 0 5 0 0 1
0 0 0 5 0 0 1
```

**Test 1 input**
```text
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 0 0 7 0
0 0 0 0 0 6 0 0 7 0
0 0 2 0 0 6 0 0 7 0
0 0 2 0 0 6 0 0 7 0
0 0 2 0 0 6 0 0 7 0
0 0 2 0 0 6 0 0 7 0
0 0 2 0 0 6 0 0 7 0
```

## Mirror Across the Main Diagonal (`easy_77_mirror_across_main_diagonal`)

**Difficulty:** easy

**Skills:** diagonal symmetry, square-grid transform, same-size output

**Scaffold notes:**
- The main diagonal stays fixed.
- A cell at row r, column c is copied to row c, column r.
- Preserve the original colors.

**Written solution:** Copy every nonzero cell to its transposed position across the main diagonal, keeping the original cells as well.

**Program solution (Python reference):**
```python
def solve_easy_77_mirror_across_main_diagonal(g):
    n=len(g)
    out=clone(g)
    for r in range(n):
        for c in range(n):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 2 0 0 8
0 0 0 0 7 0
0 0 0 0 0 3
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 2 0 0 8
0 0 0 0 7 0
2 0 0 0 0 3
0 0 0 0 0 0
0 7 0 0 0 0
8 0 3 0 0 0
```

**Train 2 input**
```text
0 0 0 4 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 9
0 0 0 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 4 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 9
4 0 0 2 0 0 0
0 0 0 0 0 0 0
0 6 0 0 0 0 0
0 0 9 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 5
0 0 1 0 0
0 0 0 0 7
0 0 0 0 0
0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 5
0 0 1 0 0
0 1 0 0 7
0 0 0 0 0
5 0 7 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 6
0 0 0 0 0 8 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 6
0 0 0 0 0 8 0 0
0 0 0 0 4 0 0 0
0 0 0 4 0 0 0 0
0 0 8 0 0 0 0 0
3 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 2 0
0 0 0 0 0 0 9
0 0 0 0 7 0 0
0 0 0 0 0 0 5
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 2 0
0 0 0 0 0 0 9
0 0 0 0 7 0 0
0 0 0 0 0 0 5
0 0 7 0 0 0 0
2 0 0 0 0 0 0
0 9 0 5 0 0 0
```

## Marker Selects the Matching Component (`medium_71_marker_selects_component_to_crop`)

**Difficulty:** medium

**Skills:** component selection, color matching, size-changing extraction

**Scaffold notes:**
- Group connected components by color.
- One color appears as a singleton marker and as one larger object.
- Crop and return the larger object of that color.

**Written solution:** Find the singleton marker. Its color tells you which larger component to keep. Return the cropped larger component of that same color.

**Program solution (Python reference):**
```python
def solve_medium_71_marker_selects_component_to_crop(g):
    comps=connected_components(g)
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp['color']].append(comp)
    target=None
    for color, arr in by_color.items():
        single=[c for c in arr if c['area']==1]
        big=[c for c in arr if c['area']>1]
        if len(single)==1 and len(big)==1:
            target=big[0]
            break
    if target is None:
        return [[0]]
    return crop_bbox(g, target['bbox'])
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 2 2 2 0 0 0
0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 0 0
4 0 0
4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 6 0 6 0 0 0 3 0 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 6
6 0 6
6 6 6
```

**Train 3 input**
```text
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 2 2 0 0 7 0
0 0 0 0 0 0 2 0 0 0 0
0 9 0 0 0 0 2 2 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 0
0 2 0
0 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 4 0 4 0 0
0 0 3 3 0 0 0 0 0 4 0 4 0 0
0 3 3 0 0 0 0 0 0 4 4 4 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8
8 8
8 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 5 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 5
0 5 0
0 5 0
```

## Fill Row-and-Column Crosses Inside Frames (`medium_72_frame_gate_cross_fill`)

**Difficulty:** medium

**Skills:** frame-local reasoning, marker interpretation, same-size transform

**Scaffold notes:**
- Treat each rectangle border independently.
- The top marker chooses a column inside the frame.
- The left marker chooses a row; fill their full cross inside the frame.

**Written solution:** Each framed region contains one colored marker just under the top border and one matching marker just inside the left border. Fill the corresponding interior column and interior row with that color.

**Program solution (Python reference):**
```python
def solve_medium_72_frame_gate_cross_fill(g):
    out=clone(g)
    frames=[comp for comp in connected_components(g, colors=[9])]
    for frame in frames:
        r0,c0,r1,c1=frame['bbox']
        # verify rectangle border
        ok=True
        for c in range(c0,c1+1):
            if g[r0][c]!=9 or g[r1][c]!=9:
                ok=False
        for r in range(r0,r1+1):
            if g[r][c0]!=9 or g[r][c1]!=9:
                ok=False
        if not ok or r1-r0<2 or c1-c0<2:
            continue
        top_marks=[(c,g[r0+1][c]) for c in range(c0+1,c1) if g[r0+1][c] not in (0,9)]
        left_marks=[(r,g[r][c0+1]) for r in range(r0+1,r1) if g[r][c0+1] not in (0,9)]
        for tc,color in top_marks:
            for lr,color2 in left_marks:
                if color==color2:
                    for c in range(c0+1,c1):
                        out[lr][c]=color
                    for r in range(r0+1,r1):
                        out[r][tc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 0 0 0 0
0 9 0 0 0 2 9 0 9 9 9 9 0
0 9 0 0 0 0 9 0 9 0 7 9 0
0 9 2 0 0 0 9 0 9 0 0 9 0
0 9 0 0 0 0 9 0 9 0 0 9 0
0 9 9 9 9 9 9 0 9 7 0 9 0
0 0 0 0 0 0 0 0 9 0 0 9 0
0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 0 0 0 0
0 9 0 0 0 2 9 0 9 9 9 9 0
0 9 0 0 0 2 9 0 9 0 7 9 0
0 9 2 2 2 2 9 0 9 0 7 9 0
0 9 0 0 0 2 9 0 9 0 7 9 0
0 9 9 9 9 9 9 0 9 7 7 9 0
0 0 0 0 0 0 0 0 9 0 7 9 0
0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 0
0 0 9 0 0 0 0 4 9 0 0 0
0 0 9 0 0 0 0 0 9 0 0 0
0 0 9 0 0 0 0 0 9 0 0 0
0 0 9 4 0 0 0 0 9 0 0 0
0 0 9 0 0 0 0 0 9 0 0 0
0 0 9 9 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 0
0 0 9 0 0 0 0 4 9 0 0 0
0 0 9 0 0 0 0 4 9 0 0 0
0 0 9 0 0 0 0 4 9 0 0 0
0 0 9 4 4 4 4 4 9 0 0 0
0 0 9 0 0 0 0 4 9 0 0 0
0 0 9 9 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0
0 9 0 0 0 0 0 8 9 0 0 0 0 0 0
0 9 8 0 0 0 0 0 9 0 0 0 0 0 0
0 9 0 0 0 0 0 0 9 0 9 9 9 9 0
0 9 0 0 0 0 0 0 9 0 9 0 3 9 0
0 9 9 9 9 9 9 9 9 0 9 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 3 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0
0 9 0 0 0 0 0 8 9 0 0 0 0 0 0
0 9 8 8 8 8 8 8 9 0 0 0 0 0 0
0 9 0 0 0 0 0 8 9 0 9 9 9 9 0
0 9 0 0 0 0 0 8 9 0 9 0 3 9 0
0 9 9 9 9 9 9 9 9 0 9 0 3 9 0
0 0 0 0 0 0 0 0 0 0 9 3 3 9 0
0 0 0 0 0 0 0 0 0 0 9 0 3 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0
0 9 0 0 6 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0 0
0 9 6 0 0 0 0 9 0 0 0
0 9 9 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0
0 9 0 0 6 0 0 9 0 0 0
0 9 0 0 6 0 0 9 0 0 0
0 9 0 0 6 0 0 9 0 0 0
0 9 0 0 6 0 0 9 0 0 0
0 9 6 6 6 6 6 9 0 0 0
0 9 9 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0
0 9 0 0 0 0 5 0 9 0 0 0 0 0
0 9 0 0 0 0 0 0 9 0 9 9 9 9
0 9 0 0 0 0 0 0 9 0 9 0 2 9
0 9 5 0 0 0 0 0 9 0 9 0 0 9
0 9 0 0 0 0 0 0 9 0 9 2 0 9
0 9 9 9 9 9 9 9 9 0 9 0 0 9
0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0
0 9 0 0 0 0 5 0 9 0 0 0 0 0
0 9 0 0 0 0 5 0 9 0 9 9 9 9
0 9 0 0 0 0 5 0 9 0 9 0 2 9
0 9 5 5 5 5 5 5 9 0 9 0 2 9
0 9 0 0 0 0 5 0 9 0 9 2 2 9
0 9 9 9 9 9 9 9 9 0 9 0 2 9
0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Rotate the Source by the Control Color (`medium_73_rotate_source_by_control_color`)

**Difficulty:** medium

**Skills:** control code, rotation, size-changing extraction

**Scaffold notes:**
- Ignore the singleton control once you read it.
- Crop the larger object.
- Apply the rotation indicated by the control color.

**Written solution:** There is one real object and one singleton control cell. The control color encodes the transform: 1 = keep as is, 2 = rotate clockwise, 3 = rotate 180°, 4 = rotate counterclockwise. Return the transformed object cropped tightly.

**Program solution (Python reference):**
```python
def solve_medium_73_rotate_source_by_control_color(g):
    h,w=dims(g)
    control=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in (1,2,3,4) and sum(1 for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]!=0)==0:
                control=v
            elif v!=0:
                cells.append((r,c))
    if control is None or not cells:
        return [[0]]
    source=crop_bbox(g, bbox(cells))
    return apply_transform(source, control)
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 8 0 0 0 0 0
0 0 0 0 6 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6
8 8 0
8 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 8 9 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
9 9 0
9 8 0
0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 0
7 8 8
7 0 0
```

**Train 4 input**
```text
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 7 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 7 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 7
0 6 0
7 6 6
```

**Test 1 input**
```text
0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 9 0 0 0 0
0 0 0 0 0 0 7 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 7 7
9 9 0
9 0 0
```

## Scale the Smallest Component and Recolor It (`medium_74_scale_smallest_component_and_recolor`)

**Difficulty:** medium

**Skills:** component size comparison, scaling, marker-based recolor

**Scaffold notes:**
- Separate the singleton marker from the real objects.
- Compare the areas of the remaining components.
- Scale the smallest one 2× and recolor it with the marker color.

**Written solution:** Ignore the singleton marker until the end. Find the smallest multi-cell component, crop it, enlarge it by a factor of two, and recolor every nonzero cell to the marker color.

**Program solution (Python reference):**
```python
def solve_medium_74_scale_smallest_component_and_recolor(g):
    comps=connected_components(g)
    marker=None
    pieces=[]
    for comp in comps:
        if comp['area']==1:
            marker=comp['color']
        else:
            pieces.append(comp)
    target=min(pieces, key=lambda c:(c['area'], c['bbox'][0], c['bbox'][1]))
    cropped=crop_bbox(g, target['bbox'])
    return recolor(scale2(cropped), marker)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 8 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 7 0 7 0 0 4 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
0 0 8 8 0 0
0 0 8 8 0 0
0 0 8 8 0 0
0 0 8 8 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 9 9 0 0 0 0 2 0 0
0 0 9 9 0 0 0 0 0 2 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 7 7 7 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 6 6 6
6 6 6 6 6 6
0 0 6 6 0 0
0 0 6 6 0 0
0 0 6 6 0 0
0 0 6 6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 9 9 0 4 0 0 0 0
0 0 0 0 0 9 9 0 0 0 0 0 0 0
0 2 2 2 0 9 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 3 3 3
3 3 3 3
3 3 3 3
3 3 3 3
3 3 0 0
3 3 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 5 5 5 5 5
5 5 5 5 5 5
0 0 5 5 0 0
0 0 5 5 0 0
0 0 5 5 0 0
0 0 5 5 0 0
```

**Test 1 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 7 7 7
7 7 7 7
7 7 7 7
7 7 7 7
7 7 0 0
7 7 0 0
```

## Quadrant Majority Summary (`medium_75_quadrant_majority_summary`)

**Difficulty:** medium

**Skills:** abstraction, quadrant partitioning, size-changing summary

**Scaffold notes:**
- The input height and width are even.
- Each output cell summarizes one quadrant.
- Ignore zeros when counting the majority color.

**Written solution:** Split the input into four equal quadrants. For each quadrant, find the majority nonzero color and write those four answers into a 2×2 summary grid.

**Program solution (Python reference):**
```python
def solve_medium_75_quadrant_majority_summary(g):
    h,w=dims(g)
    hm,wm=h//2,w//2
    quads=[
        [g[r][c] for r in range(0,hm) for c in range(0,wm)],
        [g[r][c] for r in range(0,hm) for c in range(wm,w)],
        [g[r][c] for r in range(hm,h) for c in range(0,wm)],
        [g[r][c] for r in range(hm,h) for c in range(wm,w)],
    ]
    return [
        [majority_nonzero(quads[0]), majority_nonzero(quads[1])],
        [majority_nonzero(quads[2]), majority_nonzero(quads[3])],
    ]
```

**Train 1 input**
```text
2 0 2 0 7 7
2 2 0 7 0 0
0 2 0 7 7 0
3 3 0 0 0 8
0 3 0 8 8 0
3 0 0 8 0 8
```

**Train 1 output**
```text
2 7
3 8
```

**Train 2 input**
```text
4 4 0 0 6 0
0 4 4 6 6 0
4 0 0 0 6 0
0 0 0 9 0 9
0 0 0 9 9 0
0 0 0 0 9 0
```

**Train 2 output**
```text
4 6
0 9
```

**Train 3 input**
```text
5 5 5 0 2 2
0 5 0 2 0 2
0 0 0 0 0 2
7 0 0 0 8 0
7 7 0 8 8 8
0 7 0 0 0 8
```

**Train 3 output**
```text
5 2
7 8
```

**Train 4 input**
```text
1 0 1 0 0 3
1 1 0 3 3 3
0 0 0 0 3 0
4 0 0 0 6 0
0 4 4 0 6 0
4 4 0 6 6 6
```

**Train 4 output**
```text
1 3
4 6
```

**Test 1 input**
```text
2 2 0 7 0 7
0 2 0 0 7 7
2 0 2 0 0 7
0 5 0 9 0 0
5 5 0 9 9 0
0 5 0 0 9 9
```

**Test 1 output**
```text
2 7
5 9
```

## Recover Rectangles from Three Corners (`medium_76_recover_rectangles_from_three_corners`)

**Difficulty:** medium

**Skills:** geometric completion, corner reasoning, same-size transform

**Scaffold notes:**
- Group the corner points by color.
- Use the min and max row and column values to infer the fourth corner.
- Draw the whole border of that rectangle.

**Written solution:** Each color gives you three corners of an axis-aligned rectangle. Infer the missing corner and draw the full rectangle border.

**Program solution (Python reference):**
```python
def solve_medium_76_recover_rectangles_from_three_corners(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells)!=3:
            continue
        rs=sorted({r for r,c in cells})
        cs=sorted({c for r,c in cells})
        if len(rs)!=2 or len(cs)!=2:
            continue
        r0,r1=rs
        c0,c1=cs
        draw_rect_border(out, r0,c0,r1,c1,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0
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
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 4 4 4 4 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 0
0 3 3 3 3 0 9 0 9 0
0 3 0 0 3 0 9 0 9 0
0 3 0 0 3 0 9 9 9 0
0 3 0 0 3 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 0 0 0 5 0 6 6 6 0
0 0 0 5 0 0 0 5 0 6 0 6 0
0 0 0 5 0 0 0 5 0 6 0 6 0
0 0 0 5 5 5 5 5 0 6 0 6 0
0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
0 7 0 0 7 0 0 2 2 2 2 0
0 7 0 0 7 0 0 2 0 0 2 0
0 7 0 0 7 0 0 2 0 0 2 0
0 7 7 7 7 0 0 2 0 0 2 0
0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Cast Rays Inward from the Border Until a Block (`medium_77_border_rays_until_block`)

**Difficulty:** medium

**Skills:** border-aware direction, ray casting, blockers

**Scaffold notes:**
- Border position determines direction: top goes down, bottom goes up, left goes right, right goes left.
- The gray cells are blockers.
- Fill only the blank cells along the ray.

**Written solution:** A colored seed on the border shoots inward from its side of the grid. Extend its color in a straight line until the next nonzero blocking cell or the edge stops it.

**Program solution (Python reference):**
```python
def solve_medium_77_border_rays_until_block(g):
    out=clone(g)
    h,w=dims(g)
    seeds=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v==5:
                continue
            if r==0:
                seeds.append((v,r,c,1,0))
            elif r==h-1:
                seeds.append((v,r,c,-1,0))
            elif c==0:
                seeds.append((v,r,c,0,1))
            elif c==w-1:
                seeds.append((v,r,c,0,-1))
    for color,r,c,dr,dc in seeds:
        rr,cc=r+dr,c+dc
        while 0<=rr<h and 0<=cc<w and g[rr][cc]==0:
            out[rr][cc]=color
            rr+=dr
            cc+=dc
    return out
```

**Train 1 input**
```text
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
```

**Train 1 output**
```text
0 0 2 0 0 7 0 0 0 0
0 0 2 0 0 7 0 0 0 0
0 0 2 0 0 7 0 0 0 0
0 0 2 0 0 7 0 0 0 0
3 3 3 3 5 7 0 0 0 0
0 0 2 0 0 7 0 0 0 0
0 0 2 0 0 7 0 5 0 0
0 0 2 0 0 7 0 0 0 0
0 0 2 0 0 7 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 5 6 0
0 0 4 0 0 0 0 6 0
0 0 4 5 8 8 8 8 8
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 5 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 0 0 0 0 0 0 0 9 0
7 0 0 0 0 0 0 0 0 9 0
7 0 0 0 0 5 0 0 0 9 0
7 4 4 4 4 4 4 4 4 4 4
7 0 0 0 0 0 0 0 0 9 0
7 0 0 0 0 0 0 0 5 9 0
7 0 0 5 0 0 0 0 0 9 0
7 0 0 0 0 0 0 0 0 9 0
```

**Train 4 input**
```text
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0
```

**Train 4 output**
```text
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 8 0
0 3 0 0 5 0 0 8 0
2 2 2 2 2 2 2 8 2
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 8 0
```

**Test 1 input**
```text
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 2 0 6 0 0 0 0 0
0 0 2 0 6 0 0 0 0 0
0 0 2 0 6 0 0 0 0 0
0 0 2 0 6 5 0 0 0 0
0 0 2 0 6 0 0 0 0 0
0 0 2 0 6 0 0 0 0 0
8 8 2 8 8 8 8 8 8 8
0 0 2 0 6 0 0 5 0 0
0 0 2 0 6 0 0 0 0 0
0 0 2 0 6 0 0 0 0 0
```

## Library Lookup Transform Gallery (`hard_71_library_lookup_transform_gallery`)

**Difficulty:** hard

**Skills:** library retrieval, code-driven transforms, panel composition

**Scaffold notes:**
- The top row chooses which library item to use.
- The second row chooses the rotation for that slot.
- Ignore the frames and output only the transformed library contents, packed left to right.

**Written solution:** Read the command strip at the top. Each selector chooses one library panel, and the number beneath it chooses a rotation. Extract the selected library shapes, apply the requested rotations, and place the transformed results side by side.

**Program solution (Python reference):**
```python
def solve_hard_71_library_lookup_transform_gallery(g):
    h,w=dims(g)
    frames=sorted([comp for comp in connected_components(g, colors=[9])], key=lambda c:(c['bbox'][1], c['bbox'][0]))
    library=[]
    for frame in frames:
        r0,c0,r1,c1=frame['bbox']
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]
        library.append(crop_nonzero(inner))
    cols=[c for c,v in enumerate(g[0]) if v!=0]
    pieces=[]
    for c in cols:
        sel=g[0][c]
        tr=g[1][c]
        if 1<=sel<=len(library) and tr in (1,2,3,4):
            pieces.append(apply_transform(library[sel-1], tr))
    return hstack(pieces, gap=1)
```

**Train 1 input**
```text
0 0 1 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 4 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 7 0 0 9 0 9 7 7 7 9 0 9 8 8 0 9
0 9 7 0 0 9 0 9 0 8 0 9 0 9 0 8 9 9
0 9 7 7 7 9 0 9 0 8 0 9 0 9 0 9 9 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
```

**Train 1 output**
```text
7 7 7 0 0 9 9 0 7 7 7
7 0 0 0 8 8 9 0 0 8 0
7 0 0 0 8 0 0 0 0 8 0
```

**Train 2 input**
```text
0 0 0 3 0 0 0 0 1 0 0 0 0 2 0 0 0 1 0 0
0 0 0 3 0 0 0 0 4 0 0 0 0 2 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9
0 9 7 0 0 9 0 0 9 6 6 7 9 0 0 9 0 6 0 9
0 9 7 9 0 9 0 0 9 0 6 0 9 0 0 9 6 8 6 9
0 9 7 9 9 9 0 0 9 7 6 6 9 0 0 9 0 6 0 9
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9
```

**Train 2 output**
```text
0 6 0 0 0 0 9 0 7 0 6 0 7 0 0
6 8 6 0 0 9 9 0 6 6 6 0 7 9 0
0 6 0 0 7 7 7 0 6 0 7 0 7 9 9
```

**Train 3 input**
```text
0 2 0 0 0 3 0 0 0 1 0 0 0 0 0 0 0 0 0
0 4 0 0 0 2 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 9 9 9 9 9
0 9 8 8 0 9 0 0 9 7 7 7 9 0 9 7 0 0 9
0 9 0 8 9 9 0 0 9 0 8 0 9 0 9 7 0 0 9
0 9 0 9 9 9 0 0 9 0 8 0 9 0 9 7 7 7 9
0 9 9 9 9 9 0 0 9 9 9 9 9 0 9 9 9 9 9
```

**Train 3 output**
```text
7 0 0 0 7 7 7 0 9 9 0
7 8 8 0 7 0 0 0 9 8 0
7 0 0 0 7 0 0 0 0 8 8
```

**Train 4 input**
```text
0 0 2 0 0 0 1 0 0 0 3 0 0 0 3 0 0 0 0 0 0
0 0 1 0 0 0 4 0 0 0 1 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 9 9 9 9 9 0 0 9 9 9 9 9
0 9 0 6 0 9 0 0 0 9 7 0 0 9 0 0 9 6 6 7 9
0 9 6 8 6 9 0 0 0 9 7 9 0 9 0 0 9 0 6 0 9
0 9 0 6 0 9 0 0 0 9 7 9 9 9 0 0 9 7 6 6 9
0 9 9 9 9 9 0 0 0 9 9 9 9 9 0 0 9 9 9 9 9
```

**Train 4 output**
```text
7 0 0 0 0 6 0 0 6 6 7 0 7 0 6
7 9 0 0 6 8 6 0 0 6 0 0 6 6 6
7 9 9 0 0 6 0 0 7 6 6 0 6 0 7
```

**Test 1 input**
```text
0 0 3 0 0 0 1 0 0 0 2 0 0 0 1 0 0 0 0
0 0 2 0 0 0 1 0 0 0 4 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 9 9 9 9 9
0 9 7 0 0 9 0 0 9 0 6 0 9 0 9 8 8 0 9
0 9 7 0 0 9 0 0 9 6 8 6 9 0 9 0 8 9 9
0 9 7 7 7 9 0 0 9 0 6 0 9 0 9 0 9 9 9
0 9 9 9 9 9 0 0 9 9 9 9 9 0 9 9 9 9 9
```

**Test 1 output**
```text
0 0 8 0 7 0 0 0 0 6 0 0 7 7 7
9 8 8 0 7 0 0 0 6 8 6 0 0 0 7
9 9 0 0 7 7 7 0 0 6 0 0 0 0 7
```

## Boolean Operation by Marker (`hard_72_boolean_operation_by_marker`)

**Difficulty:** hard

**Skills:** binary shape logic, control code, panel extraction

**Scaffold notes:**
- Ignore the panel borders after extracting the two inner masks.
- Read the singleton control code first.
- Compute union, intersection, or xor on the two masks, then color the surviving cells with 8.

**Written solution:** The two framed panels contain two binary shapes. The singleton control cell decides the operation: 4 = union, 5 = intersection, 6 = exclusive-or. Apply that boolean operation to the two panel masks and return the resulting shape cropped tightly in color 8.

**Program solution (Python reference):**
```python
def solve_hard_72_boolean_operation_by_marker(g):
    op_code=None
    for row in g:
        for v in row:
            if v in (4,5,6):
                op_code=v
                break
        if op_code is not None:
            break
    frames=sorted([comp for comp in connected_components(g, colors=[9])], key=lambda c:c['bbox'][1])
    if len(frames)<2:
        return [[0]]
    shapes=[]
    for frame in frames[:2]:
        r0,c0,r1,c1=frame['bbox']
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]
        shapes.append([[1 if v!=0 else 0 for v in row] for row in inner])
    a,b=shapes
    h=len(a); w=len(a[0])
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            va=a[r][c]
            vb=b[r][c]
            keep=0
            if op_code==4:
                keep=1 if (va or vb) else 0
            elif op_code==5:
                keep=1 if (va and vb) else 0
            elif op_code==6:
                keep=1 if ((va+vb)==1) else 0
            if keep:
                out[r][c]=8
    return crop_nonzero(out)
```

**Train 1 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 2 0 2 0 9 0 0 9 0 3 0 0 9 0
0 9 2 0 2 0 9 0 0 9 3 3 3 0 9 0
0 9 2 2 2 0 9 0 0 9 0 3 0 0 9 0
0 9 0 0 0 0 9 0 0 9 0 0 0 0 9 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
```

**Train 1 output**
```text
8 8 8
8 8 8
8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 2 0 0 0 9 0 0 9 0 0 3 3 9 0
0 9 0 2 0 0 9 0 0 9 0 3 3 0 9 0
0 9 0 0 2 0 9 0 0 9 3 3 0 0 9 0
0 9 0 0 0 2 9 0 0 9 0 0 0 0 9 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
```

**Train 2 output**
```text
8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 2 0 0 0 9 0 0 9 0 0 3 0 9 0
0 9 2 0 0 0 9 0 0 9 0 3 3 0 9 0
0 9 2 2 2 0 9 0 0 9 3 3 0 0 9 0
0 9 0 0 0 0 9 0 0 9 0 0 0 0 9 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
```

**Train 3 output**
```text
8 0 8
8 8 8
0 0 8
```

**Train 4 input**
```text
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 2 2 2 2 9 0 0 9 0 3 0 0 9 0
0 9 2 0 0 2 9 0 0 9 3 3 3 0 9 0
0 9 2 0 0 2 9 0 0 9 0 3 0 0 9 0
0 9 2 2 2 2 9 0 0 9 0 0 0 0 9 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
```

**Train 4 output**
```text
0 8
8 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 2 0 2 0 9 0 0 9 0 0 3 0 9 0
0 9 2 0 2 0 9 0 0 9 0 3 3 0 9 0
0 9 2 2 2 0 9 0 0 9 3 3 0 0 9 0
0 9 0 0 0 0 9 0 0 9 0 0 0 0 9 0
0 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
```

**Test 1 output**
```text
8 0 0
8 8 0
0 0 8
```

## Choose the Most-Holed Component, Scale, and Recolor (`hard_73_choose_most_holes_scale2_recolor`)

**Difficulty:** hard

**Skills:** hole counting, component comparison, scaling and recolor

**Scaffold notes:**
- Treat holes as fully enclosed zero regions inside an object.
- Compare all objects by hole count, not by color.
- After selecting the winner, enlarge it 2× and recolor it to the marker color.

**Written solution:** Ignore the singleton marker until the end. Among the multi-cell objects, choose the one with the most enclosed holes, crop it, scale it by 2, and recolor all nonzero cells with the marker color.

**Program solution (Python reference):**
```python
def solve_hard_73_choose_most_holes_scale2_recolor(g):
    comps=connected_components(g)
    marker=None
    objs=[]
    for comp in comps:
        if comp['area']==1:
            marker=comp['color']
        else:
            objs.append(comp)
    scored=[]
    for comp in objs:
        cropped=crop_bbox(g, comp['bbox'])
        holes=hole_count_binary(cropped)
        scored.append((holes, comp['area'], comp['bbox'][0], comp['bbox'][1], cropped))
    _,_,_,_,target=max(scored)
    return recolor(scale2(target), marker)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 3 3 3 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 3 3 3 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
2 2 0 0 0 0 0 0 2 2
2 2 0 0 0 0 0 0 2 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
2 2 0 0 0 0 0 0 2 2
2 2 0 0 0 0 0 0 2 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 0 0 0 0 9 9 0 0 0 0 9 9
9 9 0 0 0 0 9 9 0 0 0 0 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 0 0 0 0 9 9 0 0 0 0 9 9
9 9 0 0 0 0 9 9 0 0 0 0 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 4 4 4 0 0 0
0 3 3 3 0 0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 0 0 0 0 0 0 5 5
5 5 0 0 0 0 0 0 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 0 0 0 0 0 0 5 5
5 5 0 0 0 0 0 0 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 3 3 3 0 0 0 8 0 0 8 0 0 8 0 0
0 0 0 0 3 3 3 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 0 0 0 0 7 7 0 0 0 0 7 7
7 7 0 0 0 0 7 7 0 0 0 0 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 0 0 0 0 7 7 0 0 0 0 7 7
7 7 0 0 0 0 7 7 0 0 0 0 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 0 8 8 8 8 8 8 8 0 6 6 6 6 6 0 0 0
0 0 0 8 0 0 8 0 0 8 0 6 0 0 0 6 0 0 0
0 0 0 8 8 8 8 8 8 8 0 6 6 6 6 6 0 0 0
0 0 0 8 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0
```

**Test 1 output**
```text
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 0 0 0 0 4 4 0 0 0 0 4 4
4 4 0 0 0 0 4 4 0 0 0 0 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 0 0 0 0 4 4 0 0 0 0 4 4
4 4 0 0 0 0 4 4 0 0 0 0 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
```

## Fill the Keyed Chambers Inside Frames (`hard_74_fill_keyed_chambers_inside_frames`)

**Difficulty:** hard

**Skills:** constrained flood fill, frame-local reasoning, multiple independent regions

**Scaffold notes:**
- Process each colored key separately.
- You may move through blanks but not through walls or frame borders.
- Fill only the chamber connected to the key.

**Written solution:** Inside each framed maze, fill the entire chamber that contains the colored key cell. Walls and frame borders stop the fill.

**Program solution (Python reference):**
```python
def solve_hard_74_fill_keyed_chambers_inside_frames(g):
    out=clone(g)
    h,w=dims(g)
    seeds=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v not in (5,9):
                seeds.append((r,c,v))
    for r,c,color in seeds:
        q=deque([(r,c)])
        seen={(r,c)}
        while q:
            rr,cc=q.popleft()
            out[rr][cc]=color
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=rr+dr,cc+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen:
                    if g[nr][nc] not in (5,9) and (g[nr][nc]==0 or g[nr][nc]==color):
                        seen.add((nr,nc))
                        q.append((nr,nc))
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 5 0 0 9 0 0 9 9 9 9 9 9 9 0 0
0 9 0 2 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0 0
0 9 5 5 5 5 5 5 9 0 0 9 0 0 5 0 0 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 7 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 0 0 0 9 0 0
0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0
0 9 2 2 2 5 0 0 9 0 0 9 9 9 9 9 9 9 0 0
0 9 2 2 2 5 0 0 9 0 0 9 7 7 5 7 7 9 0 0
0 9 2 2 2 5 0 0 9 0 0 9 7 7 5 7 7 9 0 0
0 9 2 2 2 5 0 0 9 0 0 9 7 7 5 7 7 9 0 0
0 9 5 5 5 5 5 5 9 0 0 9 7 7 5 7 7 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 7 7 5 7 7 9 0 0
0 9 0 0 0 5 0 0 9 0 0 9 7 7 7 7 7 9 0 0
0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 5 0 0 9 0 0 9 9 9 9 9 9 9 0
0 9 0 0 5 0 4 9 0 0 9 0 0 0 5 0 9 0
0 9 0 0 5 0 0 9 0 0 9 0 0 0 5 0 9 0
0 9 5 5 5 5 5 9 0 0 9 5 5 5 5 5 9 0
0 9 0 0 5 0 0 9 0 0 9 0 0 0 5 0 9 0
0 9 0 0 5 0 0 9 0 0 9 0 0 0 5 0 9 0
0 9 0 0 0 0 0 9 0 0 9 0 8 0 0 0 9 0
0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 5 4 4 9 0 0 9 9 9 9 9 9 9 0
0 9 0 0 5 4 4 9 0 0 9 0 0 0 5 0 9 0
0 9 0 0 5 4 4 9 0 0 9 0 0 0 5 0 9 0
0 9 5 5 5 5 5 9 0 0 9 5 5 5 5 5 9 0
0 9 0 0 5 0 0 9 0 0 9 8 8 8 5 8 9 0
0 9 0 0 5 0 0 9 0 0 9 8 8 8 5 8 9 0
0 9 0 0 0 0 0 9 0 0 9 8 8 8 8 8 9 0
0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 5 0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 5 0 0 9 0 0 9 9 9 9 9 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 0 5 0 0 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 0 5 0 3 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 0 5 0 0 9 0
0 0 9 5 5 5 5 5 5 9 0 0 9 0 5 0 0 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 0 5 0 0 9 0
0 0 9 0 5 0 5 0 0 9 0 0 9 0 0 0 0 9 0
0 0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 5 0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 5 0 0 9 0 0 9 9 9 9 9 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 3 5 3 3 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 3 5 3 3 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 3 5 3 3 9 0
0 0 9 5 5 5 5 5 5 9 0 0 9 3 5 3 3 9 0
0 0 9 0 0 0 5 0 0 9 0 0 9 3 5 3 3 9 0
0 0 9 0 5 0 5 0 0 9 0 0 9 3 3 3 3 9 0
0 0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 0 0 5 0 0 9 0 0 9 9 9 9 9 9 0
0 9 0 6 5 0 0 9 0 0 9 0 5 0 0 9 0
0 9 0 0 5 0 0 9 0 0 9 0 5 0 0 9 0
0 9 5 5 5 5 5 9 0 0 9 0 5 0 0 9 0
0 9 0 0 5 0 0 9 0 0 9 0 5 0 0 9 0
0 9 0 0 0 0 0 9 0 0 9 0 5 0 2 9 0
0 9 9 9 9 9 9 9 0 0 9 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 6 6 5 0 0 9 0 0 9 9 9 9 9 9 0
0 9 6 6 5 0 0 9 0 0 9 2 5 2 2 9 0
0 9 6 6 5 0 0 9 0 0 9 2 5 2 2 9 0
0 9 5 5 5 5 5 9 0 0 9 2 5 2 2 9 0
0 9 0 0 5 0 0 9 0 0 9 2 5 2 2 9 0
0 9 0 0 0 0 0 9 0 0 9 2 5 2 2 9 0
0 9 9 9 9 9 9 9 0 0 9 2 2 2 2 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 5 0 0 9 0 0 9 9 9 9 9 9 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 4 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0
0 9 5 5 5 5 5 5 9 0 0 9 5 5 5 5 5 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 0 0 9 0
0 9 0 8 0 5 0 0 9 0 0 9 0 0 0 0 0 9 0
0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 5 0 0 9 0 0 9 9 9 9 9 9 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 4 4 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 4 4 9 0
0 9 0 0 0 5 0 0 9 0 0 9 0 0 5 4 4 9 0
0 9 5 5 5 5 5 5 9 0 0 9 5 5 5 5 5 9 0
0 9 8 8 8 5 0 0 9 0 0 9 0 0 5 0 0 9 0
0 9 8 8 8 5 0 0 9 0 0 9 0 0 0 0 0 9 0
0 9 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Rotational Equivalence Matrix (`hard_75_rotational_equivalence_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, rotation invariance, abstract relation matrix

**Scaffold notes:**
- Crop each framed shape.
- Convert it to a binary shape and normalize over the four rotations.
- Write 8 for matching pairs in the relation matrix.

**Written solution:** Compare the framed shapes pairwise, ignoring color and allowing rotation. Output a matrix with 8 wherever two shapes are equivalent up to rotation, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_75_rotational_equivalence_matrix(g):
    frames=sorted([comp for comp in connected_components(g, colors=[9])], key=lambda c:c['bbox'][1])
    shapes=[]
    for frame in frames:
        r0,c0,r1,c1=frame['bbox']
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]
        shapes.append(canonical_rot(inner))
    n=len(shapes)
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if shapes[i]==shapes[j]:
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 2 0 0 9 0 9 2 2 2 9 0 9 4 4 4 9
0 9 2 0 0 9 0 9 2 0 0 9 0 9 0 4 0 9
0 9 2 2 2 9 0 9 2 0 0 9 0 9 0 4 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
```

**Train 1 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 3 3 9 0 9 0 0 3 9 0 9 2 0 0 9
0 9 3 3 0 9 0 9 0 3 3 9 0 9 2 0 0 9
0 9 3 0 0 9 0 9 3 3 0 9 0 9 2 2 2 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
```

**Train 2 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 9 9 9 9 9 9 0
0 9 5 5 0 0 9 0 9 0 0 0 5 9 0 9 6 0 6 0 9 0
0 9 0 5 5 0 9 0 9 0 5 5 5 9 0 9 6 6 6 0 9 0
0 9 0 0 5 0 9 0 9 5 5 0 0 9 0 9 0 0 6 0 9 0
0 9 0 0 5 5 9 0 9 5 0 0 0 9 0 9 0 0 6 0 9 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 9 9 9 9 9 9 0
```

**Train 3 output**
```text
8 8 0
8 8 0
0 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 0 0 9 9 9 9 9 9 0
0 9 7 7 0 0 9 0 9 4 4 4 9 0 0 9 0 0 0 7 9 0
0 9 0 7 0 0 9 0 9 0 4 0 9 0 0 9 0 7 7 7 9 0
0 9 0 7 7 7 9 0 9 0 4 0 9 0 0 9 0 7 0 0 9 0
0 9 0 0 0 7 9 0 9 9 9 9 9 0 0 9 7 7 0 0 9 0
0 9 9 9 9 9 9 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
```

**Train 4 output**
```text
8 0 8
0 8 0
8 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 9 9 9 9 9 0 0
0 9 6 0 6 0 9 0 9 0 6 0 0 9 0 9 0 3 3 9 0 0
0 9 6 6 6 0 9 0 9 0 6 0 0 9 0 9 3 3 0 9 0 0
0 9 0 0 6 0 9 0 9 0 6 6 6 9 0 9 3 0 0 9 0 0
0 9 0 0 6 0 9 0 9 0 6 0 6 9 0 9 9 9 9 9 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 0
8 8 0
0 0 8
```

## Rank Components by Area and Stack Them (`hard_76_rank_components_by_area_and_stack`)

**Difficulty:** hard

**Skills:** area ranking, recolor by rank, packed composition

**Scaffold notes:**
- The top row is a color code, not an object row.
- Compare the component areas below it.
- Recolor by rank and pack the cropped pieces vertically.

**Written solution:** Read the three rank colors from the top row. Sort the multi-cell components by area from largest to smallest, recolor them with the rank colors in that order, and stack the cropped results vertically with one blank row between them.

**Program solution (Python reference):**
```python
def solve_hard_76_rank_components_by_area_and_stack(g):
    h,w=dims(g)
    rank_colors=[v for v in g[0] if v!=0]
    work=[row[:] for row in g[1:]]
    comps=[c for c in connected_components(work) if c['area']>1]
    comps=sorted(comps, key=lambda c:(-c['area'], c['bbox'][0], c['bbox'][1]))
    pieces=[]
    for comp, color in zip(comps, rank_colors):
        cropped=crop_bbox(work, comp['bbox'])
        pieces.append(recolor(cropped, color))
    return vstack(pieces, gap=1)
```

**Train 1 input**
```text
0 2 0 4 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 2
2 0 2
2 2 2
0 0 0
4 4 0
4 4 0
4 0 0
0 0 0
7 0 0
7 0 0
7 7 7
```

**Train 2 input**
```text
0 8 0 5 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0 0 0
0 2 2 0 0 0 0 0 0 7 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8
0 8 0
0 8 0
0 0 0
0 5 5
5 5 0
5 0 0
0 0 0
1 1 0
1 1 0
1 0 0
```

**Train 3 input**
```text
0 6 0 3 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 0 6
6 0 6
6 6 6
0 0 0
3 0 0
3 0 0
3 3 3
0 0 0
0 9 9
9 9 0
9 0 0
```

**Train 4 input**
```text
0 7 0 2 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 5 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 0 7
7 0 7
7 7 7
0 0 0
2 2 0
2 2 0
2 0 0
0 0 0
4 4 4
0 4 0
0 4 0
```

**Test 1 input**
```text
0 5 0 8 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 9 9 9 0 0 0 0 0 4 4 4 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 5 5
5 5 0
5 0 0
0 0 0
8 0 0
8 0 0
8 8 8
0 0 0
2 2 2
0 2 0
0 2 0
```

## Cross-Product Intersection Gallery (`hard_77_cross_product_intersection_gallery`)

**Difficulty:** hard

**Skills:** panel composition, pairwise intersections, structured output layout

**Scaffold notes:**
- Extract the two top templates and the two left templates.
- For every row-template/column-template pair, keep only the cells where both templates are nonzero.
- Arrange the four resulting panels in a 2×2 gallery.

**Written solution:** The top framed panels define the column templates and the left framed panels define the row templates. Build a 2×2 gallery where each cell is the binary intersection of one row template with one column template, colored with 8.

**Program solution (Python reference):**
```python
def solve_hard_77_cross_product_intersection_gallery(g):
    frames6=sorted([comp for comp in connected_components(g, colors=[6])], key=lambda c:c['bbox'][1])
    frames7=sorted([comp for comp in connected_components(g, colors=[7])], key=lambda c:c['bbox'][0])
    cols=[]
    rows=[]
    for frame in frames6:
        r0,c0,r1,c1=frame['bbox']
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]
        cols.append([[1 if v!=0 else 0 for v in row] for row in inner])
    for frame in frames7:
        r0,c0,r1,c1=frame['bbox']
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]
        rows.append([[1 if v!=0 else 0 for v in row] for row in inner])
    gallery_rows=[]
    for rshape in rows:
        panels=[]
        for cshape in cols:
            h=len(rshape); w=len(rshape[0])
            inter=zeros(h,w)
            for r in range(h):
                for c in range(w):
                    if rshape[r][c] and cshape[r][c]:
                        inter[r][c]=8
            panels.append(inter)
        gallery_rows.append(hstack(panels, gap=1))
    return vstack(gallery_rows, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 6 2 2 0 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 0 2 2 0 6 6 3 3 3 0 6
0 0 0 0 0 0 0 0 6 0 0 2 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 0 0 2 2 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 4 0 0 0 7 7 0 5 5 0 7 0 0 0 0 0 0 0
0 7 4 4 0 0 7 7 5 5 0 0 7 0 0 0 0 0 0 0
0 7 0 4 4 0 7 7 0 5 5 0 7 0 0 0 0 0 0 0
0 7 0 0 4 4 7 7 0 0 5 5 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 0 0 8 8 0 8 0 0
0 8 0 0 8 8 8 8 0 0
0 0 8 0 8 8 0 8 0 0
0 0 8 8 8 8 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 6 0 3 0 0 6 6 6 0 6 0 6
0 0 0 0 0 0 0 0 6 3 3 3 0 6 6 6 6 6 0 6
0 0 0 0 0 0 0 0 6 0 3 0 0 6 6 0 0 6 0 6
0 0 0 0 0 0 0 0 6 0 3 0 0 6 6 0 0 6 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 0 5 5 0 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 5 5 0 0 7 7 7 7 7 0 7 0 0 0 0 0 0 0
0 7 0 5 5 0 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 0 0 5 5 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8 0 0 8 8 0 0 0 0
8 8 0 0 8 8 8 8 8 0
0 8 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 6 2 2 0 0 6 6 6 0 6 0 6
0 0 0 0 0 0 0 0 6 0 2 2 0 6 6 6 6 6 0 6
0 0 0 0 0 0 0 0 6 0 0 2 0 6 6 0 0 6 0 6
0 0 0 0 0 0 0 0 6 0 0 2 2 6 6 0 0 6 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 4 0 0 0 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 4 4 0 0 7 7 7 7 7 0 7 0 0 0 0 0 0 0
0 7 0 4 4 0 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 0 0 4 4 7 7 0 7 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0 0 8 8 0 0 0 0
0 8 0 0 8 8 8 8 8 0
0 0 8 0 8 8 0 0 0 0
0 0 8 8 8 8 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 6 6 0 6 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 6 6 6 0 6 6 3 3 3 0 6
0 0 0 0 0 0 0 0 6 0 0 6 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 0 0 6 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 4 0 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 0 7 7 4 4 0 0 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 0 4 4 0 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 0 0 4 4 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 8 8 0 0 0 0
8 8 8 0 8 8 8 8 0 0
0 0 0 0 8 8 0 8 0 0
0 0 0 0 8 8 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 6 2 2 0 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 0 2 2 0 6 6 3 3 3 0 6
0 0 0 0 0 0 0 0 6 0 0 2 0 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 0 0 2 2 6 6 0 3 0 0 6
0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 0 5 5 0 7 0 0 0 0 0 0 0
0 7 7 7 7 0 7 7 5 5 0 0 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 0 5 5 0 7 0 0 0 0 0 0 0
0 7 0 7 0 0 7 7 0 0 5 5 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 8 0 0 8 8 0 8 0 0
0 8 8 0 8 8 8 8 0 0
0 0 0 0 8 8 0 8 0 0
0 0 0 0 8 8 0 0 0 0
```
