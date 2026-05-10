from __future__ import annotations
from collections import deque
from typing import List

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
    return [row[:] for row in reversed(g)]

def rot90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g):
    return rot90(rot90(g))

def rot270(g):
    return rot90(rot180(g))

def scale2(g):
    out=[]
    for row in g:
        exp=[]
        for v in row:
            exp.extend([v,v])
        out.append(exp[:]); out.append(exp[:])
    return out

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
    cg=crop_nonzero(g)
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
            dq=deque([(r,c)])
            cells=[]
            while dq:
                rr,cc=dq.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and (nr,nc) not in ignore_positions:
                        nv=g[nr][nc]
                        if nv!=0 and (colors is None or nv in colors):
                            seen[nr][nc]=True
                            dq.append((nr,nc))
            comps.append(cells)
    return comps

def component_grid(g, cells):
    r0,c0,r1,c1=bbox(cells)
    out=zeros(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out

def sign(x):
    return (x>0)-(x<0)

def transform_by_code(g, code):
    # 1=id 2=rot90 3=hflip 4=vflip
    if code==1: return [row[:] for row in g]
    if code==2: return rot90(g)
    if code==3: return hflip(g)
    if code==4: return vflip(g)
    raise ValueError(code)

def panelize_row(panels, sep=1):
    h=len(panels[0])
    w=sum(len(p[0]) for p in panels)+sep*(len(panels)-1)
    out=zeros(h,w)
    c=0
    for i,p in enumerate(panels):
        stamp(out,p,0,c)
        c+=len(p[0])
        if i<len(panels)-1:
            c+=sep
    return out

def gallery_grid(panels2d, sep=1):
    # panels2d: rows of panels same size
    ph,pw=dims(panels2d[0][0])
    rows=len(panels2d); cols=len(panels2d[0])
    out=zeros(rows*ph+(rows-1)*sep, cols*pw+(cols-1)*sep)
    for i,row in enumerate(panels2d):
        for j,p in enumerate(row):
            stamp(out,p, i*(ph+sep), j*(pw+sep))
    return out

def xor_panels(a,b,color=7):
    h,w=dims(a)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if (a[r][c]!=0) ^ (b[r][c]!=0):
                out[r][c]=color
    return out

def find_regions_without_walls(g, wall=5, skip_rows=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    regions=[]
    for r in range(skip_rows,h):
        for c in range(w):
            if seen[r][c] or g[r][c]==wall:
                continue
            seen[r][c]=True
            dq=deque([(r,c)])
            cells=[]
            while dq:
                rr,cc=dq.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if skip_rows<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=wall:
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            regions.append(cells)
    return regions


def solve_easy_120_complete_vertical_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[r][w-1-c]=v
    return out

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

def solve_easy_124_right_pack_each_row_preserving_order(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        start=w-len(vals)
        for i,v in enumerate(vals):
            out[r][start+i]=v
    return out

def solve_easy_125_crop_the_nonzero_bounding_box(g):
    return crop_nonzero(g)

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

def solve_medium_126_select_ranked_object_and_scale2(g):
    rank=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    comps=connected_components(gg)
    comps=sorted(comps, key=lambda cells: len(cells))
    target=comps[rank-1]
    return scale2(component_grid(gg, target))

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

SOLVERS = {
    'easy_120_complete_vertical_mirror': solve_easy_120_complete_vertical_mirror,
    'easy_121_fill_horizontal_spans_between_matching_endpoints': solve_easy_121_fill_horizontal_spans_between_matching_endpoints,
    'easy_122_fill_vertical_spans_between_matching_endpoints': solve_easy_122_fill_vertical_spans_between_matching_endpoints,
    'easy_123_expand_singletons_to_radius1_diamonds': solve_easy_123_expand_singletons_to_radius1_diamonds,
    'easy_124_right_pack_each_row_preserving_order': solve_easy_124_right_pack_each_row_preserving_order,
    'easy_125_crop_the_nonzero_bounding_box': solve_easy_125_crop_the_nonzero_bounding_box,
    'easy_126_fill_diagonal_segments_between_matching_endpoints': solve_easy_126_fill_diagonal_segments_between_matching_endpoints,
    'medium_120_select_object_by_corner_legend_and_crop': solve_medium_120_select_object_by_corner_legend_and_crop,
    'medium_121_fill_intersections_from_frame_markers': solve_medium_121_fill_intersections_from_frame_markers,
    'medium_122_apply_gravity_in_each_walled_chamber': solve_medium_122_apply_gravity_in_each_walled_chamber,
    'medium_123_select_reflection_match_and_recolor': solve_medium_123_select_reflection_match_and_recolor,
    'medium_124_connect_color_pairs_with_clear_elbows': solve_medium_124_connect_color_pairs_with_clear_elbows,
    'medium_125_recolor_components_by_area_rank': solve_medium_125_recolor_components_by_area_rank,
    'medium_126_select_ranked_object_and_scale2': solve_medium_126_select_ranked_object_and_scale2,
    'hard_120_build_rotation_equivalence_matrix': solve_hard_120_build_rotation_equivalence_matrix,
    'hard_121_decode_library_with_transform_codes': solve_hard_121_decode_library_with_transform_codes,
    'hard_122_overlay_rays_until_block_count_map': solve_hard_122_overlay_rays_until_block_count_map,
    'hard_123_fill_chambers_by_seed_priority_legend': solve_hard_123_fill_chambers_by_seed_priority_legend,
    'hard_124_build_pairwise_xor_gallery': solve_hard_124_build_pairwise_xor_gallery,
    'hard_125_fill_chambers_by_nearest_seed': solve_hard_125_fill_chambers_by_nearest_seed,
    'hard_126_centered_transformed_stamp_count_map': solve_hard_126_centered_transformed_stamp_count_map,
}
