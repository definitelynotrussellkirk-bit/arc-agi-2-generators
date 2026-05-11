# ARC Puzzle Bank — Eighth 21 Puzzles
This eighth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`50`–`56`) so it follows directly after the seventh bundle.
This volume leans harder into diagonal reasoning, bounding-box abstraction, ray casting, frame-local selection, rotation-invariant comparison, and boolean shape composition. It also introduces a few reusable solver primitives that fit your pipeline well: `march_until_block`, `canonical_shape_under_rotation`, hole counting on cropped components, and keyed frame-local transforms.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_eighth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_eighth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_eighth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_50_diagonal_bridge` — **Draw Each Diagonal between Matching Endpoints**
- `easy_51_crop_nonzero_bbox` — **Crop the Smallest Box Covering All Colored Cells**
- `easy_52_markers_to_hollow_squares` — **Replace Each Marker with a Hollow 3×3 Square**
- `easy_53_keep_tallest_bar` — **Keep Only the Tallest Vertical Bar**
- `easy_54_reflect_main_diagonal` — **Reflect Everything across the Main Diagonal**
- `easy_55_move_object_to_marker` — **Move the Object so its Top-Left Corner Lands on the Marker**
- `easy_56_pack_nonempty_rows` — **Remove All Empty Rows**

### Medium (7)
- `medium_50_emit_rays` — **Emit Rays until a Gray Blocker**
- `medium_51_keyed_component_rotate` — **Pick the Component Named by the Key and Rotate it Clockwise**
- `medium_52_sort_components_by_area` — **Sort the Components by Area and Pack Them into a Row**
- `medium_53_equality_matrix` — **Build the Equality Matrix from the Row and Column Headers**
- `medium_54_checker_fill_bboxes` — **Replace Each Component by a Checkerboard over Its Bounding Box**
- `medium_55_recolor_template_stamp` — **Stamp Recolored Copies of the Source Template**
- `medium_56_frame_majority_centers` — **Mark Each Frame with Its Majority Interior Color**

### Hard (7)
- `hard_50_frame_direction_rays` — **Cast the Keyed Ray inside Each Frame**
- `hard_51_dual_template_rotation_mosaic` — **Decode a Rotation Mosaic from Two Template Libraries**
- `hard_52_shape_similarity_matrix` — **Compare All Components up to Rotation**
- `hard_53_frame_select_rank_center` — **In Each Frame, Choose by Size Rank, Transform, and Recenter**
- `hard_54_boolean_ops_panel` — **Build the Boolean-Operation Gallery of Two Shapes**
- `hard_55_sort_by_holes` — **Sort the Components by Hole Count and Pack Them**
- `hard_56_frame_transform_gallery` — **Transform Each Framed Object and Build a Gallery**

## Draw Each Diagonal between Matching Endpoints (`easy_50_diagonal_bridge`)

**Difficulty:** easy

**Skills:** diagonal reasoning, line filling, color grouping

**Scaffold notes:**
- Start by pairing cells of the same color.
- Check whether the row change and column change have the same magnitude.
- Walk one step at a time along that diagonal and color every visited cell.

**Written solution:** Group the nonzero cells by color. In each group, the two cells are the endpoints of a 45-degree diagonal segment. Fill every cell along that diagonal, inclusive, with the same color.

**Program solution (Python reference):**
```python
def solve_easy_50_diagonal_bridge(g:Grid)->Grid:
    out=clone(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)>=2:
            # pair farthest apart if same diagonal
            (r0,c0),(r1,c1)=cells[0],cells[-1]
            dr=r1-r0; dc=c1-c0
            if abs(dr)==abs(dc) and dr!=0:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                for k in range(abs(dr)+1):
                    out[r0+sr*k][c0+sc*k]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 0 0 0 4 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 2 0 0 0 4 0
0 0 2 0 4 0 0
0 0 0 4 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 6 0 3 0 0
0 0 6 0 0 0 3 0
0 6 0 0 0 0 0 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 7 0 0
0 0 0 5 0 7 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 3 0 0 0 0 0 4 0 0
0 0 3 0 0 0 4 0 0 0
0 0 0 3 0 4 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Crop the Smallest Box Covering All Colored Cells (`easy_51_crop_nonzero_bbox`)

**Difficulty:** easy

**Skills:** bounding box, cropping, size change

**Scaffold notes:**
- Treat every nonzero cell as part of the foreground.
- Find the top, bottom, left, and right extremes.
- Return only that rectangle.

**Written solution:** Ignore the background. Find the minimum and maximum row and column occupied by any nonzero cell, then cut out exactly that rectangle.

**Program solution (Python reference):**
```python
def solve_easy_51_crop_nonzero_bbox(g:Grid)->Grid:
    cells=nonzero_cells(g)
    return crop_bbox(g,bbox(cells))
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 0 0
2 0 0 0 0 0
0 0 0 0 4 0
0 0 0 0 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 3 3 3
0 0 0 0 3 0
0 0 0 0 0 0
0 0 0 0 0 0
6 6 0 0 0 0
6 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 5 5 0 0 2 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 2
0 0 0 0 0 2
0 5 5 0 0 2
5 5 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 7 0 7
0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0
4 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 8 0 0 0 0 0
8 8 8 0 0 0 0
0 8 0 0 0 0 0
0 0 0 0 0 3 0
0 0 0 0 0 0 3
```

## Replace Each Marker with a Hollow 3×3 Square (`easy_52_markers_to_hollow_squares`)

**Difficulty:** easy

**Skills:** local stamping, neighborhood reasoning, shape replacement

**Scaffold notes:**
- Every colored cell stands alone and marks a center.
- Think in terms of a 3×3 neighborhood around each marker.
- Fill the ring, not the center.

**Written solution:** Each nonzero marker is the center of a 3×3 pattern. Erase the marker itself and draw the eight border cells of that 3×3 square in the marker's color, leaving the center empty.

**Program solution (Python reference):**
```python
def solve_easy_52_markers_to_hollow_squares(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0:
                for rr in range(r-1,r+2):
                    for cc in range(c-1,c+2):
                        if rr in (r-1,r+1) or cc in (c-1,c+1):
                            out[rr][cc]=v
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
0 2 2 2 0 0 0 0
0 2 0 2 0 0 0 0
0 2 2 2 0 0 0 0
0 0 0 0 4 4 4 0
0 0 0 0 4 0 4 0
0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 3 3 3 0 0
0 7 7 7 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0
0 0 8 8 8 0 0 2 2 2 0
0 0 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 4 0 4 0 0 0 0
0 0 4 4 4 7 7 7 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Keep Only the Tallest Vertical Bar (`easy_53_keep_tallest_bar`)

**Difficulty:** easy

**Skills:** counting, component selection, filtering

**Scaffold notes:**
- Treat each occupied column as one candidate bar.
- Count how many cells belong to that bar.
- Preserve only the maximum-height column.

**Written solution:** Each colored object is a solid one-column vertical bar. Measure the height of each bar and keep only the tallest one, erasing all the others.

**Program solution (Python reference):**
```python
def solve_easy_53_keep_tallest_bar(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    best=None
    for c in range(w):
        cells=[r for r in range(h) if g[r][c]!=0]
        if not cells:
            continue
        color=g[cells[0]][c]
        if all(g[r][c]==color for r in cells) and max(cells)-min(cells)+1==len(cells):
            height=len(cells)
            cand=(height,-min(cells),c,color,min(cells),max(cells))
            if best is None or cand>best:
                best=cand
    if best:
        _,_,c,color,r0,r1=best
        for r in range(r0,r1+1):
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 2 0 0 5 0 0 0
0 2 0 0 5 0 3 0
0 2 0 0 5 0 3 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 0
0 0 4 0 0 7 0 6 0
0 0 4 0 0 7 0 6 0
0 0 4 0 0 7 0 6 0
0 0 4 0 0 7 0 6 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 5 0
0 0 0 0 8 0 0 0 5 0
0 3 0 0 8 0 0 0 5 0
0 3 0 0 8 0 0 0 5 0
0 3 0 0 8 0 0 0 5 0
0 3 0 0 8 0 0 0 5 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 6 0 0 0 0 0 0 2 0
0 0 6 0 0 0 0 0 0 2 0
0 0 6 0 0 0 4 0 0 2 0
0 0 6 0 0 0 4 0 0 2 0
0 0 0 0 0 0 4 0 0 2 0
0 0 0 0 0 0 4 0 0 2 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 5 0 0 0 3 0 0 0 0
0 5 0 0 0 3 0 0 0 0
0 5 0 0 0 3 0 0 7 0
0 5 0 0 0 3 0 0 7 0
0 5 0 0 0 3 0 0 7 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
```

## Reflect Everything across the Main Diagonal (`easy_54_reflect_main_diagonal`)

**Difficulty:** easy

**Skills:** symmetry, transpose, square-grid reasoning

**Scaffold notes:**
- The grid is square, so row and column can be swapped.
- Each colored cell creates a partner across the main diagonal.
- Cells already on the diagonal stay where they are.

**Written solution:** Copy every colored cell to its transposed position: a cell at row r, column c also appears at row c, column r. Keep the original cells too.

**Program solution (Python reference):**
```python
def solve_easy_54_reflect_main_diagonal(g:Grid)->Grid:
    h,w=dims(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 2 0
0 3 0 2 0 0
0 0 0 0 0 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 2 0
0 3 0 2 0 0
0 0 0 0 0 4
0 2 0 0 0 0
2 0 0 0 0 0
0 0 4 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 5 0
0 0 0 0 0 0 2
0 0 0 0 5 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 5 0
0 0 0 0 0 0 2
0 0 0 0 5 0 0
0 0 0 7 0 0 0
0 0 5 0 0 0 0
5 0 0 0 0 0 0
0 2 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 8
0 0 0 0 3 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 8
0 0 0 0 3 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 4 0 0
0 3 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 8 0 0 0 0 0
8 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 6
0 0 0 0 2 0 0
0 0 7 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 6
0 0 0 0 2 0 0
0 0 7 0 0 2 0
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 2 0 0 0 0
6 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 3
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 3
0 0 0 0 5 0 0 0
0 0 0 5 0 0 0 0
0 4 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0
```

## Move the Object so its Top-Left Corner Lands on the Marker (`easy_55_move_object_to_marker`)

**Difficulty:** easy

**Skills:** translation, object extraction, anchor placement

**Scaffold notes:**
- Separate the magenta marker from the actual object.
- Use the object's bounding box to define what gets moved.
- The marker is the new top-left anchor.

**Written solution:** There is one real object and one magenta marker. Crop the object's bounding box, erase both the old object and the marker, and paste the cropped object back so that its top-left corner sits exactly on the marker cell.

**Program solution (Python reference):**
```python
def solve_easy_55_move_object_to_marker(g:Grid)->Grid:
    h,w=dims(g)
    marker_color=9
    marker=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==marker_color:
                marker=(r,c)
            elif v!=0:
                cells.append((r,c))
    r0,c0,r1,c1=bbox(cells)
    obj=crop_bbox(g,(r0,c0,r1,c1))
    # clear object and marker
    out=zeros(h,w,0)
    paste(out,obj,marker[0],marker[1],transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Remove All Empty Rows (`easy_56_pack_nonempty_rows`)

**Difficulty:** easy

**Skills:** row filtering, size change, order preservation

**Scaffold notes:**
- Scan the grid row by row.
- Keep only rows that contain at least one nonzero cell.
- Do not reorder the surviving rows.

**Written solution:** Delete every all-zero row and keep the remaining rows in their original top-to-bottom order. The width stays the same, but the output has fewer rows.

**Program solution (Python reference):**
```python
def solve_easy_56_pack_nonempty_rows(g:Grid)->Grid:
    rows=[row[:] for row in g if any(v!=0 for v in row)]
    return rows if rows else [[0]*len(g[0])]
```

**Train 1 input**
```text
0 0 0 0 0 0
2 0 0 2 0 0
0 0 0 0 0 0
0 3 3 0 0 0
0 0 0 0 0 0
4 0 0 0 4 0
```

**Train 1 output**
```text
2 0 0 2 0 0
0 3 3 0 0 0
4 0 0 0 4 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0
0 5 0 0 0 0 0
0 0 0 0 0 0 0
2 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 7 7 7 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 0 0 0 0 0
2 2 0 0 0 0 0
0 0 0 7 7 7 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0
3 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0
```

**Train 3 output**
```text
0 0 6 0 0 0 0 0
3 0 0 3 0 0 0 0
0 4 4 4 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0
8 0 8 0 0 0 0
0 0 0 0 0 0 0
0 0 0 2 0 2 0
0 0 0 0 0 0 0
0 5 0 0 5 0 0
```

**Train 4 output**
```text
8 0 8 0 0 0 0
0 0 0 2 0 2 0
0 5 0 0 5 0 0
```

**Test input**
```text
0 0 0 0 0 0
0 2 0 0 0 0
0 0 0 0 0 0
3 3 0 0 0 0
0 0 0 0 0 0
0 0 4 4 4 0
```

**Test output**
```text
0 2 0 0 0 0
3 3 0 0 0 0
0 0 4 4 4 0
```

## Emit Rays until a Gray Blocker (`medium_50_emit_rays`)

**Difficulty:** medium

**Skills:** direction codes, ray casting, obstacle handling

**Scaffold notes:**
- Map each emitter color to one cardinal direction.
- Advance one cell at a time through zeros.
- Stop just before a gray blocker or the edge.

**Written solution:** Colors 1, 2, 3, and 4 are directional emitters: up, right, down, and left. Starting from each emitter, extend a straight ray of the same color through empty cells until the ray would hit a gray 5 blocker or leave the grid.

**Program solution (Python reference):**
```python
def solve_medium_50_emit_rays(g:Grid)->Grid:
    h,w=dims(g)
    out=clone(g)
    dirs={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}
    blockers={5}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in dirs:
                dr,dc=dirs[v]
                for rr,cc in march_until_block(g,(r,c),dr,dc,blockers):
                    if out[rr][cc]==0:
                        out[rr][cc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 3 0
0 2 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 1 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 1 0 0 5 0 0 0 0
0 1 0 0 5 0 0 3 0
0 2 2 2 5 0 0 3 0
0 1 0 0 0 0 0 3 0
0 1 0 0 0 0 0 3 0
0 1 0 0 0 0 0 5 0
4 1 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 3 2
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
5 5 5 5 5 5 0 3 0
0 0 1 0 0 0 0 3 0
0 0 1 0 0 0 0 3 0
4 4 1 4 4 4 4 4 0
0 0 0 0 0 0 0 3 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 4 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 1 0 0 0 0 0 0 0 0
0 1 2 2 2 2 2 2 3 2
0 1 0 0 0 0 0 0 3 0
0 1 0 0 0 5 0 0 3 0
0 1 0 0 0 5 0 0 3 0
0 1 0 0 0 5 0 0 3 0
0 1 0 0 0 5 0 0 3 0
0 1 0 0 0 5 4 4 4 0
0 1 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 4 0
0 0 0 1 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 1 0 0 0 0 0 0
0 2 2 2 2 2 2 2 3 2
0 0 0 1 0 0 5 0 3 0
0 0 0 1 0 0 5 0 3 0
0 0 0 1 0 0 5 0 3 0
0 0 0 1 0 0 5 4 4 0
0 0 0 1 0 0 5 0 3 0
0 0 0 0 0 0 0 0 3 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 3 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 1 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 1 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 3 2
0 0 1 0 0 5 0 0 0 3 0
0 0 1 0 0 5 0 0 0 3 0
0 0 1 0 0 5 0 0 0 3 0
0 0 1 0 0 5 0 0 0 3 0
0 0 1 0 0 5 0 0 0 3 0
4 4 1 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 3 0
```

## Pick the Component Named by the Key and Rotate it Clockwise (`medium_51_keyed_component_rotate`)

**Difficulty:** medium

**Skills:** color keying, component extraction, rotation, cropping

**Scaffold notes:**
- Read the bottom key first.
- Match that key color to a full component elsewhere in the grid.
- Crop tightly before rotating.

**Written solution:** A singleton key on the last row names the color of the component to select from the main field. Find that component, crop it to its bounding box, then rotate the crop 90° clockwise.

**Program solution (Python reference):**
```python
def solve_medium_51_keyed_component_rotate(g:Grid)->Grid:
    h,w=dims(g)
    # key is singleton in last row
    key=None
    for c,v in enumerate(g[-1]):
        if v!=0:
            key=v; break
    comps=connected_components(g)
    # ignore key singleton on last row (component of size1 at last row)
    target=None
    for comp in comps:
        if comp["color"]==key and not (len(comp["cells"])==1 and comp["cells"][0][0]==h-1):
            target=comp
            break
    return rotate_cw(crop_bbox(g,target["bbox"]))
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 4 4 0 0
0 2 0 0 0 0 4 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
```

**Train 1 output**
```text
0 4
4 4
0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
```

**Train 2 output**
```text
0 7
7 7
7 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 8 8 8 0
0 2 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
```

**Train 3 output**
```text
2 2 2
0 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 5 0 0
0 6 0 0 0 0 0 5 5 5 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
```

**Train 4 output**
```text
5 5
5 0
5 5
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
```

**Test output**
```text
7 7 7
7 0 0
```

## Sort the Components by Area and Pack Them into a Row (`medium_52_sort_components_by_area`)

**Difficulty:** medium

**Skills:** component extraction, area sorting, packing

**Scaffold notes:**
- Count cells, not bounding-box size.
- Crop each component before packing.
- Use one blank column between packed pieces.

**Written solution:** Find each connected component, crop each one to its own bounding box, sort the crops by increasing number of colored cells, then place them left to right with a one-column gap, aligned to the top.

**Program solution (Python reference):**
```python
def solve_medium_52_sort_components_by_area(g:Grid)->Grid:
    comps=connected_components(g)
    comps_sorted=sorted(comps,key=lambda comp:(len(comp["cells"]), comp["bbox"][0], comp["bbox"][1]))
    pieces=[crop_bbox(g,comp["bbox"]) for comp in comps_sorted]
    heights=[len(p) for p in pieces]
    widths=[len(p[0]) for p in pieces]
    H=max(heights)
    W=sum(widths)+max(0,len(pieces)-1)
    out=zeros(H,W,0)
    x=0
    for p in pieces:
        paste(out,p,0,x,transparent=0)
        x+=len(p[0])+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 4 4 4 0 7 7
2 0 0 0 4 0 0 7 7
0 0 0 0 0 0 0 7 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 0 5 0 5 0 8 8 8
3 0 0 5 5 5 0 8 0 8
0 0 0 0 0 0 0 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0 0 0
0 6 6 0 0 0 4 4 4 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2 0 6 6 0 4 4 4
0 2 0 0 6 6 0 4 0 4
0 0 0 0 6 0 0 4 4 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 3 3 0 0 0 0 5 0 0 0 0
0 3 3 0 0 0 0 5 0 0 0 0
0 3 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 0 5 0 3 3
7 0 0 5 0 3 3
0 0 0 5 0 3 0
0 0 0 5 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 2 2 0 0 0 0 6 6 6 0 0
0 0 2 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 0 0 6 0 0 4 4 4
2 0 0 6 6 6 0 4 0 4
0 0 0 0 6 0 0 4 4 4
```

## Build the Equality Matrix from the Row and Column Headers (`medium_53_equality_matrix`)

**Difficulty:** medium

**Skills:** symbolic matching, matrix construction, header reasoning

**Scaffold notes:**
- Separate the top headers from the left headers.
- Compare one row header against one column header at a time.
- Only matches produce color in the output.

**Written solution:** The top row (excluding the corner) gives column headers and the left column (excluding the corner) gives row headers. Build the interior matrix so that a cell is filled with that color exactly when its row header and column header are equal; otherwise leave it black.

**Program solution (Python reference):**
```python
def solve_medium_53_equality_matrix(g:Grid)->Grid:
    h,w=dims(g)
    top=g[0][1:]
    left=[g[r][0] for r in range(1,h)]
    out=zeros(h-1,w-1,0)
    for r,a in enumerate(left):
        for c,b in enumerate(top):
            if a!=0 and a==b:
                out[r][c]=a
    return out
```

**Train 1 input**
```text
0 2 3 2 4
2 0 0 0 0
4 0 0 0 0
3 0 0 0 0
```

**Train 1 output**
```text
2 0 2 0
0 0 0 4
0 3 0 0
```

**Train 2 input**
```text
0 5 6 5 7 6
6 0 0 0 0 0
5 0 0 0 0 0
7 0 0 0 0 0
5 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 6
5 0 5 0 0
0 0 0 7 0
5 0 5 0 0
```

**Train 3 input**
```text
0 2 8 4 8
8 0 0 0 0
2 0 0 0 0
4 0 0 0 0
2 0 0 0 0
```

**Train 3 output**
```text
0 8 0 8
2 0 0 0
0 0 4 0
2 0 0 0
```

**Train 4 input**
```text
0 3 3 6 7
7 0 0 0 0
3 0 0 0 0
6 0 0 0 0
```

**Train 4 output**
```text
0 0 0 7
3 3 0 0
0 0 6 0
```

**Test input**
```text
0 4 2 4 5 2
2 0 0 0 0 0
4 0 0 0 0 0
5 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 2
4 0 4 0 0
0 0 0 5 0
```

## Replace Each Component by a Checkerboard over Its Bounding Box (`medium_54_checker_fill_bboxes`)

**Difficulty:** medium

**Skills:** bounding boxes, local texture synthesis, parity

**Scaffold notes:**
- Work component by component.
- Replace shape with its bounding box, not its exact outline.
- Use top-left parity to decide which cells stay colored.

**Written solution:** For each connected component, ignore its original internal shape and keep only its bounding box. Refill that box with a checkerboard anchored at the top-left corner of the box: even-parity cells get the component color and odd-parity cells stay black.

**Program solution (Python reference):**
```python
def solve_medium_54_checker_fill_bboxes(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if (r-r0 + c-c0)%2==0:
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Stamp Recolored Copies of the Source Template (`medium_55_recolor_template_stamp`)

**Difficulty:** medium

**Skills:** template extraction, recoloring, translation

**Scaffold notes:**
- Identify the unique color-1 template first.
- Turn the template into a binary footprint.
- Restamp that footprint at each marker in the marker's color.

**Written solution:** The color-1 object is the source template. Ignore its position, keep only its footprint, and at each singleton marker stamp that same footprint with the marker's color, using the marker as the template's top-left corner.

**Program solution (Python reference):**
```python
def solve_medium_55_recolor_template_stamp(g:Grid)->Grid:
    h,w=dims(g)
    # template is the only color-1 component, markers are singletons of colors !=1
    comps=connected_components(g)
    template_comp=None
    markers=[]
    for comp in comps:
        if comp["color"]==1 and len(comp["cells"])>1:
            template_comp=comp
        elif len(comp["cells"])==1:
            markers.append((comp["cells"][0], comp["color"]))
    tmpl=crop_bbox(g,template_comp["bbox"])
    # normalize template to color 1 footprint with zeros preserved
    mask=[[1 if v==1 else 0 for v in row] for row in tmpl]
    out=zeros(h,w,0)
    for (r,c),color in markers:
        pat=[[color if cell==1 else 0 for cell in row] for row in mask]
        paste(out,pat,r,c,transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 2 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 7 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 8 8 0 0 0 2 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 5 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Mark Each Frame with Its Majority Interior Color (`medium_56_frame_majority_centers`)

**Difficulty:** medium

**Skills:** local counting, frames, center placement

**Scaffold notes:**
- Treat each frame independently.
- Count interior colors, ignoring both black and the frame border.
- Write only one summary cell at the center.

**Written solution:** Each 8-colored rectangle is a frame. Count the nonzero interior cells by color, keep the frame itself, and place a single cell of the majority interior color at the frame's center.

**Program solution (Python reference):**
```python
def solve_medium_56_frame_majority_centers(g:Grid)->Grid:
    out=zeros(*dims(g),0)
    for box in frame_boxes_from_color(g,8):
        r0,c0,r1,c1=box
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
        counts=defaultdict(int)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v not in (0,8):
                    counts[v]+=1
        if counts:
            color=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))[0][0]
            cr=(r0+r1)//2; cc=(c0+c1)//2
            out[cr][cc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 8 2 2 0 8 0 8 4 0 0 8 0
0 8 0 0 0 8 0 8 4 0 0 8 0
0 8 0 0 3 8 0 8 0 0 6 8 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 8 0 0 0 8 0 8 0 0 0 8 0
0 8 0 2 0 8 0 8 0 4 0 8 0
0 8 0 0 0 8 0 8 0 0 0 8 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 8 5 0 0 8 0 0 0 0 0 0
0 8 0 5 0 8 0 0 0 0 0 0
0 8 0 0 2 8 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 8 3 3 0 8 0
0 0 0 0 0 0 8 0 3 0 8 0
0 0 0 0 0 0 8 0 0 6 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0
0 8 0 5 0 8 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 0 3 0 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 7 0 7 8 0 0 8 6 0 0 8 0
0 8 0 0 0 8 0 0 8 0 6 0 8 0
0 8 0 4 0 8 0 0 8 2 6 0 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 0 0 0 8 0 0 8 0 0 0 8 0
0 8 0 7 0 8 0 0 8 0 6 0 8 0
0 8 0 0 0 8 0 0 8 0 0 0 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 5 0 8 0 0 0 0 0 0 0
0 8 2 2 0 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 4 0 0 8 0 0 0 0 0 0 0
0 8 0 4 4 8 0 0 0 0 0 0 0
0 8 6 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 0 2 0 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 0 4 0 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 8 3 3 0 8 0 8 6 0 0 8 0
0 8 0 0 0 8 0 8 0 6 0 8 0
0 8 0 0 5 8 0 8 2 6 0 8 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 8 0 0 0 8 0 8 0 0 0 8 0
0 8 0 3 0 8 0 8 0 6 0 8 0
0 8 0 0 0 8 0 8 0 0 0 8 0
0 8 8 8 8 8 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Cast the Keyed Ray inside Each Frame (`hard_50_frame_direction_rays`)

**Difficulty:** hard

**Skills:** frame-local reasoning, direction keys, obstacle-aware casting

**Scaffold notes:**
- Find each frame and solve it separately.
- Read the 1–4 key to choose the ray direction.
- Stop before either a 7 blocker or the border.

**Written solution:** Inside each 8-colored frame there is a direction key (1=up, 2=right, 3=down, 4=left), an emitter 6, and possibly blocker cells 7. Keep the frame, key, emitter, and blockers, then extend a 6-colored ray from the emitter in the keyed direction until the ray would hit a blocker or the frame wall.

**Program solution (Python reference):**
```python
def solve_hard_50_frame_direction_rays(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    dirs={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}
    for box in frame_boxes_from_color(g,8):
        r0,c0,r1,c1=box
        # copy frame and blockers/emitter
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
        emitter=None; key=None
        blockers=[]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v==6:
                    emitter=(r,c)
                    out[r][c]=6
                elif v==7:
                    out[r][c]=7
                elif v in dirs:
                    key=v
                    out[r][c]=v
        dr,dc=dirs[key]
        r,c=emitter
        while True:
            r+=dr; c+=dc
            if not (r0<r<r1 and c0<c<c1):
                break
            if g[r][c]==7:
                break
            if out[r][c] in (0,):
                out[r][c]=6
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 8 2 0 0 0 0 8 0 8 3 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 8 0
0 8 0 0 6 0 7 8 0 8 0 0 6 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 7 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 8 2 0 0 0 0 8 0 8 3 0 0 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 8 0
0 8 0 0 6 6 7 8 0 8 0 0 6 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 7 0 0 8 0
0 8 0 0 0 0 0 8 0 8 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 1 0 7 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 6 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 4 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 7 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 1 0 7 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 6 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 6 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 4 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 7 6 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 2 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 6 0 7 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 1 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 2 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 6 6 7 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 1 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 4 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 7 0 6 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 3 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 4 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 7 6 6 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 3 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 2 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 6 7 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 1 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 2 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 6 7 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 1 0 7 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Decode a Rotation Mosaic from Two Template Libraries (`hard_51_dual_template_rotation_mosaic`)

**Difficulty:** hard

**Skills:** template libraries, rotation codes, mosaic assembly

**Scaffold notes:**
- Separate the two template exemplars from the code grid.
- Decode both template choice and rotation from each code value.
- Expand one code cell into one full tile.

**Written solution:** There are two source templates, one in color 6 and one in color 7. The code grid chooses which template to stamp and how to rotate it: 1–4 mean template 6 rotated by 0°, 90°, 180°, or 270° clockwise; 5–8 mean the same four rotations of template 7. Replace each code cell by the corresponding rotated tile to build the full mosaic.

**Program solution (Python reference):**
```python
def solve_hard_51_dual_template_rotation_mosaic(g:Grid)->Grid:
    comps=connected_components(g)
    t6=max([comp for comp in comps if comp["color"]==6], key=lambda comp: len(comp["cells"]))
    t7=max([comp for comp in comps if comp["color"]==7], key=lambda comp: len(comp["cells"]))
    A=crop_bbox(g,t6["bbox"])
    B=crop_bbox(g,t7["bbox"])
    # code cells are values 1..8 not part of template bboxes
    used=set(t6["cells"])|set(t7["cells"])
    code_cells=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v in range(1,9) and (r,c) not in used]
    r0=min(r for r,c,v in code_cells); c0=min(c for r,c,v in code_cells)
    r1=max(r for r,c,v in code_cells); c1=max(c for r,c,v in code_cells)
    code=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c,v in code_cells:
        code[r-r0][c-c0]=v
    th,tw=dims(A)
    ch,cw=dims(code)
    out=zeros(ch*th, cw*tw, 0)
    for rr in range(ch):
        for cc in range(cw):
            v=code[rr][cc]
            if 1<=v<=4:
                pat=A
                k=v-1
            else:
                pat=B
                k=v-5
            cur=pat
            for _ in range(k):
                cur=rotate_cw(cur)
            paste(out,cur,rr*th,cc*tw,transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 7 7 0 0 0
0 6 0 6 0 0 0 0 0 0 0 7 7 0 0
0 6 6 6 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 5 2 0 0 0 0 0 0 0
0 0 0 0 0 6 3 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6 7 7 0 6 6 6
6 0 6 0 7 7 6 0 6
6 6 6 0 7 0 6 6 6
0 0 7 6 6 6 0 7 0
7 7 7 6 0 6 7 7 7
0 7 0 6 6 6 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 7 0 7 0 0
0 0 6 6 6 0 0 0 0 0 0 7 7 7 0 0
0 0 0 6 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 7 0
6 6 6 7 7 7
0 6 0 7 0 7
0 6 0 7 7 0
6 6 6 0 7 7
0 6 0 7 7 0
7 0 7 0 6 0
7 7 7 6 6 6
0 7 0 0 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 6 6 0 0 0 0 0 0 0 7 0 7 0 0
0 0 6 0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 5 8 0 0 0 0 0 0 0 0
0 0 0 0 0 1 2 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 7 7 7 7 7 7 7
7 0 7 7 0 7 7 0 7
7 7 7 7 7 7 7 7 7
6 6 0 0 0 6 0 6 0
0 6 6 6 6 6 6 6 0
0 6 0 0 6 0 0 6 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 7 0 0 0
0 0 6 6 6 0 0 0 0 0 7 7 7 0 0
0 0 0 6 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 4 1 0 0 0 0 0 0 0 0
0 0 0 0 8 2 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 7 0 6 6 0 6 0 6
7 7 7 0 6 6 6 6 6
0 7 0 6 6 0 0 6 0
0 7 0 0 6 6 0 7 0
7 7 7 6 6 0 7 7 7
0 7 0 0 6 6 0 7 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 7 0 7 0 0
0 6 0 6 0 0 0 0 0 0 0 7 7 7 0 0
0 6 6 6 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 6 6 0 7 7
6 0 6 7 7 0
6 6 6 0 7 7
6 6 6 0 7 0
6 0 6 7 7 7
6 6 6 7 0 7
6 6 6 7 7 0
6 0 6 0 7 7
6 6 6 7 7 0
```

## Compare All Components up to Rotation (`hard_52_shape_similarity_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, rotation invariance, relation matrix

**Scaffold notes:**
- Crop and normalize each component shape.
- Consider all four rotations when testing shape equality.
- Fill a square matrix in component order.

**Written solution:** Order the connected components by reading order. Compare every pair after normalizing their shapes up to rotation. The output is a square relation matrix with 5 on the diagonal and 8 wherever two components have the same shape under some rotation; all other cells stay black.

**Program solution (Python reference):**
```python
def solve_hard_52_shape_similarity_matrix(g:Grid)->Grid:
    comps=connected_components(g)
    comps=sorted(comps,key=lambda comp:(comp["bbox"][0],comp["bbox"][1]))
    canons=[]
    for comp in comps:
        offs=normalize_shape(comp["cells"])
        canons.append(canonical_shape_under_rot(offs))
    n=len(comps)
    out=zeros(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif canons[i]==canons[j]:
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 3 3 0 0 0 0
0 2 0 0 0 0 0 3 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 5 5 0 0 0 0
0 0 4 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
5 8 0 0
8 5 0 0
0 0 5 0
0 0 0 5
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 5 5 5 0 0 0 0
0 4 4 4 0 0 0 0 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 8 0 0
8 5 0 0
0 0 5 8
0 0 8 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 2 2 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 5 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 8 0 0
8 5 0 0
0 0 5 0
0 0 0 5
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 3 3 0 0 0 0
0 2 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 5 5 0 0 0
0 0 0 4 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 8 0 0
8 5 0 0
0 0 5 8
0 0 8 5
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 2 2 0 0 0 0 0 0 3 3 3 0 0 0
0 0 2 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 5 0 5 0 0 0
0 0 4 0 0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 8 0 0
8 5 0 0
0 0 5 0
0 0 0 5
```

## In Each Frame, Choose by Size Rank, Transform, and Recenter (`hard_53_frame_select_rank_center`)

**Difficulty:** hard

**Skills:** local selection, size ranking, conditional rotation, centering

**Scaffold notes:**
- Use the frame to isolate the local puzzle.
- Choose by cell-count rank before doing any transform.
- The border color controls whether a 180° rotation happens.

**Written solution:** Each frame contains a key cell and two candidate components. Key 1 means keep the smaller component; key 2 means keep the larger one. If the frame border is 9, rotate the chosen component by 180°; if the border is 8, keep its orientation. Then center the chosen crop inside the frame interior and erase everything else inside the frame.

**Program solution (Python reference):**
```python
def solve_hard_53_frame_select_rank_center(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w,0)
    for frame_color in (8,9):
        for box in frame_boxes_from_color(g,frame_color):
            r0,c0,r1,c1=box
            # copy frame
            for c in range(c0,c1+1):
                out[r0][c]=frame_color; out[r1][c]=frame_color
            for r in range(r0,r1+1):
                out[r][c0]=frame_color; out[r][c1]=frame_color
            key=None
            interior=zeros(r1-r0-1,c1-c0-1,0)
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    v=g[r][c]
                    if v in (1,2) and key is None:
                        key=v
                    elif v!=0:
                        interior[r-(r0+1)][c-(c0+1)]=v
            comps=connected_components(interior)
            # choose by size
            comps=sorted(comps,key=lambda comp:(len(comp["cells"]),comp["bbox"][0],comp["bbox"][1]))
            chosen=comps[0] if key==1 else comps[-1]
            obj=crop_bbox(interior,chosen["bbox"])
            if frame_color==9:
                obj=rotate_180(obj)
            canvas_h=r1-r0-1; canvas_w=c1-c0-1
            placed=center_place(canvas_h,canvas_w,obj)
            paste(out,placed,r0+1,c0+1,transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 9 9 9 9 9 9 9 0
0 8 1 0 0 0 0 8 0 9 2 0 0 0 0 9 0
0 8 0 3 3 4 4 8 0 9 0 5 0 0 0 9 0
0 8 0 3 0 4 4 8 0 9 0 0 6 0 6 9 0
0 8 0 0 0 4 0 8 0 9 0 0 6 6 6 9 0
0 8 0 0 0 0 0 8 0 9 0 0 0 0 0 9 0
0 8 8 8 8 8 8 8 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 9 9 9 9 9 9 9 0
0 8 0 0 0 0 0 8 0 9 0 0 0 0 0 9 0
0 8 0 3 3 0 0 8 0 9 0 6 6 6 0 9 0
0 8 0 3 0 0 0 8 0 9 0 6 0 6 0 9 0
0 8 0 0 0 0 0 8 0 9 0 0 0 0 0 9 0
0 8 0 0 0 0 0 8 0 9 0 0 0 0 0 9 0
0 8 8 8 8 8 8 8 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 2 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 2 2 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 2 4 4 4 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 4 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 1 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 5 0 7 7 8 0
0 0 0 0 0 0 0 0 0 8 0 0 5 7 7 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 7 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 4 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 4 4 4 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 5 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 2 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 3 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 6 0 6 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 6 6 6 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 9 1 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 4 4 0 7 9 0
0 0 0 0 0 0 0 0 0 0 9 0 4 0 0 7 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 7 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 6 0 6 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 6 6 6 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 4 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 4 4 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 1 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 5 2 2 2 8 0 0 0 0 0 0 0 0 0 0
0 8 0 5 2 0 2 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 2 2 2 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 9 2 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 4 0 6 6 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 4 6 6 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 6 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 5 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 6 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 6 6 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 6 6 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 1 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 3 7 0 7 9 0 0 0 0 0 0 0 0 0
0 9 0 0 7 7 7 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 2 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 4 4 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 4 6 6 6 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 6 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 3 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 9 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 6 6 6 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 6 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Build the Boolean-Operation Gallery of Two Shapes (`hard_54_boolean_ops_panel`)

**Difficulty:** hard

**Skills:** shape masks, set operations, panel composition

**Scaffold notes:**
- Turn both source shapes into binary masks first.
- Apply one boolean operation per panel tile.
- Keep the panel order fixed: union, intersection, A-B, B-A.

**Written solution:** Crop the color-2 shape and the color-3 shape to their own matching bounding boxes and treat them as binary masks. Build a 2×2 panel of color-8 results: top-left union, top-right intersection, bottom-left shape-2 minus shape-3, and bottom-right shape-3 minus shape-2.

**Program solution (Python reference):**
```python
def solve_hard_54_boolean_ops_panel(g:Grid)->Grid:
    comps=connected_components(g)
    A=crop_bbox(g,max([comp for comp in comps if comp["color"]==2], key=lambda comp: len(comp["cells"]))["bbox"])
    B=crop_bbox(g,max([comp for comp in comps if comp["color"]==3], key=lambda comp: len(comp["cells"]))["bbox"])
    h,w=dims(A)
    assert dims(B)==(h,w)
    def mask(grid,color):
        return [[1 if v==color else 0 for v in row] for row in grid]
    ma=mask(A,2); mb=mask(B,3)
    def build(kind):
        out=zeros(h,w,0)
        for r in range(h):
            for c in range(w):
                a=ma[r][c]; b=mb[r][c]
                on=False
                if kind=="union": on=a or b
                elif kind=="inter": on=a and b
                elif kind=="a_minus_b": on=a and not b
                elif kind=="b_minus_a": on=b and not a
                if on: out[r][c]=8
        return out
    tl=build("union"); tr=build("inter"); bl=build("a_minus_b"); br=build("b_minus_a")
    out=zeros(h*2+1,w*2+1,0)
    paste(out,tl,0,0); paste(out,tr,0,w+1); paste(out,bl,h+1,0); paste(out,br,h+1,w+1)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 3 0 0 0
0 2 0 2 0 0 0 0 0 3 3 3 0 0
0 2 2 2 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 0 0 8 0
8 8 8 0 8 0 8
8 8 8 0 0 8 0
0 0 0 0 0 0 0
8 0 8 0 0 0 0
0 0 0 0 0 8 0
8 0 8 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 3 0 3 0 0
0 0 2 2 0 0 0 0 0 3 3 3 0 0
0 0 2 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 0 8 0 0
8 8 8 0 0 8 8
0 8 0 0 0 8 0
0 0 0 0 0 0 0
0 8 0 0 0 0 8
0 0 0 0 8 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 3 3 0 0 0
0 2 2 2 0 0 0 0 0 0 3 3 0 0
0 0 2 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0 0 0 8 0
8 8 8 0 0 8 8
0 8 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
8 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 3 3 3 0 0
0 2 2 2 0 0 0 0 0 3 0 3 0 0
0 0 2 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8 0 8 0 8
8 8 8 0 8 0 8
8 8 8 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 8 0
0 8 0 0 0 0 0
0 0 0 0 8 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 3 3 0 0 0
0 2 0 2 0 0 0 0 0 0 3 3 0 0
0 2 2 2 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8 0 8 8 0
8 8 8 0 0 0 8
8 8 8 0 0 8 0
0 0 0 0 0 0 0
0 0 8 0 0 0 0
8 0 0 0 0 8 0
8 0 8 0 0 0 0
```

## Sort the Components by Hole Count and Pack Them (`hard_55_sort_by_holes`)

**Difficulty:** hard

**Skills:** topology, hole counting, packing

**Scaffold notes:**
- Count enclosed voids, not background regions touching the crop edge.
- Sort by hole count before packing.
- Keep the original component colors and crops.

**Written solution:** Crop each connected component separately and count how many enclosed holes it has. Sort the components by descending hole count and then pack the cropped pieces left to right with one blank column between them.

**Program solution (Python reference):**
```python
def solve_hard_55_sort_by_holes(g:Grid)->Grid:
    comps=connected_components(g)
    pieces=[]
    for comp in comps:
        piece=crop_bbox(g,comp["bbox"])
        holes=component_hole_count(piece)
        pieces.append(( -holes, comp["bbox"][0], comp["bbox"][1], piece))
    pieces.sort()
    pats=[p[-1] for p in pieces]
    H=max(len(p) for p in pats)
    W=sum(len(p[0]) for p in pats)+len(pats)-1
    out=zeros(H,W,0)
    x=0
    for pat in pats:
        paste(out,pat,0,x,transparent=0)
        x+=len(pat[0])+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 4 4 4 0 0 0 0 0 0
0 2 0 2 0 2 0 0 0 4 0 4 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 2 2 0 4 4 4 0 6 6
2 0 2 0 2 0 4 0 4 0 6 0
2 2 2 2 2 0 4 4 4 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 5 5 5 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 5 0 5 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 3 0 5 5 5 0 7 0 7
3 0 0 3 0 5 0 5 0 0 0 0
3 0 0 3 0 5 5 5 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 6 0 0 0 0 2 2 2 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6 6 6 0 8 8 8 0 2 2 2
6 0 6 0 6 0 8 0 8 0 2 2 2
6 6 6 6 6 0 8 8 8 0 2 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 7 7 7 0 4 4 4 0 3 3
7 0 7 0 7 0 4 0 4 0 3 0
7 7 7 7 7 0 4 4 4 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 2 2 2 0 5 5 5 5 0 8 0 8
2 0 2 0 2 0 5 0 0 5 0 0 0 0
2 2 2 2 2 0 5 0 0 5 0 0 0 0
0 0 0 0 0 0 5 5 5 5 0 0 0 0
```

## Transform Each Framed Object and Build a Gallery (`hard_56_frame_transform_gallery`)

**Difficulty:** hard

**Skills:** local extraction, per-frame transform keys, gallery assembly

**Scaffold notes:**
- Solve each frame separately, then assemble globally.
- Read the bottom-right key after cropping the object.
- Center every transformed result inside a 3×3 tile before packing.

**Written solution:** Each 8-colored frame contains one small object and a key in the bottom-right interior cell. The key means identity (1), horizontal flip (2), vertical flip (3), or 90° clockwise rotation (4). Crop the object, apply the keyed transform, center it inside a 3×3 tile, and place the four tiles into a 2×2 gallery in frame reading order.

**Program solution (Python reference):**
```python
def solve_hard_56_frame_transform_gallery(g:Grid)->Grid:
    # frames color 8, 4 frames with 3x3 interior object bbox and one key cell color 1-4 at interior bottom-right
    boxes=sorted(frame_boxes_from_color(g,8), key=lambda box:(box[0],box[1]))
    tiles=[]
    for box in boxes:
        r0,c0,r1,c1=box
        interior=zeros(r1-r0-1,c1-c0-1,0)
        key=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if (r,c)==(r1-1,c1-1):
                    key=v
                else:
                    interior[r-(r0+1)][c-(c0+1)]=v
        # crop object bbox within interior
        cells=nonzero_cells(interior)
        obj=crop_bbox(interior,bbox(cells))
        if key==1:
            trans=obj
        elif key==2:
            trans=flip_h(obj)
        elif key==3:
            trans=flip_v(obj)
        elif key==4:
            trans=rotate_cw(obj)
        else:
            raise ValueError(key)
        # embed in 3x3 tile (or max 3x3)
        tile=zeros(3,3,0)
        oh,ow=dims(trans)
        paste(tile,trans,(3-oh)//2,(3-ow)//2,transparent=0)
        tiles.append(tile)
    out=zeros(3*2+1,3*2+1,0)
    paste(out,tiles[0],0,0); paste(out,tiles[1],0,4); paste(out,tiles[2],4,0); paste(out,tiles[3],4,4)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 2 2 0 8 0 0 8 3 0 0 8 0
0 8 2 0 0 8 0 0 8 3 0 0 8 0
0 8 0 0 1 8 0 0 8 3 3 2 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 4 0 0 8 0 0 8 0 5 5 8 0
0 8 0 4 0 8 0 0 8 0 5 0 8 0
0 8 0 0 3 8 0 0 8 0 0 4 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 0 3 0
2 0 0 0 0 3 0
0 0 0 0 3 3 0
0 0 0 0 0 0 0
0 4 0 0 5 5 0
4 0 0 0 0 5 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 6 0 0 8 0 0 8 0 0 0 8 0
0 8 0 6 0 8 0 0 8 2 2 0 8 0
0 8 0 0 4 8 0 0 8 2 0 3 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 4 0 0 8 0 0 8 0 0 0 8 0
0 8 4 0 0 8 0 0 8 7 0 0 8 0
0 8 4 4 2 8 0 0 8 0 7 1 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 2 0 0
6 0 0 0 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 4 0 0 7 0 0
0 4 0 0 0 7 0
4 4 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 0 3 3 8 0 0 8 5 0 0 8 0
0 8 0 3 0 8 0 0 8 0 5 0 8 0
0 8 0 0 2 8 0 0 8 0 0 4 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 0 0 0 8 0 0 8 2 0 0 8 0
0 8 6 6 0 8 0 0 8 2 0 0 8 0
0 8 6 0 1 8 0 0 8 2 2 3 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 3 0 0 0 5 0
0 3 0 0 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
6 6 0 0 2 2 0
6 0 0 0 2 0 0
0 0 0 0 2 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 7 0 0 8 0 0 8 0 0 0 8 0
0 8 7 0 0 8 0 0 8 4 4 0 8 0
0 8 7 7 3 8 0 0 8 4 0 1 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 0 2 0 8 0 0 8 6 6 0 8 0
0 8 0 0 2 8 0 0 8 6 0 0 8 0
0 8 0 0 2 8 0 0 8 0 0 4 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 0 0 4 4 0
7 0 0 0 4 0 0
7 0 0 0 0 0 0
0 0 0 0 0 0 0
0 2 0 0 6 6 0
2 0 0 0 0 6 0
0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 5 0 0 8 0 0 8 3 0 0 8 0
0 8 0 5 0 8 0 0 8 3 0 0 8 0
0 8 0 0 1 8 0 0 8 3 3 4 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 8 0 0 0 8 0 0 8 0 7 0 8 0
0 8 2 2 0 8 0 0 8 0 0 7 8 0
0 8 2 0 2 8 0 0 8 0 0 3 8 0
0 8 8 8 8 8 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 0 0 0 3 3 3
0 5 0 0 3 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 2 0 0 0 7 0
0 2 0 0 7 0 0
0 0 0 0 0 0 0
```
