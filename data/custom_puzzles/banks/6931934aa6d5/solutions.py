from __future__ import annotations

import json
from pathlib import Path
from typing import List

Grid = List[List[int]]


from collections import deque, Counter, defaultdict

def zeros(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def paste(g, pat, top, left, transparent=0, allow_overlap=False):
    h,w=dims(g); ph,pw=dims(pat)
    if top<0 or left<0 or top+ph>h or left+pw>w:
        return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent and not allow_overlap and g[top+r][left+c]!=0:
                return False
    for r in range(ph):
        for c in range(pw):
            v=pat[r][c]
            if v!=transparent:
                g[top+r][left+c]=v
    return True

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, box):
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def nonzero_cells(g):
    h,w=dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c]!=0]

def crop_nonzero(g):
    cells=nonzero_cells(g)
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))

def connected_components(g, colors=None):
    h,w=dims(g)
    if colors is not None:
        colors=set(colors)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            q=deque([(r,c)])
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        if colors is None or v in colors:
                            seen[nr][nc]=True
                            q.append((nr,nc))
            comps.append({'color':v,'cells':cells,'bbox':bbox(cells),'area':len(cells)})
    return comps

def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]

def rotate_180(g):
    return [row[::-1] for row in g[::-1]]

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def draw_rect_border(g, r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color
        g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color
        g[r][c1]=color

def fill_rect(g, r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color

def hstack(grids, gap=1):
    if not grids:
        return [[]]
    h=max(len(g) for g in grids)
    total=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,total)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out, g, (h-gh)//2, x)
        x += gw
        if i+1<len(grids):
            x += gap
    return out

def vstack(grids, gap=1):
    if not grids:
        return [[]]
    w=max(len(g[0]) for g in grids)
    total=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(total,w)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out, g, y, (w-gw)//2)
        y += gh
        if i+1<len(grids):
            y += gap
    return out

def scale2(g):
    out=[]
    for row in g:
        big=[]
        for v in row:
            big.extend([v,v])
        out.append(big[:])
        out.append(big[:])
    return out

def recolor(g, color):
    return [[color if v!=0 else 0 for v in row] for row in g]

def majority_nonzero(vals):
    vals=[v for v in vals if v!=0]
    if not vals:
        return 0
    cnt=Counter(vals)
    return max(cnt.items(), key=lambda kv:(kv[1], kv[0]))[0]

def normalize_binary(g):
    return [[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]

def canonical_rot(g):
    cur=normalize_binary(g)
    vars=[]
    for _ in range(4):
        vars.append(cur)
        cur=rotate_cw(cur)
    return min(vars, key=lambda x: repr(x))

def hole_count_binary(g):
    # g is binary-ish; nonzero treated as wall
    b=[[1 if v!=0 else 0 for v in row] for row in g]
    b=crop_nonzero(b)
    h,w=dims(b)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if b[r][c]!=0 or seen[r][c]:
                continue
            seen[r][c]=True
            q=deque([(r,c)])
            border=False
            while q:
                rr,cc=q.popleft()
                if rr in (0,h-1) or cc in (0,w-1):
                    border=True
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and b[nr][nc]==0 and not seen[nr][nc]:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            if not border:
                holes += 1
    return holes


def apply_transform(g, code):
    if code==1:
        return clone(g)
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
    raise ValueError(code)

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

def solve_easy_73_crop_nonzero_bounding_box(g):
    return crop_nonzero(g)

def solve_easy_74_compact_nonzero_rows_up(g):
    h,w=dims(g)
    rows=[row[:] for row in g if any(v!=0 for v in row)]
    while len(rows)<h:
        rows.append([0]*w)
    return rows

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

def solve_easy_77_mirror_across_main_diagonal(g):
    n=len(g)
    out=clone(g)
    for r in range(n):
        for c in range(n):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out

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

SOLVERS = {
    "solve_easy_71_fill_diagonal_between_matching_endpoints": solve_easy_71_fill_diagonal_between_matching_endpoints,
    "solve_easy_72_expand_singletons_to_plus": solve_easy_72_expand_singletons_to_plus,
    "solve_easy_73_crop_nonzero_bounding_box": solve_easy_73_crop_nonzero_bounding_box,
    "solve_easy_74_compact_nonzero_rows_up": solve_easy_74_compact_nonzero_rows_up,
    "solve_easy_75_fill_hollow_rectangles": solve_easy_75_fill_hollow_rectangles,
    "solve_easy_76_cast_vertical_rays_downward": solve_easy_76_cast_vertical_rays_downward,
    "solve_easy_77_mirror_across_main_diagonal": solve_easy_77_mirror_across_main_diagonal,
    "solve_medium_71_marker_selects_component_to_crop": solve_medium_71_marker_selects_component_to_crop,
    "solve_medium_72_frame_gate_cross_fill": solve_medium_72_frame_gate_cross_fill,
    "solve_medium_73_rotate_source_by_control_color": solve_medium_73_rotate_source_by_control_color,
    "solve_medium_74_scale_smallest_component_and_recolor": solve_medium_74_scale_smallest_component_and_recolor,
    "solve_medium_75_quadrant_majority_summary": solve_medium_75_quadrant_majority_summary,
    "solve_medium_76_recover_rectangles_from_three_corners": solve_medium_76_recover_rectangles_from_three_corners,
    "solve_medium_77_border_rays_until_block": solve_medium_77_border_rays_until_block,
    "solve_hard_71_library_lookup_transform_gallery": solve_hard_71_library_lookup_transform_gallery,
    "solve_hard_72_boolean_operation_by_marker": solve_hard_72_boolean_operation_by_marker,
    "solve_hard_73_choose_most_holes_scale2_recolor": solve_hard_73_choose_most_holes_scale2_recolor,
    "solve_hard_74_fill_keyed_chambers_inside_frames": solve_hard_74_fill_keyed_chambers_inside_frames,
    "solve_hard_75_rotational_equivalence_matrix": solve_hard_75_rotational_equivalence_matrix,
    "solve_hard_76_rank_components_by_area_and_stack": solve_hard_76_rank_components_by_area_and_stack,
    "solve_hard_77_cross_product_intersection_gallery": solve_hard_77_cross_product_intersection_gallery,
}


def verify_against_json(json_path: Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_eleventh_21.json")
    data = json.loads(json_path.read_text())
    for task in data:
        solver = SOLVERS[task["solver_name"]]
        for section in ("train", "test"):
            for pair in task[section]:
                got = solver(pair["input"])
                if got != pair["output"]:
                    raise AssertionError(f"Mismatch for {task['id']} in {section}")
    print(f"verified {len(data)} tasks against {json_path.name}")


if __name__ == "__main__":
    verify_against_json()
