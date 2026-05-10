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

def transpose_square(g):
    n=len(g)
    return [[g[c][r] for c in range(n)] for r in range(n)]

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

def flood_regions_nonwall(g, wall=8):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    regs=[]
    for r in range(h):
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
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=wall:
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            regs.append(cells)
    return regs

def component_grid(g, cells):
    r0,c0,r1,c1=bbox(cells)
    out=zeros(r1-r0+1, c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out

def perimeter_of_cells(cells):
    s=set(cells)
    p=0
    for r,c in cells:
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            if (r+dr,c+dc) not in s:
                p+=1
    return p

def recolor_nonzero(g, color):
    return [[color if v!=0 else 0 for v in row] for row in g]

def transform_by_code(g, code):
    if code==1: return [row[:] for row in g]
    if code==2: return rot90(g)
    if code==3: return hflip(g)
    if code==4: return vflip(g)
    raise ValueError(code)

def all_rotations(g):
    a=normalize_binary(g)
    outs=[]
    cur=a
    for _ in range(4):
        if cur not in outs:
            outs.append(cur)
        cur=rot90(cur)
    return outs

def all_dihedral(g):
    a=normalize_binary(g)
    outs=[]
    cur=a
    for _ in range(4):
        if cur not in outs:
            outs.append(cur)
        cur=rot90(cur)
    cur=hflip(a)
    for _ in range(4):
        if cur not in outs:
            outs.append(cur)
        cur=rot90(cur)
    return outs

def is_vertical_symmetric(g):
    a=normalize_binary(g)
    return a==hflip(a)

def elbow_cells(p1, p2, first='h'):
    r1,c1=p1; r2,c2=p2
    cells=[]
    if first=='h':
        step=1 if c2>=c1 else -1
        for c in range(c1, c2+step, step):
            cells.append((r1,c))
        step=1 if r2>=r1 else -1
        for r in range(r1+step, r2+step, step):
            cells.append((r,c2))
    else:
        step=1 if r2>=r1 else -1
        for r in range(r1, r2+step, step):
            cells.append((r,c1))
        step=1 if c2>=c1 else -1
        for c in range(c1+step, c2+step, step):
            cells.append((r2,c))
    seen=set()
    out=[]
    for x in cells:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def path_clear(g, cells, endpoints):
    h,w=dims(g)
    endset=set(endpoints)
    for r,c in cells:
        if not (0<=r<h and 0<=c<w):
            return False
        if (r,c) in endset:
            continue
        if g[r][c]!=0:
            return False
    return True

def center_stamp(canvas_h, canvas_w, obj):
    h,w=dims(obj)
    out=zeros(canvas_h, canvas_w)
    top=(canvas_h-h)//2
    left=(canvas_w-w)//2
    stamp(out,obj,top,left)
    return out

def solve_easy_127_complete_horizontal_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[h-1-r][c]=v
    return out

def solve_easy_128_fill_rectangle_from_opposite_corners(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return clone(g)
    color=g[cells[0][0]][cells[0][1]]
    r0,c0,r1,c1=bbox(cells)
    out=zeros(len(g), len(g[0]))
    for r in range(r0, r1+1):
        for c in range(c0, c1+1):
            out[r][c]=color
    return out

def solve_easy_129_expand_singletons_to_radius1_pluses(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr,dc in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out

def solve_easy_130_up_pack_each_column_preserving_order(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[i][c]=v
    return out

def solve_easy_131_transpose_square_grid(g):
    return transpose_square(g)

def solve_easy_132_draw_bbox_border_around_nonzero_cells(g):
    h,w=dims(g)
    out=clone(g)
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return out
    r0,c0,r1,c1=bbox(cells)
    for c in range(c0, c1+1):
        if out[r0][c]==0: out[r0][c]=8
        if out[r1][c]==0: out[r1][c]=8
    for r in range(r0, r1+1):
        if out[r][c0]==0: out[r][c0]=8
        if out[r][c1]==0: out[r][c1]=8
    return out

def solve_easy_133_recolor_source_to_target_from_corner_legend(g):
    h,w=dims(g)
    src=g[0][0]
    tgt=g[0][w-1]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if (r,c) not in ((0,0),(0,w-1)) and out[r][c]==src:
                out[r][c]=tgt
    return out

def solve_medium_127_select_legend_object_and_rotate_cw(g):
    legend=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    comps=connected_components(gg)
    for cells in comps:
        colors={gg[r][c] for r,c in cells if gg[r][c]!=0}
        if colors=={legend}:
            return rot90(component_grid(gg, cells))
    return [[0]]

def solve_medium_128_build_marker_equality_matrix(g):
    top=g[0][1:]
    left=[row[0] for row in g[1:]]
    out=zeros(len(left), len(top))
    for r,lv in enumerate(left):
        for c,tv in enumerate(top):
            if lv!=0 and lv==tv:
                out[r][c]=lv
    return out

def solve_medium_129_apply_upward_gravity_in_each_walled_chamber(g):
    h,w=dims(g)
    out=clone(g)
    chambers=flood_regions_nonwall(g, wall=8)
    for cells in chambers:
        for r,c in cells:
            out[r][c]=0
        cols=sorted({c for r,c in cells})
        for c in cols:
            rows=sorted(r for r,cc in cells if cc==c)
            vals=[g[r][c] for r in rows if g[r][c]!=0]
            for i,r in enumerate(rows):
                out[r][c]=vals[i] if i<len(vals) else 0
    return out

def solve_medium_130_find_exemplar_match_and_recolor(g):
    exemplar=[row[:5] for row in g[:5]]
    target_norm=normalize_binary(exemplar)
    gg=clone(g)
    for r in range(5):
        for c in range(5):
            gg[r][c]=0
    for cells in connected_components(gg):
        if normalize_binary(component_grid(gg, cells))==target_norm:
            return recolor_nonzero(component_grid(gg, cells), 2)
    return [[0]]

def solve_medium_131_connect_color_pairs_with_clear_elbows(g):
    h,w=dims(g)
    out=clone(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v not in (0,8):
                pos.setdefault(v, []).append((r,c))
    for color, pts in pos.items():
        if len(pts)!=2:
            continue
        p1,p2=pts
        path_h=elbow_cells(p1,p2,'h')
        path_v=elbow_cells(p1,p2,'v')
        if path_clear(g, path_h, pts):
            cells=path_h
        else:
            cells=path_v
        for r,c in cells:
            if out[r][c]!=8:
                out[r][c]=color
    return out

def solve_medium_132_recolor_components_by_perimeter_rank(g):
    comps=connected_components(g)
    ranked=sorted(comps, key=lambda cells: perimeter_of_cells(cells))
    colors=[2,3,4]
    out=zeros(len(g), len(g[0]))
    for cells,color in zip(ranked, colors):
        for r,c in cells:
            out[r][c]=color
    return out

def solve_medium_133_select_vertically_symmetric_object_and_crop(g):
    for cells in connected_components(g):
        cg=component_grid(g, cells)
        if is_vertical_symmetric(cg):
            return recolor_nonzero(cg, 8)
    return [[0]]

def solve_hard_127_build_reflection_equivalence_matrix(g):
    panel_w=5
    sep=1
    panels=[]
    c=0
    while c+panel_w<=len(g[0]):
        panel=[row[c:c+panel_w] for row in g]
        panels.append(normalize_binary(panel))
        c+=panel_w+sep
    n=len(panels)
    out=zeros(n,n)
    for i,a in enumerate(panels):
        for j,b in enumerate(panels):
            if i==j:
                out[i][j]=8
            elif b==normalize_binary(hflip(a)) or b==normalize_binary(vflip(a)):
                out[i][j]=2
    return out

def solve_hard_128_decode_prototype_library_with_transform_and_recolor_codes(g):
    lib_rows=g[:3]
    code_row=g[4]
    protos=[]
    c=0
    while c+3<=len(lib_rows[0]):
        protos.append([row[c:c+3] for row in lib_rows])
        c+=4
    panels=[]
    for start in (0,4,8):
        idx,code,col=code_row[start:start+3]
        obj=transform_by_code(protos[idx-1], code)
        panels.append(recolor_nonzero(obj, col))
    return panelize_row(panels, sep=1)

def solve_hard_129_overlay_elbow_paths_count_map(g):
    h,w=dims(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos.setdefault(v, []).append((r,c))
    counts=zeros(h,w)
    for color,pts in pos.items():
        if len(pts)!=2:
            continue
        for r,c in elbow_cells(pts[0], pts[1], 'h'):
            counts[r][c]+=1
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if counts[r][c]==1:
                out[r][c]=2
            elif counts[r][c]==2:
                out[r][c]=3
            elif counts[r][c]>=3:
                out[r][c]=4
    return out

def solve_hard_130_fill_chambers_by_legend_priority(g):
    h,w=dims(g)
    out=clone(g)
    priority=[v for v in g[0] if v not in (0,8)]
    area=[row[:] for row in g[2:]]
    chambers=flood_regions_nonwall(area, wall=8)
    for cells in chambers:
        present={area[r][c] for r,c in cells if area[r][c]!=0}
        chosen=0
        for color in priority:
            if color in present:
                chosen=color
                break
        for r,c in cells:
            out[r+2][c]=chosen
    return out

def solve_hard_131_build_boolean_gallery_union_intersection_xor(g):
    left=[row[:5] for row in g]
    right=[row[6:11] for row in g]
    union=zeros(5,5)
    inter=zeros(5,5)
    xor=zeros(5,5)
    for r in range(5):
        for c in range(5):
            a=1 if left[r][c]!=0 else 0
            b=1 if right[r][c]!=0 else 0
            if a or b: union[r][c]=2
            if a and b: inter[r][c]=3
            if (a+b)==1: xor[r][c]=4
    return panelize_row([union, inter, xor], sep=1)

def solve_hard_132_build_dihedral_relation_matrix(g):
    panel_w=5
    sep=1
    panels=[]
    c=0
    while c+panel_w<=len(g[0]):
        panel=[row[c:c+panel_w] for row in g]
        panels.append(normalize_binary(panel))
        c+=panel_w+sep
    n=len(panels)
    out=zeros(n,n)
    for i,a in enumerate(panels):
        rotset=all_rotations(a)
        dihedral=all_dihedral(a)
        for j,b in enumerate(panels):
            if i==j:
                out[i][j]=8
            elif b==a:
                out[i][j]=1
            elif b in rotset:
                out[i][j]=2
            elif b in dihedral:
                out[i][j]=3
            else:
                out[i][j]=0
    return out

def solve_hard_133_compose_two_transforms_and_center_stamp(g):
    proto=crop_nonzero(g[:5])
    t1,t2,col=g[5][:3]
    obj=transform_by_code(proto, t1)
    obj=transform_by_code(obj, t2)
    obj=recolor_nonzero(obj, col)
    return center_stamp(7, 7, obj)
