from __future__ import annotations

import json

from pathlib import Path

from typing import List, Tuple

from collections import deque, defaultdict



Grid = List[List[int]]



def clone(g: Grid) -> Grid:
    return [row[:] for row in g]



def zeros(h:int,w:int,val:int=0)->Grid:
    return [[val for _ in range(w)] for _ in range(h)]



def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0])



def paste(g:Grid, pat:Grid, top:int,left:int, transparent:int=0)->Grid:
    h,w=dims(g); ph,pw=dims(pat)
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                assert 0<=rr<h and 0<=cc<w
                g[rr][cc]=v
    return g



def bbox(cells:Iterable[Tuple[int,int]])->Tuple[int,int,int,int]:
    cells=list(cells)
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)



def crop_bbox(g:Grid, box:Tuple[int,int,int,int])->Grid:
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]



def normalize_offsets(cells:Iterable[Tuple[int,int]])->List[Tuple[int,int]]:
    cells=list(cells)
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)



def offsets_to_grid(offsets:Iterable[Tuple[int,int]], color:int=1)->Grid:
    offsets=list(offsets)
    if not offsets:
        return [[0]]
    r0,c0,r1,c1=bbox(offsets)
    g=zeros(r1-r0+1,c1-c0+1,0)
    for r,c in offsets:
        g[r-r0][c-c0]=color
    return g



def rotate_grid_cw(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]



def rotate_grid_180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]



def flip_horizontal(g:Grid)->Grid:
    return [row[::-1] for row in g]



def rotate_offsets_cw(offsets:List[Tuple[int,int]])->List[Tuple[int,int]]:
    if not offsets:
        return []
    g=offsets_to_grid(offsets,1)
    rg=rotate_grid_cw(g)
    return [(r,c) for r,row in enumerate(rg) for c,v in enumerate(row) if v]



def components4_color(g:Grid, color:int)->List[List[Tuple[int,int]]]:
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=color or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); comp=[]
            while q:
                rr,cc=q.popleft(); comp.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]==color and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            out.append(comp)
    return out



def components4_any(g:Grid)->List[List[Tuple[int,int]]]:
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); comp=[]
            while q:
                rr,cc=q.popleft(); comp.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]!=0 and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            out.append(comp)
    return out



def component_perimeter(comp:Set[Tuple[int,int]])->int:
    s=set(comp)
    p=0
    for r,c in s:
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            if (r+dr,c+dc) not in s:
                p+=1
    return p



def draw_rect(g:Grid, top:int,left:int,h:int,w:int,color:int,border_only=False):
    for r in range(top, top+h):
        for c in range(left, left+w):
            if border_only:
                if r in (top, top+h-1) or c in (left, left+w-1):
                    g[r][c]=color
            else:
                g[r][c]=color
    return g



def rect_border_cells(top,left,h,w):
    cells=[]
    for r in range(top, top+h):
        for c in range(left, left+w):
            if r in (top, top+h-1) or c in (left, left+w-1):
                cells.append((r,c))
    return cells



def gallery_h(crops:List[Grid], sep:int=1)->Grid:
    if not crops:
        return [[0]]
    h=max(len(c) for c in crops)
    w=sum(len(c[0]) for c in crops)+sep*(len(crops)-1)
    out=zeros(h,w,0); x=0
    for crop in crops:
        paste(out,crop,0,x,0)
        x+=len(crop[0])+sep
    return out



def canonical_shape_rotations(cells:Iterable[Tuple[int,int]])->Tuple[Tuple[Tuple[int,int],...],...]:
    offs=normalize_offsets(cells)
    variants=[]
    cur=offs
    for _ in range(4):
        variants.append(tuple(normalize_offsets(cur)))
        cur=rotate_offsets_cw(cur)
    return tuple(sorted(set(variants)))



def shape_match_under_rotation(cells1, cells2)->bool:
    return tuple(normalize_offsets(cells2)) in canonical_shape_rotations(cells1)



def ray_diag_until_block(g:Grid,start:Tuple[int,int],dr:int,dc:int,blockers:set[int],include_start=False,bounds=None):
    h,w=dims(g); r,c=start; out=[]
    if include_start:
        if bounds is None or (bounds[0]<=r<=bounds[2] and bounds[1]<=c<=bounds[3]):
            out.append((r,c))
    rr,cc=r+dr,c+dc
    while 0<=rr<h and 0<=cc<w:
        if bounds is not None:
            r0,c0,r1,c1=bounds
            if not (r0<=rr<=r1 and c0<=cc<=c1): break
        if g[rr][cc] in blockers: break
        out.append((rr,cc))
        rr += dr; cc += dc
    return out



def elbow_path(a:Tuple[int,int], b:Tuple[int,int], prefer='vertical_first')->List[Tuple[int,int]]:
    r1,c1=a; r2,c2=b
    cells=[]
    if prefer=='vertical_first':
        step = 1 if r2>=r1 else -1
        for r in range(r1, r2+step, step):
            cells.append((r,c1))
        step = 1 if c2>=c1 else -1
        for c in range(c1, c2+step, step):
            cells.append((r2,c))
    else:
        step = 1 if c2>=c1 else -1
        for c in range(c1, c2+step, step):
            cells.append((r1,c))
        step = 1 if r2>=r1 else -1
        for r in range(r1, r2+step, step):
            cells.append((r,c2))
    # unique preserve order
    seen=set(); out=[]
    for cell in cells:
        if cell not in seen:
            seen.add(cell); out.append(cell)
    return out



def frame_boxes_from_color(g:Grid, color:int=5):
    boxes=[]
    for comp in components4_color(g,color):
        r0,c0,r1,c1 = bbox(comp)
        expected=set(rect_border_cells(r0,c0,r1-r0+1,c1-c0+1))
        if set(comp)==expected and r1-r0+1>=3 and c1-c0+1>=3:
            boxes.append((r0,c0,r1,c1))
    return sorted(boxes)



def inside(box):
    r0,c0,r1,c1=box
    return r0+1,c0+1,r1-1,c1-1



def transform_by_key_grid(g:Grid,key:int)->Grid:
    if key==1: return clone(g)
    if key==2: return rotate_grid_cw(g)
    if key==3: return rotate_grid_180(g)
    if key==4: return flip_horizontal(g)
    raise ValueError(key)



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



def solve_easy_37_replace_components_by_bboxes(g: Grid) -> Grid:
    out = zeros(*dims(g), 0)
    for comp in components4_any(g):
        r0,c0,r1,c1 = bbox(comp)
        draw_rect(out, r0, c0, r1-r0+1, c1-c0+1, 8, border_only=True)
    return out



def solve_easy_38_keep_bottommost_component(g: Grid) -> Grid:
    comps = components4_any(g)
    best = max(comps, key=lambda comp: (bbox(comp)[2], bbox(comp)[0], -bbox(comp)[1]))
    out = zeros(*dims(g),0)
    for r,c in best:
        out[r][c] = g[r][c]
    return out



def solve_easy_39_crop_tallest_component(g: Grid) -> Grid:
    comps = components4_any(g)
    best = max(comps, key=lambda comp: ((bbox(comp)[2]-bbox(comp)[0]+1), len(comp), -bbox(comp)[1]))
    return crop_bbox(g, bbox(best))



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



def solve_easy_42_component_colors_by_top_order(g: Grid) -> Grid:
    comps = components4_any(g)
    ordered = sorted(comps, key=lambda comp: (bbox(comp)[0], bbox(comp)[1]))
    colors = [g[comp[0][0]][comp[0][1]] for comp in ordered]
    return [colors]



def solve_medium_36_perimeter_sorted_gallery(g: Grid) -> Grid:
    comps = components4_any(g)
    decorated = []
    for comp in comps:
        crop = crop_bbox(g, bbox(comp))
        decorated.append((component_perimeter(set(comp)), bbox(comp)[0], bbox(comp)[1], crop))
    decorated.sort(key=lambda x: (-x[0], x[1], x[2]))
    crops = [crop for _,_,_,crop in decorated]
    return gallery_h(crops, sep=1)



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



def solve_medium_41_color_equality_matrix(g: Grid) -> Grid:
    top = [v for v in g[0][1:] if v != 0 or True]  # allow zeros? legends will be nonzero
    left = [g[r][0] for r in range(1,len(g))]
    return [[rowc if rowc == colc else 0 for colc in top] for rowc in left]



def solve_medium_42_crop_union_of_key_components(g: Grid) -> Grid:
    keys = [v for v in g[0] if v != 0][:2]
    body = [row[:] for row in g[2:]]
    selected_cells = []
    for color in keys:
        comps = components4_color(body, color)
        assert len(comps)==1
        selected_cells.extend(comps[0])
    return crop_bbox(body, bbox(selected_cells))



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



SOLVERS = {

    "easy_36_diagonal_rays_from_seeds": solve_easy_36_diagonal_rays_from_seeds,

    "easy_37_replace_components_by_bboxes": solve_easy_37_replace_components_by_bboxes,

    "easy_38_keep_bottommost_component": solve_easy_38_keep_bottommost_component,

    "easy_39_crop_tallest_component": solve_easy_39_crop_tallest_component,

    "easy_40_fill_between_vertical_markers": solve_easy_40_fill_between_vertical_markers,

    "easy_41_stamp_x_at_markers": solve_easy_41_stamp_x_at_markers,

    "easy_42_component_colors_by_top_order": solve_easy_42_component_colors_by_top_order,

    "medium_36_perimeter_sorted_gallery": solve_medium_36_perimeter_sorted_gallery,

    "medium_37_elbow_connect_pairs": solve_medium_37_elbow_connect_pairs,

    "medium_38_legend_ordered_component_gallery": solve_medium_38_legend_ordered_component_gallery,

    "medium_39_fill_tallest_ring_with_key": solve_medium_39_fill_tallest_ring_with_key,

    "medium_40_drop_whole_components": solve_medium_40_drop_whole_components,

    "medium_41_color_equality_matrix": solve_medium_41_color_equality_matrix,

    "medium_42_crop_union_of_key_components": solve_medium_42_crop_union_of_key_components,

    "hard_36_local_diagonal_rays_in_frames": solve_hard_36_local_diagonal_rays_in_frames,

    "hard_37_boolean_panel_from_two_templates": solve_hard_37_boolean_panel_from_two_templates,

    "hard_38_shifted_overlay_count_map": solve_hard_38_shifted_overlay_count_map,

    "hard_39_local_object_gravity_in_frames": solve_hard_39_local_object_gravity_in_frames,

    "hard_40_shape_color_relation_matrix": solve_hard_40_shape_color_relation_matrix,

    "hard_41_legend_ordered_transformed_gallery": solve_hard_41_legend_ordered_transformed_gallery,

    "hard_42_chamber_elbow_paths": solve_hard_42_chamber_elbow_paths,

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
    bank_path = Path(__file__).with_name("arc_puzzle_bank_sixth_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
