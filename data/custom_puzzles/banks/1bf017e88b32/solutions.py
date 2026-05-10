from __future__ import annotations
import collections
from typing import List, Tuple

Grid = List[List[int]]

def zeros(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, box):
    r0,c0,r1,c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))

def hflip(g):
    return [list(reversed(row)) for row in g]

def vflip(g):
    return list(reversed([row[:] for row in g]))

def rot90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g):
    return rot90(rot90(g))

def rot270(g):
    return rot90(rot180(g))

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def scale2(g):
    out=[]
    for row in g:
        exp=[]
        for v in row:
            exp.extend([v,v])
        out.append(exp[:])
        out.append(exp[:])
    return out

def colorize(mask, color):
    return [[color if v else 0 for v in row] for row in mask]

def stamp(g, obj, top, left, transparent=0):
    H,W=dims(g)
    h,w=dims(obj)
    for r in range(h):
        for c in range(w):
            v=obj[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                if 0<=rr<H and 0<=cc<W:
                    g[rr][cc]=v
    return g

def count_stamp(counts, obj, top, left, transparent=0):
    H,W=dims(counts)
    h,w=dims(obj)
    for r in range(h):
        for c in range(w):
            v=obj[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                if 0<=rr<H and 0<=cc<W:
                    counts[rr][cc]+=1
    return counts

def normalize_binary(g):
    cg = crop_nonzero(g)
    return [[1 if v!=0 else 0 for v in row] for row in cg]

def connected_components(g, colors=None, ignore_positions=None):
    colors=None if colors is None else set(colors)
    ignore_positions=set() if ignore_positions is None else set(ignore_positions)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in ignore_positions:
                seen[r][c]=True
                continue
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            dq=collections.deque([(r,c)])
            cells=[]
            while dq:
                rr,cc=dq.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and (nr,nc) not in ignore_positions:
                        if g[nr][nc]==v and (colors is None or v in colors):
                            seen[nr][nc]=True
                            dq.append((nr,nc))
            comps.append({"color": v, "cells": cells, "bbox": bbox(cells), "area": len(cells)})
    return comps

def object_crop_from_component(g, comp):
    return crop_bbox(g, comp["bbox"])

def same_under_rotation(a,b):
    na=normalize_binary(a)
    cur=normalize_binary(b)
    for _ in range(4):
        if na==normalize_binary(cur):
            return True
        cur=rot90(cur)
    return False

def same_under_dihedral(a,b):
    na=normalize_binary(a)
    cur=normalize_binary(b)
    cands=[]
    tmp=cur
    for _ in range(4):
        cands.append(tmp)
        cands.append(hflip(tmp))
        tmp=rot90(tmp)
    return any(na==normalize_binary(x) for x in cands)

def hole_count(obj):
    mask=[[1 if v!=0 else 0 for v in row] for row in crop_nonzero(obj)]
    h,w=dims(mask)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0 or seen[r][c]:
                continue
            seen[r][c]=True
            dq=collections.deque([(r,c)])
            touches_border=False
            while dq:
                rr,cc=dq.popleft()
                if rr in (0,h-1) or cc in (0,w-1):
                    touches_border=True
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and mask[nr][nc]==0:
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            if not touches_border:
                holes+=1
    return holes

def is_horiz_symmetric(obj):
    cg=crop_nonzero(obj)
    return cg==hflip(cg)

def is_vert_symmetric(obj):
    cg=crop_nonzero(obj)
    return cg==vflip(cg)

def apply_transform_code(obj, code):
    if code==1:
        return clone(obj)
    if code==2:
        return rot90(obj)
    if code==3:
        return rot180(obj)
    if code==4:
        return rot270(obj)
    if code==5:
        return hflip(obj)
    if code==6:
        return vflip(obj)
    if code==7:
        return transpose(obj)
    raise ValueError(code)

def recolor_object(obj, color):
    return [[color if v!=0 else 0 for v in row] for row in obj]

def monotone_stair_path(p0, p1):
    r,c = p0
    tr,tc = p1
    path=[(r,c)]
    while (r,c)!=(tr,tc):
        if r!=tr:
            r += 1 if tr>r else -1
            path.append((r,c))
        if c!=tc:
            c += 1 if tc>c else -1
            path.append((r,c))
    return path

def gallery_row(objs, gap=1):
    h=max(len(o) for o in objs)
    w=sum(len(o[0]) for o in objs)+gap*(len(objs)-1)
    out=zeros(h,w)
    c=0
    for i,obj in enumerate(objs):
        stamp(out,obj,0,c)
        c += len(obj[0])
        if i+1 < len(objs):
            c += gap
    return out

def gallery_grid(panels, gap=1):
    # panels: list of rows, each row is list of equally-dimensioned grids
    ph = max(len(p) for row in panels for p in row)
    pw = max(len(p[0]) for row in panels for p in row)
    rows = len(panels)
    cols = len(panels[0])
    out = zeros(rows*ph + gap*(rows-1), cols*pw + gap*(cols-1))
    for rr,row in enumerate(panels):
        for cc,p in enumerate(row):
            top = rr*(ph+gap)
            left = cc*(pw+gap)
            stamp(out,p,top,left)
    return out

def encode_count_map(counts):
    h,w=dims(counts)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            k=counts[r][c]
            if k<=0:
                out[r][c]=0
            else:
                out[r][c]=min(k+1,9)
    return out

def flood_region_within(g, start, wall_color, row_min=0):
    h,w=dims(g)
    sr,sc=start
    if not (row_min <= sr < h and 0 <= sc < w):
        return set()
    if g[sr][sc]==wall_color:
        return set()
    dq=collections.deque([start])
    seen={start}
    while dq:
        r,c=dq.popleft()
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=r+dr,c+dc
            if row_min <= nr < h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=wall_color:
                seen.add((nr,nc))
                dq.append((nr,nc))
    return seen

def solve_easy_113_complete_horizontal_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[h-1-r][c]=v
    return out

def solve_easy_114_draw_rectangle_borders_from_opposite_corners(g):
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
        rlo,rhi=min(r0,r1),max(r0,r1)
        clo,chi=min(c0,c1),max(c0,c1)
        for c in range(clo,chi+1):
            out[rlo][c]=color
            out[rhi][c]=color
        for r in range(rlo,rhi+1):
            out[r][clo]=color
            out[r][chi]=color
    return out

def solve_easy_115_top_pack_each_column(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for r,v in enumerate(vals):
            out[r][c]=v
    return out

def solve_easy_116_fill_diagonal_segments(g):
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
        dr = 1 if r1>r0 else -1
        dc = 1 if c1>c0 else -1
        if abs(r1-r0)==abs(c1-c0):
            steps=abs(r1-r0)
            for k in range(steps+1):
                out[r0+dr*k][c0+dc*k]=color
    return out

def solve_easy_117_crop_largest_object(g):
    comps=connected_components(g)
    comp=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return object_crop_from_component(g, comp)

def solve_easy_118_turn_filled_rectangles_into_frames(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
    return out

def solve_easy_119_keep_centers_of_odd_squares(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        hh=r1-r0+1
        ww=c1-c0+1
        if hh==ww and hh%2==1:
            out[r0+hh//2][c0+ww//2]=color
    return out

def solve_medium_113_select_object_by_legend_and_transform(g):
    h,w=dims(g)
    key=g[0][0]
    code=g[0][w-1]
    work=clone(g)
    work[0][0]=0
    work[0][w-1]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    obj=object_crop_from_component(work, comp)
    return apply_transform_code(obj, code)

def solve_medium_114_fill_matching_border_lines_inside_frame(g):
    h,w=dims(g)
    out=clone(g)
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==5]
    r0,c0,r1,c1=bbox(frame_cells)
    groups=collections.defaultdict(list)
    border_positions=set()
    for c in range(c0,c1+1):
        border_positions.add((r0,c)); border_positions.add((r1,c))
    for r in range(r0,r1+1):
        border_positions.add((r,c0)); border_positions.add((r,c1))
    for r,c in border_positions:
        v=g[r][c]
        if v not in (0,5):
            groups[v].append((r,c))
    for color,cells in groups.items():
        rows=collections.defaultdict(list)
        cols=collections.defaultdict(list)
        for r,c in cells:
            rows[r].append(c)
            cols[c].append(r)
        for r,cs in rows.items():
            if len(cs)>=2:
                lo,hi=min(cs),max(cs)
                if lo==c0 and hi==c1:
                    for c in range(c0+1,c1):
                        out[r][c]=color
        for c,rs in cols.items():
            if len(rs)>=2:
                lo,hi=min(rs),max(rs)
                if lo==r0 and hi==r1:
                    for r in range(r0+1,r1):
                        out[r][c]=color
    return out

def solve_medium_115_recolor_objects_by_hole_count(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        obj=object_crop_from_component(g, comp)
        new_color=8 if hole_count(obj)>=1 else 2
        for r,c in comp["cells"]:
            out[r][c]=new_color
    return out

def solve_medium_116_apply_gravity_inside_each_box(g):
    h,w=dims(g)
    out=zeros(h,w)
    boxes=[comp for comp in connected_components(g, colors={5})]
    for box in boxes:
        r0,c0,r1,c1=box["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=5
            out[r1][c]=5
        for r in range(r0,r1+1):
            out[r][c0]=5
            out[r][c1]=5
        ih=r1-r0-1
        iw=c1-c0-1
        for ic in range(iw):
            vals=[]
            for ir in range(ih):
                v=g[r0+1+ir][c0+1+ic]
                if v!=0:
                    vals.append(v)
            for i,v in enumerate(reversed(vals)):
                out[r1-1-i][c0+1+ic]=v
    return out

def solve_medium_117_select_rotation_match_and_recolor(g):
    h,w=dims(g)
    target=g[0][w-1]
    work=clone(g)
    work[0][w-1]=0
    ref_comp=max([comp for comp in connected_components(work, colors={1})], key=lambda comp: comp["area"])
    ref_obj=object_crop_from_component(work, ref_comp)
    for r,c in ref_comp["cells"]:
        work[r][c]=0
    candidates=connected_components(work)
    for comp in sorted(candidates, key=lambda comp: (comp["bbox"][0], comp["bbox"][1])):
        obj=object_crop_from_component(work, comp)
        if same_under_rotation(ref_obj, obj):
            return recolor_object(obj, target)
    return [[0]]

def solve_medium_118_connect_pairs_with_monotone_staircases(g):
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
        for r,c in monotone_stair_path(cells[0], cells[1]):
            out[r][c]=color
    return out

def solve_medium_119_scale_the_only_horizontally_symmetric_object(g):
    comps=connected_components(g)
    for comp in sorted(comps, key=lambda comp: (comp["bbox"][0], comp["bbox"][1])):
        obj=object_crop_from_component(g, comp)
        if is_horiz_symmetric(obj):
            return scale2(obj)
    return [[0]]

def solve_hard_113_build_dihedral_equivalence_matrix(g):
    comps=sorted(connected_components(g), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    n=len(comps)
    out=zeros(n,n)
    objs=[object_crop_from_component(g, comp) for comp in comps]
    for i in range(n):
        for j in range(n):
            if same_under_dihedral(objs[i], objs[j]):
                out[i][j]=8
    return out

def solve_hard_114_decode_library_strip_with_transform_and_recolor(g):
    h,w=dims(g)
    lib_area=[row[:] for row in g[:-1]]
    seq=g[-1]
    lib={}
    for comp in sorted(connected_components(lib_area), key=lambda comp: (comp["bbox"][1], comp["bbox"][0])):
        lib[comp["color"]]=object_crop_from_component(lib_area, comp)
    tokens=[]
    i=0
    while i < w:
        if seq[i]==0:
            i+=1
            continue
        if i+2 >= w:
            break
        tokens.append((seq[i], seq[i+1], seq[i+2]))
        i += 4
    objs=[]
    for selector,code,recolor in tokens:
        obj=apply_transform_code(lib[selector], code)
        objs.append(recolor_object(obj, recolor))
    return gallery_row(objs, gap=1)

def solve_hard_115_overlay_monotone_staircases_into_count_map(g):
    h,w=dims(g)
    counts=zeros(h,w)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        for r,c in monotone_stair_path(cells[0], cells[1]):
            counts[r][c]+=1
    return encode_count_map(counts)

def solve_hard_116_fill_chambers_by_priority_seed(g):
    h,w=dims(g)
    legend=[v for v in g[0] if v not in (0,5)]
    priority={color:i for i,color in enumerate(legend)}
    out=clone(g)
    visited=set()
    for r in range(1,h):
        for c in range(w):
            if g[r][c] in (0,*legend) and (r,c) not in visited:
                region=flood_region_within(g,(r,c),wall_color=5, row_min=1)
                visited |= region
                seeds=sorted({g[rr][cc] for rr,cc in region if g[rr][cc] in priority}, key=lambda color: priority[color])
                if not seeds:
                    fill=0
                else:
                    fill=seeds[0]
                for rr,cc in region:
                    out[rr][cc]=fill
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    return out

def solve_hard_117_decode_index_grid_into_prototype_mosaic(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==0 for v in g[r]):
            sep=r
            break
    lib_area=[row[:] for row in g[:sep]]
    raw_index=[row[:] for row in g[sep+1:]]
    # crop index grid to its nonzero extent so right-side padding does not matter
    index_area=crop_nonzero(raw_index)
    lib={}
    comps=sorted(connected_components(lib_area), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    ph=max(comp["bbox"][2]-comp["bbox"][0]+1 for comp in comps)
    pw=max(comp["bbox"][3]-comp["bbox"][1]+1 for comp in comps)
    for comp in comps:
        obj=object_crop_from_component(lib_area, comp)
        padded=zeros(ph,pw)
        stamp(padded,obj,0,0)
        lib[comp["color"]]=padded
    rows=len(index_area)
    cols=len(index_area[0])
    panels=[]
    for r in range(rows):
        prow=[]
        for c in range(cols):
            prow.append(lib[index_area[r][c]])
        panels.append(prow)
    return gallery_grid(panels, gap=0)

def solve_hard_118_overlay_transformed_prototype_stamps_into_count_map(g):
    h,w=dims(g)
    proto_comp=max([comp for comp in connected_components(g, colors={8})], key=lambda comp: comp["area"])
    proto=object_crop_from_component(g, proto_comp)
    counts=zeros(h,w)
    for r in range(h):
        for c in range(w):
            code=g[r][c]
            if code in (1,2,3,4):
                obj=apply_transform_code(proto, code)
                count_stamp(counts, obj, r, c)
    return encode_count_map(counts)

def solve_hard_119_build_pairwise_union_gallery(g):
    comps=sorted(connected_components(g), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    objs=[normalize_binary(object_crop_from_component(g, comp)) for comp in comps]
    ph=max(len(o) for o in objs)
    pw=max(len(o[0]) for o in objs)
    padded=[]
    for obj in objs:
        tmp=zeros(ph,pw)
        for r in range(len(obj)):
            for c in range(len(obj[0])):
                if obj[r][c]:
                    tmp[r][c]=1
        padded.append(tmp)
    panels=[]
    for a in padded:
        row=[]
        for b in padded:
            union=zeros(ph,pw)
            for r in range(ph):
                for c in range(pw):
                    if a[r][c] or b[r][c]:
                        union[r][c]=8
            row.append(union)
        panels.append(row)
    return gallery_grid(panels, gap=1)

SOLVERS = {

    'solve_easy_113_complete_horizontal_mirror': solve_easy_113_complete_horizontal_mirror,

    'solve_easy_114_draw_rectangle_borders_from_opposite_corners': solve_easy_114_draw_rectangle_borders_from_opposite_corners,

    'solve_easy_115_top_pack_each_column': solve_easy_115_top_pack_each_column,

    'solve_easy_116_fill_diagonal_segments': solve_easy_116_fill_diagonal_segments,

    'solve_easy_117_crop_largest_object': solve_easy_117_crop_largest_object,

    'solve_easy_118_turn_filled_rectangles_into_frames': solve_easy_118_turn_filled_rectangles_into_frames,

    'solve_easy_119_keep_centers_of_odd_squares': solve_easy_119_keep_centers_of_odd_squares,

    'solve_medium_113_select_object_by_legend_and_transform': solve_medium_113_select_object_by_legend_and_transform,

    'solve_medium_114_fill_matching_border_lines_inside_frame': solve_medium_114_fill_matching_border_lines_inside_frame,

    'solve_medium_115_recolor_objects_by_hole_count': solve_medium_115_recolor_objects_by_hole_count,

    'solve_medium_116_apply_gravity_inside_each_box': solve_medium_116_apply_gravity_inside_each_box,

    'solve_medium_117_select_rotation_match_and_recolor': solve_medium_117_select_rotation_match_and_recolor,

    'solve_medium_118_connect_pairs_with_monotone_staircases': solve_medium_118_connect_pairs_with_monotone_staircases,

    'solve_medium_119_scale_the_only_horizontally_symmetric_object': solve_medium_119_scale_the_only_horizontally_symmetric_object,

    'solve_hard_113_build_dihedral_equivalence_matrix': solve_hard_113_build_dihedral_equivalence_matrix,

    'solve_hard_114_decode_library_strip_with_transform_and_recolor': solve_hard_114_decode_library_strip_with_transform_and_recolor,

    'solve_hard_115_overlay_monotone_staircases_into_count_map': solve_hard_115_overlay_monotone_staircases_into_count_map,

    'solve_hard_116_fill_chambers_by_priority_seed': solve_hard_116_fill_chambers_by_priority_seed,

    'solve_hard_117_decode_index_grid_into_prototype_mosaic': solve_hard_117_decode_index_grid_into_prototype_mosaic,

    'solve_hard_118_overlay_transformed_prototype_stamps_into_count_map': solve_hard_118_overlay_transformed_prototype_stamps_into_count_map,

    'solve_hard_119_build_pairwise_union_gallery': solve_hard_119_build_pairwise_union_gallery,

}


BANK_JSON_NAME = 'arc_puzzle_bank_seventeenth_21.json'

def verify_against_bank():
    import json
    from pathlib import Path
    bank = json.loads(Path(__file__).with_name(BANK_JSON_NAME).read_text())
    mismatches=[]
    for task in bank:
        solver = SOLVERS[task['solver_name']]
        for split_name in ('train','test'):
            for i,pair in enumerate(task[split_name]):
                got = solver(pair['input'])
                if got != pair['output']:
                    mismatches.append((task['id'], split_name, i, got, pair['output']))
    return mismatches

if __name__ == '__main__':
    mismatches = verify_against_bank()
    if mismatches:
        print('MISMATCHES:', mismatches[:3], '... total', len(mismatches))
        raise SystemExit(1)
    print('All tasks verified against the stored bank.')
