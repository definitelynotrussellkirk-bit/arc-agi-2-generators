from __future__ import annotations
from typing import List, Tuple, Dict, Callable, Any
from collections import deque, Counter

Grid = List[List[int]]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def zeros(h: int, w: int, val: int = 0) -> Grid:
    return [[val for _ in range(w)] for _ in range(h)]

def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0])

def add_cells(g: Grid, cells: List[Tuple[int, int]], color: int) -> Grid:
    h, w = dims(g)
    for r, c in cells:
        assert 0 <= r < h and 0 <= c < w, (r, c, h, w)
        g[r][c] = color
    return g

def bbox(cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_to_bbox(g: Grid, cells: List[Tuple[int, int]]) -> Grid:
    r0, c0, r1, c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def grid_from_offsets(offsets: List[Tuple[int,int]], color: int = 1) -> Grid:
    if not offsets:
        return [[0]]
    minr = min(r for r,c in offsets)
    minc = min(c for r,c in offsets)
    normed = [(r-minr, c-minc) for r,c in offsets]
    h = max(r for r,c in normed) + 1
    w = max(c for r,c in normed) + 1
    g = zeros(h, w)
    for r,c in normed:
        g[r][c] = color
    return g

def offsets_from_grid(g: Grid, colors: set[int]|None=None) -> List[Tuple[int,int]]:
    cells=[]
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (colors is None or g[r][c] in colors):
                cells.append((r,c))
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0, c-c0) for r,c in cells)

def normalize_offsets(cells: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0, c-c0) for r,c in cells)

def reflect_offsets_vertical(offsets: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    if not offsets:
        return []
    maxc = max(c for r,c in offsets)
    return sorted((r, maxc-c) for r,c in offsets)

def reflect_offsets_horizontal(offsets: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    if not offsets:
        return []
    maxr = max(r for r,c in offsets)
    return sorted((maxr-r, c) for r,c in offsets)

def scale_offsets(offsets: List[Tuple[int,int]], k: int) -> List[Tuple[int,int]]:
    out=[]
    for r,c in offsets:
        for dr in range(k):
            for dc in range(k):
                out.append((r*k+dr, c*k+dc))
    return sorted(out)

def paste(g: Grid, shape: Grid, top: int, left: int, transparent_zero: bool=True) -> Grid:
    h,w=dims(g)
    sh,sw=dims(shape)
    for r in range(sh):
        for c in range(sw):
            val=shape[r][c]
            if transparent_zero and val==0:
                continue
            rr,cc=top+r,left+c
            assert 0 <= rr < h and 0 <= cc < w, (rr,cc,h,w,top,left,sh,sw)
            g[rr][cc]=val
    return g

def centered_top_left(canvas_h: int, canvas_w: int, obj_h: int, obj_w: int) -> Tuple[int,int]:
    return (canvas_h - obj_h)//2, (canvas_w - obj_w)//2

def components4(g: Grid, include_colors: set[int]|None=None, exclude_colors: set[int]|None=None) -> List[Dict[str, Any]]:
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            val=g[r][c]
            if val==0 or seen[r][c]:
                continue
            if include_colors is not None and val not in include_colors:
                continue
            if exclude_colors is not None and val in exclude_colors:
                continue
            q=deque([(r,c)])
            seen[r][c]=True
            cells=[]
            colors=Counter()
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                colors[g[rr][cc]] += 1
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc]!=0:
                        if include_colors is not None and g[nr][nc] not in include_colors:
                            continue
                        if exclude_colors is not None and g[nr][nc] in exclude_colors:
                            continue
                        seen[nr][nc]=True
                        q.append((nr,nc))
            r0,c0,r1,c1=bbox(cells)
            sub=[row[c0:c1+1] for row in g[r0:r1+1]]
            out.append({
                'cells': cells,
                'bbox': (r0,c0,r1,c1),
                'h': r1-r0+1,
                'w': c1-c0+1,
                'area': len(cells),
                'colors': dict(colors),
                'subgrid': sub,
                'norm_cells': normalize_offsets(cells),
            })
    return out

def is_h_symmetric(offsets: List[Tuple[int,int]]) -> bool:
    return sorted(offsets) == reflect_offsets_horizontal(offsets)

def is_v_symmetric(offsets: List[Tuple[int,int]]) -> bool:
    return sorted(offsets) == reflect_offsets_vertical(offsets)

def rotate_grid_cw(g: Grid) -> Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def recolor_nonzero(g: Grid, color: int) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=color
    return out

def is_full_rect_border(g: Grid, cells: List[Tuple[int,int]], color: int) -> bool:
    r0,c0,r1,c1=bbox(cells)
    expected=set()
    for c in range(c0,c1+1):
        expected.add((r0,c)); expected.add((r1,c))
    for r in range(r0,r1+1):
        expected.add((r,c0)); expected.add((r,c1))
    return set(cells)==expected and all(g[r][c]==color for r,c in expected)

def center_paste_inside_box(out: Grid, shape: Grid, box: Tuple[int,int,int,int], color: int|None=None):
    r0,c0,r1,c1=box
    interior_h = r1-r0+1
    interior_w = c1-c0+1
    sg=shape
    if color is not None:
        sg=recolor_nonzero(shape,color)
    sh,sw=dims(sg)
    top = r0 + (interior_h - sh)//2
    left = c0 + (interior_w - sw)//2
    paste(out, sg, top, left)

def apply_op_to_template(g: Grid, key: int) -> Grid:
    tg=clone(g)
    op=STRIP_KEY_OPS[key]
    if op=='id':
        return tg
    if op=='rot90':
        return rotate_grid_cw(tg)
    if op=='rot180':
        return rotate_grid_cw(rotate_grid_cw(tg))
    if op=='flipv':
        h,w=dims(tg)
        return [list(reversed(row)) for row in tg]
    raise ValueError(key)

ROT_KEY = {2:0, 3:1, 4:2, 5:3}
LOCAL_ROT_KEY = {2:0, 3:1, 4:2, 5:3}
STRIP_KEY_OPS = {2:'id',3:'rot90',4:'rot180',5:'flipv'}

def solve_easy_22_recolor_exact_pluses(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    centers=[]
    for r in range(1, h-1):
        for c in range(1, w-1):
            if g[r][c]==3 and g[r-1][c]==3 and g[r+1][c]==3 and g[r][c-1]==3 and g[r][c+1]==3:
                centers.append((r,c))
    for r,c in centers:
        for rr,cc in [(r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
            out[rr][cc]=7
    return out

def solve_easy_23_fill_hollow_ring_centers(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            ok=True
            for dr in range(3):
                for dc in range(3):
                    rr,cc=r+dr,c+dc
                    if dr==1 and dc==1:
                        if g[rr][cc]!=0:
                            ok=False
                    else:
                        if g[rr][cc]!=1:
                            ok=False
            if ok:
                out[r+1][c+1]=2
    return out

def solve_easy_24_bridge_single_horizontal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==6 and g[r][c+1]==6:
                if c-2 < 0 or g[r][c-2] != 6:
                    if c+2 >= w or g[r][c+2] != 6:
                        out[r][c]=8
    return out

def solve_easy_25_complete_descending_diagonal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c]==4 and g[r+1][c+1]==0 and g[r+2][c+2]==4:
                if (r-1 < 0 or c-1 < 0 or g[r-1][c-1] != 4) and (r+3 >= h or c+3 >= w or g[r+3][c+3] != 4):
                    out[r+1][c+1]=4
    return out

def solve_easy_26_complete_2x2_from_l(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            cells=[g[r+dr][c+dc] for dr in range(2) for dc in range(2)]
            if cells.count(5)==3 and cells.count(0)==1:
                for dr in range(2):
                    for dc in range(2):
                        if g[r+dr][c+dc]==0:
                            out[r+dr][c+dc]=5
    return out

def solve_easy_27_recolor_exact_2x3_rectangles(g: Grid) -> Grid:
    out = clone(g)
    comps = components4(g, include_colors={2})
    for comp in comps:
        r0,c0,r1,c1 = comp['bbox']
        h = comp['h']; w = comp['w']; area = comp['area']
        if area == 6 and ((h==2 and w==3) or (h==3 and w==2)):
            # ensure full rectangle
            full=True
            for rr in range(r0,r1+1):
                for cc in range(c0,c1+1):
                    if g[rr][cc] != 2:
                        full=False
            if full:
                for rr,cc in comp['cells']:
                    out[rr][cc]=8
    return out

def solve_easy_28_mirror_singletons_across_horizontal_midline(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==7:
                mr = h-1-r
                out[mr][c] = 7
    return out

def solve_medium_22_gravity_down_each_column(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,val in enumerate(vals):
            out[start+i][c]=val
    return out

def solve_medium_23_connect_aligned_pairs(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors = sorted({g[r][c] for r in range(h) for c in range(w) if g[r][c] != 0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2:
                for c in range(min(c1,c2), max(c1,c2)+1):
                    out[r1][c]=color
            elif c1==c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    out[r][c1]=color
    return out

def solve_medium_24_keep_only_even_area_components(g: Grid) -> Grid:
    out=zeros(*dims(g))
    for comp in components4(g):
        if comp['area'] % 2 == 0:
            for r,c in comp['cells']:
                out[r][c]=g[r][c]
    return out

def solve_medium_25_rotate_template_by_key_and_center(g: Grid) -> Grid:
    h,w=dims(g)
    # template is all color 1 cells
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    assert cells
    r0,c0,r1,c1=bbox(cells)
    templ=[row[c0:c1+1] for row in g[r0:r1+1]]
    # trim to color1 only
    templ=[[1 if cell==1 else 0 for cell in row] for row in templ]
    key=[g[r][c] for r in range(h) for c in range(w) if g[r][c] in ROT_KEY]
    assert len(key)==1
    k=ROT_KEY[key[0]]
    tg=templ
    for _ in range(k):
        tg=rotate_grid_cw(tg)
    out=zeros(h,w)
    th,tw=dims(tg)
    top,left=centered_top_left(h,w,th,tw)
    paste(out,tg,top,left)
    return out

def solve_medium_26_crop_and_stack_components_vertically_by_area(g: Grid) -> Grid:
    comps=components4(g)
    comps_sorted=sorted(comps, key=lambda comp: (comp['area'], comp['bbox'][0], comp['bbox'][1]))
    crops=[]
    maxw=0
    for comp in comps_sorted:
        crop=crop_to_bbox(g, comp['cells'])
        crops.append(crop)
        maxw=max(maxw, len(crop[0]))
    totalh=sum(len(crop) for crop in crops) + max(0, len(crops)-1)
    out=zeros(totalh, maxw)
    r=0
    for i,crop in enumerate(crops):
        paste(out,crop,r,0)
        r += len(crop)
        if i < len(crops)-1:
            r += 1
    return out

def solve_medium_27_place_cross_at_bbox_center(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for comp in components4(g):
        color=max(comp['colors'], key=lambda k: comp['colors'][k])
        r0,c0,r1,c1=comp['bbox']
        bh, bw = comp['h'], comp['w']
        assert bh % 2 == 1 and bw % 2 == 1
        cr = (r0+r1)//2
        cc = (c0+c1)//2
        for rr,cc2 in [(cr,cc),(cr-1,cc),(cr+1,cc),(cr,cc-1),(cr,cc+1)]:
            out[rr][cc2]=color
    return out

def solve_medium_28_fill_component_bboxes_with_key_color(g: Grid) -> Grid:
    h,w=dims(g)
    # key is unique singleton of color not 6
    key_cells=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=6]
    key_colors=[clr for r,c,clr in key_cells]
    assert len(key_colors)>=1
    # choose singleton color occurring once and not 6
    cnt=Counter(key_colors)
    key=[clr for clr,n in cnt.items() if n==1][0]
    out=zeros(h,w)
    for comp in components4(g, include_colors={6}):
        r0,c0,r1,c1=comp['bbox']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=key
    return out

def solve_hard_22_local_key_rotate_template_inside_frames(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    # template
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[1 if cell==1 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    # preserve frames and keys
    for r in range(h):
        for c in range(w):
            if g[r][c] in {7,2,3,4,5}:
                out[r][c]=g[r][c]
    # detect color7 frame components
    for comp in components4(g, include_colors={7}):
        if not is_full_rect_border(g, comp['cells'], 7):
            continue
        fr0,fc0,fr1,fc1 = comp['bbox']
        # key inside frame
        key_cells=[(r,c,g[r][c]) for r in range(fr0+1, fr1) for c in range(fc0+1, fc1) if g[r][c] in LOCAL_ROT_KEY]
        assert len(key_cells)==1
        _,_,key=key_cells[0]
        tg=templ
        for _ in range(LOCAL_ROT_KEY[key]):
            tg=rotate_grid_cw(tg)
        center_paste_inside_box(out, tg, (fr0+1,fc0+1,fr1-1,fc1-1), color=key)
    return out

def solve_hard_23_make_transform_strip_from_template_and_three_keys(g: Grid) -> Grid:
    h,w=dims(g)
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[1 if cell==1 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    keys=sorted([(c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in STRIP_KEY_OPS])
    assert len(keys)==3
    pieces=[]
    maxh=0
    for _,key in keys:
        piece=apply_op_to_template(templ,key)
        piece=recolor_nonzero(piece,key)
        pieces.append(piece)
        maxh=max(maxh,len(piece))
    totalw=sum(len(piece[0]) for piece in pieces)+2
    out=zeros(maxh,totalw)
    c=0
    for i,piece in enumerate(pieces):
        paste(out,piece,0,c)
        c += len(piece[0])
        if i < len(pieces)-1:
            c += 1
    return out

def solve_hard_24_stamp_template_at_every_mask_cell(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[8 if cell==2 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    mask_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3]
    for r,c in mask_cells:
        paste(out,templ,r,c)
    return out

def solve_hard_25_bar_chart_component_areas_by_color(g: Grid) -> Grid:
    comps=components4(g)
    area_by_color={}
    for comp in comps:
        # assume single-color comp
        color=max(comp['colors'], key=lambda k: comp['colors'][k])
        area_by_color[color]=comp['area']
    colors=sorted(area_by_color)
    maxw=max(area_by_color.values())
    out=zeros(len(colors), maxw)
    for r,color in enumerate(colors):
        for c in range(area_by_color[color]):
            out[r][c]=color
    return out

def solve_hard_26_stamp_unique_bisymmetric_component_at_markers(g: Grid) -> Grid:
    h,w=dims(g)
    comps=components4(g, include_colors={1})
    sym=[]
    for comp in comps:
        off=comp['norm_cells']
        if is_h_symmetric(off) and is_v_symmetric(off):
            sym.append(comp)
    assert len(sym)==1
    comp=sym[0]
    base=crop_to_bbox(g, comp['cells'])
    # recolor later
    bh,bw=dims(base)
    assert bh % 2 == 1 and bw % 2 == 1
    out=zeros(h,w)
    markers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in {2,3,4,5}]
    for r,c,color in markers:
        top = r - bh//2
        left = c - bw//2
        piece=recolor_nonzero(base,color)
        paste(out,piece,top,left)
    return out

def solve_hard_27_frame_local_intersections_with_fill_key(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    # preserve all nonzero input
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[r][c]=g[r][c]
    for comp in components4(g, include_colors={7}):
        if not is_full_rect_border(g, comp['cells'], 7):
            continue
        r0,c0,r1,c1=comp['bbox']
        row_marks=[r for r in range(r0+1,r1) if g[r][c0+1]==2]
        col_marks=[c for c in range(c0+1,c1) if g[r0+1][c]==3]
        key_cells=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in {0,2,3}]
        # one fill key inside
        assert len(key_cells)>=1
        fill=Counter(key_cells).most_common(1)[0][0]
        for r in row_marks:
            for c in col_marks:
                out[r][c]=fill
    return out

def solve_hard_28_select_by_marker_count_scale_and_center(g: Grid) -> Grid:
    h,w=dims(g)
    comps=components4(g, include_colors={1})
    comps=sorted(comps, key=lambda comp: (comp['area'], comp['bbox'][0], comp['bbox'][1]))
    n_markers=sum(1 for r in range(h) for c in range(w) if g[r][c]==9)
    idx=n_markers-1
    comp=comps[idx]
    crop=crop_to_bbox(g, comp['cells'])
    # scale 2x and recolor 8
    offsets=offsets_from_grid(crop,{1})
    scaled=scale_offsets(offsets,2)
    out=grid_from_offsets(scaled, 8)
    return out

SOLVERS: Dict[str, Callable[[Grid], Grid]] = {
    "easy_22_recolor_exact_pluses": solve_easy_22_recolor_exact_pluses,
    "easy_23_fill_hollow_ring_centers": solve_easy_23_fill_hollow_ring_centers,
    "easy_24_bridge_single_horizontal_gaps": solve_easy_24_bridge_single_horizontal_gaps,
    "easy_25_complete_descending_diagonal_gaps": solve_easy_25_complete_descending_diagonal_gaps,
    "easy_26_complete_2x2_from_l": solve_easy_26_complete_2x2_from_l,
    "easy_27_recolor_exact_2x3_rectangles": solve_easy_27_recolor_exact_2x3_rectangles,
    "easy_28_mirror_singletons_across_horizontal_midline": solve_easy_28_mirror_singletons_across_horizontal_midline,
    "medium_22_gravity_down_each_column": solve_medium_22_gravity_down_each_column,
    "medium_23_connect_aligned_pairs": solve_medium_23_connect_aligned_pairs,
    "medium_24_keep_only_even_area_components": solve_medium_24_keep_only_even_area_components,
    "medium_25_rotate_template_by_key_and_center": solve_medium_25_rotate_template_by_key_and_center,
    "medium_26_crop_and_stack_components_vertically_by_area": solve_medium_26_crop_and_stack_components_vertically_by_area,
    "medium_27_place_cross_at_bbox_center": solve_medium_27_place_cross_at_bbox_center,
    "medium_28_fill_component_bboxes_with_key_color": solve_medium_28_fill_component_bboxes_with_key_color,
    "hard_22_local_key_rotate_template_inside_frames": solve_hard_22_local_key_rotate_template_inside_frames,
    "hard_23_make_transform_strip_from_template_and_keys": solve_hard_23_make_transform_strip_from_template_and_three_keys,
    "hard_24_stamp_template_at_every_mask_cell": solve_hard_24_stamp_template_at_every_mask_cell,
    "hard_25_bar_chart_component_areas_by_color": solve_hard_25_bar_chart_component_areas_by_color,
    "hard_26_stamp_unique_bisymmetric_component_at_markers": solve_hard_26_stamp_unique_bisymmetric_component_at_markers,
    "hard_27_frame_local_intersections_with_fill_key": solve_hard_27_frame_local_intersections_with_fill_key,
    "hard_28_select_by_marker_count_scale_and_center": solve_hard_28_select_by_marker_count_scale_and_center,
}

def verify_bank(bank: List[dict]) -> None:
    for task in bank:
        solver = SOLVERS[task["id"]]
        for split in ("train", "test"):
            for i, example in enumerate(task[split]):
                got = solver(example["input"])
                exp = example["output"]
                if got != exp:
                    raise AssertionError(f'{task["id"]} {split}[{i}] mismatch')
    print(f"verified {len(bank)} tasks")

if __name__ == "__main__":
    import json
    from pathlib import Path
    bank_path = Path(__file__).with_name("arc_puzzle_bank_fourth_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
