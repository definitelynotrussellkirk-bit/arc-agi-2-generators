from __future__ import annotations
import json
from pathlib import Path
from typing import List
import collections

Grid = List[List[int]]

def zeros(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, box):
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    return crop_bbox(g,bbox(cells))

def place(g, pattern, top, left):
    H,W=dims(g)
    h,w=dims(pattern)
    for r in range(h):
        for c in range(w):
            v=pattern[r][c]
            if v!=0:
                rr,cc=top+r,left+c
                if 0<=rr<H and 0<=cc<W:
                    g[rr][cc]=v
    return g

def connected_components(g, colors=None):
    colors=None if colors is None else set(colors)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            q=collections.deque([(r,c)])
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v and (colors is None or v in colors):
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({"color":v, "cells":cells, "bbox":bbox(cells), "area":len(cells)})
    return comps

def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_180(g):
    return [list(reversed(row)) for row in reversed(g)]

def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]

def flip_h(g):
    return [list(reversed(row)) for row in g]

def flip_v(g):
    return list(reversed([row[:] for row in g]))

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=v
            out[2*r+1][2*c]=v
            out[2*r][2*c+1]=v
            out[2*r+1][2*c+1]=v
    return out

def normalize_binary(g):
    return crop_nonzero([[1 if v!=0 else 0 for v in row] for row in g])

def downscale2_if_possible(g):
    h,w=dims(g)
    if h%2 or w%2:
        return None
    out=zeros(h//2,w//2)
    for r in range(0,h,2):
        for c in range(0,w,2):
            vals={g[r+dr][c+dc] for dr in (0,1) for dc in (0,1)}
            if len(vals)!=1:
                return None
            out[r//2][c//2]=next(iter(vals))
    return out

def binary_signature_scale_normalized(g):
    cur=normalize_binary(g)
    # downscale exact 2x repetitions repeatedly
    while True:
        ds=downscale2_if_possible(cur)
        if ds is None:
            break
        cur=normalize_binary([[1 if v!=0 else 0 for v in row] for row in ds])
    return cur

def apply_transform_code(g, code):
    if code==1:
        return [row[:] for row in g]
    if code==2:
        return rotate_cw(g)
    if code==3:
        return rotate_180(g)
    if code==4:
        return rotate_ccw(g)
    if code==5:
        return flip_h(g)
    if code==6:
        return flip_v(g)
    if code==7:
        return transpose(g)
    return [row[:] for row in g]

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

def solve_easy_107_complete_vertical_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[r][w-1-c]=v
    return out

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

def solve_easy_109_left_pack_each_row(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        vals=[v for v in g[r] if v!=0]
        for c,v in enumerate(vals):
            out[r][c]=v
    return out

def solve_easy_110_keep_centers_of_three_cell_lines(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        if comp["area"]==3 and ((r1-r0==0 and c1-c0==2) or (r1-r0==2 and c1-c0==0)):
            out[(r0+r1)//2][(c0+c1)//2]=comp["color"]
    return out

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

def solve_medium_107_transform_and_recolor_object_by_corner_codes(g):
    transform_code=g[0][0]
    target_color=g[0][-1]
    work=clone(g)
    work[0][0]=0
    work[0][-1]=0
    obj=crop_nonzero(work)
    obj=apply_transform_code(obj, transform_code)
    return [[target_color if v!=0 else 0 for v in row] for row in obj]

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

def solve_medium_109_recolor_components_by_area_rank(g):
    h,w=dims(g)
    out=zeros(h,w)
    comps=sorted(connected_components(g), key=lambda comp: (comp["area"], comp["bbox"][0], comp["bbox"][1]))
    palette=[2,4,6,8]
    for comp,new_color in zip(comps, palette):
        for r,c in comp["cells"]:
            out[r][c]=new_color
    return out

def solve_medium_110_select_by_most_frequent_legend_color_and_scale2(g):
    counts=collections.Counter(v for v in g[0] if v!=0)
    key=max(counts.items(), key=lambda kv: (kv[1], -kv[0]))[0]
    work=[row[:] for row in g[1:]]
    candidates=[comp for comp in connected_components(work) if comp["color"]==key]
    comp=max(candidates, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return scale2(crop_bbox(work, comp["bbox"]))

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

def solve_hard_107_build_scale_normalized_shape_equivalence_matrix(g):
    panels=[[row[s:s+6] for row in g] for s in (0,7,14)]
    sigs=[binary_signature_scale_normalized(panel) for panel in panels]
    out=zeros(3,3)
    for i,a in enumerate(sigs):
        for j,b in enumerate(sigs):
            if a==b:
                out[i][j]=8
    return out

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

SOLVERS = {
    "solve_easy_106_fill_row_or_column_spans": solve_easy_106_fill_row_or_column_spans,
    "solve_easy_107_complete_vertical_mirror": solve_easy_107_complete_vertical_mirror,
    "solve_easy_108_reduce_rectangles_to_corners": solve_easy_108_reduce_rectangles_to_corners,
    "solve_easy_109_left_pack_each_row": solve_easy_109_left_pack_each_row,
    "solve_easy_110_keep_centers_of_three_cell_lines": solve_easy_110_keep_centers_of_three_cell_lines,
    "solve_easy_111_fill_component_bounding_boxes": solve_easy_111_fill_component_bounding_boxes,
    "solve_easy_112_cast_rightward_rays_until_blockers": solve_easy_112_cast_rightward_rays_until_blockers,
    "solve_medium_106_crop_the_only_hollow_rectangle": solve_medium_106_crop_the_only_hollow_rectangle,
    "solve_medium_107_transform_and_recolor_object_by_corner_codes": solve_medium_107_transform_and_recolor_object_by_corner_codes,
    "solve_medium_108_apply_gravity_inside_vertical_chambers": solve_medium_108_apply_gravity_inside_vertical_chambers,
    "solve_medium_109_recolor_components_by_area_rank": solve_medium_109_recolor_components_by_area_rank,
    "solve_medium_110_select_by_most_frequent_legend_color_and_scale2": solve_medium_110_select_by_most_frequent_legend_color_and_scale2,
    "solve_medium_111_connect_same_color_pairs_with_ordered_elbows": solve_medium_111_connect_same_color_pairs_with_ordered_elbows,
    "solve_medium_112_pack_component_crops_by_width_ascending": solve_medium_112_pack_component_crops_by_width_ascending,
    "solve_hard_106_build_transform_recolor_cross_product_gallery": solve_hard_106_build_transform_recolor_cross_product_gallery,
    "solve_hard_107_build_scale_normalized_shape_equivalence_matrix": solve_hard_107_build_scale_normalized_shape_equivalence_matrix,
    "solve_hard_108_fill_chambers_by_nearest_seed_manhattan": solve_hard_108_fill_chambers_by_nearest_seed_manhattan,
    "solve_hard_109_select_shape_class_and_apply_transform_sequence": solve_hard_109_select_shape_class_and_apply_transform_sequence,
    "solve_hard_110_overlay_elbow_paths_into_count_map": solve_hard_110_overlay_elbow_paths_into_count_map,
    "solve_hard_111_decode_library_sequence_into_strip": solve_hard_111_decode_library_sequence_into_strip,
    "solve_hard_112_build_pairwise_intersection_gallery": solve_hard_112_build_pairwise_intersection_gallery,
}

def verify_against_bank(json_path: str | Path | None = None):
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_sixteenth_21.json")
    data = json.loads(Path(json_path).read_text())
    mismatches=[]
    for task in data:
        fn = SOLVERS[task["solver_name"]]
        for split in ("train","test"):
            for i,pair in enumerate(task[split]):
                got = fn(pair["input"])
                if got != pair["output"]:
                    mismatches.append((task["id"], split, i))
    return mismatches

if __name__ == "__main__":
    mismatches = verify_against_bank()
    if mismatches:
        print("MISMATCHES:", mismatches)
        raise SystemExit(1)
    print("All tasks verified against the stored bank.")