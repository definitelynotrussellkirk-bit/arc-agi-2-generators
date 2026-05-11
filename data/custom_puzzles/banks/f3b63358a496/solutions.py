from __future__ import annotations

import json

from pathlib import Path

from typing import List, Tuple, Iterable

from collections import deque, Counter, defaultdict



Grid = List[List[int]]



def zeros(h,w,val=0): return [[val for _ in range(w)] for _ in range(h)]

def clone(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def paste(g, pat, top, left, transparent=0, allow_overlap=False):
    h,w=dims(g); ph,pw=dims(pat)
    if top<0 or left<0 or top+ph>h or left+pw>w: return False
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
    return min(rs),min(cs),max(rs),max(cs)

def crop_bbox(g, box):
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def nonzero_cells(g):
    h,w=dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c]!=0]

def crop_nonzero(g):
    cells=nonzero_cells(g)
    if not cells: return [[0]]
    return crop_bbox(g,bbox(cells))

def connected_components(g, colors=None):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    if colors is not None: colors=set(colors)
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

def rotate_180(g): return [row[::-1] for row in g[::-1]]

def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]

def flip_h(g): return [row[::-1] for row in g]

def flip_v(g): return g[::-1]

def mirror_vertical(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][w-1-c]=g[r][c]
    return out

def draw_rect_border(out, r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        out[r0][c]=color; out[r1][c]=color
    for r in range(r0,r1+1):
        out[r][c0]=color; out[r][c1]=color

def hstack(grids,gap=1):
    if not grids: return [[]]
    h=max(len(g) for g in grids)
    total=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,total)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out,g,(h-gh)//2,x)
        x+=gw
        if i+1<len(grids): x+=gap
    return out

def vstack(grids,gap=1):
    if not grids: return [[]]
    w=max(len(g[0]) for g in grids)
    total=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(total,w)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        paste(out,g,y,(w-gw)//2)
        y+=gh
        if i+1<len(grids): y+=gap
    return out

def scale2(g):
    out=[]
    for row in g:
        big=[]
        for v in row:
            big.extend([v,v])
        out.append(big[:]); out.append(big[:])
    return out

def normalize_shape(g):
    return [[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]

def normalize_shape_rot(g):
    vars=[]
    cur=normalize_shape(g)
    for _ in range(4):
        vars.append(cur)
        cur=rotate_cw(cur)
    # canonical by repr
    return min(vars, key=lambda x: repr(x))

def recolor(g, color):
    return [[color if v!=0 else 0 for v in row] for row in g]

def apply_transform(g, code):
    # 1 identity,2 cw,3 180,4 flip_h,5 flip_v,6 ccw
    if code==1: return clone(g)
    if code==2: return rotate_cw(g)
    if code==3: return rotate_180(g)
    if code==4: return flip_h(g)
    if code==5: return flip_v(g)
    if code==6: return rotate_ccw(g)
    raise ValueError(code)

def majority_nonzero(vals):
    vals=[v for v in vals if v!=0]
    if not vals: return 0
    cnt=Counter(vals)
    return max(cnt.items(), key=lambda kv:(kv[1], kv[0]))[0]

def hole_count_pattern(g):
    # count zero regions fully enclosed within bbox of nonzero cells
    cells=nonzero_cells(g)
    if not cells: return 0
    cr=crop_nonzero([[1 if v!=0 else 0 for v in row] for row in g])
    h,w=dims(cr)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if cr[r][c]!=0 or seen[r][c]: 
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
                    if 0<=nr<h and 0<=nc<w and cr[nr][nc]==0 and not seen[nr][nc]:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            if not border: holes+=1
    return holes

def path_elbow(p1,p2):
    (r1,c1),(r2,c2)=p1,p2
    # sort by row then col for start
    if (r2,c2) < (r1,c1):
        r1,c1,r2,c2=r2,c2,r1,c1
    cells=[]
    step=1 if c2>=c1 else -1
    for c in range(c1, c2+step, step):
        cells.append((r1,c))
    step=1 if r2>=r1 else -1
    for r in range(r1, r2+step, step):
        cells.append((r,c2))
    return list(dict.fromkeys(cells))

def fill_from_gate_in_frame(g):
    h,w=dims(g)
    out=clone(g)
    comps=connected_components([[8 if v==8 else 0 for v in row] for row in g], colors=[8])
    # components of color 8 only; connected_components expects exact value in grid; works.
    frames=[]
    # better detect by bboxes of 8 components that form rectangular border
    for comp in comps:
        r0,c0,r1,c1=comp['bbox']
        # verify border mostly 8 maybe.
        frames.append((r0,c0,r1,c1))
    seen_boxes=set()
    for r0,c0,r1,c1 in frames:
        if (r0,c0,r1,c1) in seen_boxes: 
            continue
        seen_boxes.add((r0,c0,r1,c1))
        gate=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v not in (0,5,8):
                    if gate is None:
                        gate=(r,c,v)
        if gate is None:
            continue
        gr,gc,color=gate
        q=deque([(gr,gc)])
        seen={(gr,gc)}
        while q:
            r,c=q.popleft()
            out[r][c]=color
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if not (r0<nr<r1 and c0<nc<c1): 
                    continue
                if (nr,nc) in seen: 
                    continue
                if g[nr][nc] in (0,color): # allow fill through zeros; gate only color
                    seen.add((nr,nc))
                    q.append((nr,nc))
        # note walls 5 and other colors block
    return out

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

def solve_easy_65_complete_vertical_mirror(g):
    return mirror_vertical(g)

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

def solve_easy_67_move_cropped_object_to_top_left(g):
    obj=crop_nonzero(g)
    h,w=dims(g)
    out=zeros(h,w)
    paste(out,obj,0,0)
    return out

def solve_easy_68_read_column_markers_as_row(g):
    h,w=dims(g)
    out=[]
    for c in range(w):
        col=[g[r][c] for r in range(h) if g[r][c]!=0]
        if col:
            out.append(col[0])
    return [out]

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

def solve_medium_64_stack_crops_by_area(g):
    comps=connected_components(g)
    crops=[]
    for comp in comps:
        crops.append((comp['area'], comp['bbox'][0], comp['bbox'][1], crop_bbox(g, comp['bbox'])))
    crops=sorted(crops, key=lambda x:(x[0], x[1], x[2]))
    return vstack([c for _,_,_,c in crops], gap=1)

def solve_medium_65_transform_object_by_key(g):
    key=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    return apply_transform(obj, {1:1,2:2,3:3,4:4}[key])

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

def solve_medium_67_summarize_quadrant_majorities(g):
    h,w=dims(g)
    hm,wm=h//2,w//2
    quads=[(0,hm,0,wm),(0,hm,wm,w),(hm,h,0,wm),(hm,h,wm,w)]
    vals=[]
    for r0,r1,c0,c1 in quads:
        cell_vals=[g[r][c] for r in range(r0,r1) for c in range(c0,c1)]
        vals.append(majority_nonzero(cell_vals))
    return [[vals[0], vals[1]],[vals[2], vals[3]]]

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

def solve_hard_64_fill_local_chambers_from_gates(g):
    return fill_from_gate_in_frame(g)

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

def solve_hard_69_sort_by_holes_rotate_and_pack(g):
    items=[]
    for comp in connected_components(g):
        crop=crop_bbox(g, comp['bbox'])
        holes=hole_count_pattern(crop)
        items.append((holes, comp['area'], comp['bbox'][0], comp['bbox'][1], rotate_cw(crop)))
    items.sort(key=lambda x:(x[0], x[1], x[2], x[3]))
    return hstack([item[-1] for item in items], gap=1)

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

SOLVERS = {
    "solve_easy_64_fill_between_matching_endpoints": solve_easy_64_fill_between_matching_endpoints,
    "solve_easy_65_complete_vertical_mirror": solve_easy_65_complete_vertical_mirror,
    "solve_easy_66_draw_rectangle_borders_from_corner_pairs": solve_easy_66_draw_rectangle_borders_from_corner_pairs,
    "solve_easy_67_move_cropped_object_to_top_left": solve_easy_67_move_cropped_object_to_top_left,
    "solve_easy_68_read_column_markers_as_row": solve_easy_68_read_column_markers_as_row,
    "solve_easy_69_cast_rightward_rays_until_wall": solve_easy_69_cast_rightward_rays_until_wall,
    "solve_easy_70_expand_diagonal_pairs_into_xs": solve_easy_70_expand_diagonal_pairs_into_xs,
    "solve_medium_64_stack_crops_by_area": solve_medium_64_stack_crops_by_area,
    "solve_medium_65_transform_object_by_key": solve_medium_65_transform_object_by_key,
    "solve_medium_66_build_equality_matrix_from_headers": solve_medium_66_build_equality_matrix_from_headers,
    "solve_medium_67_summarize_quadrant_majorities": solve_medium_67_summarize_quadrant_majorities,
    "solve_medium_68_connect_matching_markers_with_elbows": solve_medium_68_connect_matching_markers_with_elbows,
    "solve_medium_69_crop_component_with_most_holes": solve_medium_69_crop_component_with_most_holes,
    "solve_medium_70_fill_each_components_bounding_box": solve_medium_70_fill_each_components_bounding_box,
    "solve_hard_64_fill_local_chambers_from_gates": solve_hard_64_fill_local_chambers_from_gates,
    "solve_hard_65_decode_library_transform_recolor_gallery": solve_hard_65_decode_library_transform_recolor_gallery,
    "solve_hard_66_build_rotation_invariant_shape_color_relation_matrix": solve_hard_66_build_rotation_invariant_shape_color_relation_matrix,
    "solve_hard_67_select_ranked_component_scale_and_place": solve_hard_67_select_ranked_component_scale_and_place,
    "solve_hard_68_build_template_transform_mosaic": solve_hard_68_build_template_transform_mosaic,
    "solve_hard_69_sort_by_holes_rotate_and_pack": solve_hard_69_sort_by_holes_rotate_and_pack,
    "solve_hard_70_decode_local_frame_template_codes": solve_hard_70_decode_local_frame_template_codes,
}


def verify_bank(json_path: str | Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_tenth_21.json")
    json_path = Path(json_path)
    tasks = json.loads(json_path.read_text())
    for task in tasks:
        solver = SOLVERS[task["solver_name"]]
        for pair in task["train"] + task["test"]:
            got = solver(pair["input"])
            if got != pair["output"]:
                raise AssertionError(f"Mismatch in {task['id']} via {task['solver_name']}")
    print(f"verified {len(tasks)} tasks from {json_path.name}")

if __name__ == "__main__":
    verify_bank()