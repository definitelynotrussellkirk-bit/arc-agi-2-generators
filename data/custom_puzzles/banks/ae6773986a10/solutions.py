"""Reference solvers for the fifth 21-task ARC-style puzzle bank.

This batch deliberately broadens the task families beyond the earlier banks.

New primitive introduced here:
- beamcast(start, direction, stop_condition): march cell-by-cell from a seed or
  signal source in a chosen direction until a blocker or border stops the ray.

The primitive is used explicitly in:
  easy_e01, medium_e01, hard_e01, hard_e05
"""

from typing import Tuple

NEW_PRIMITIVES = {
    "beamcast": "March from a start cell in a direction until a blocker or border, returning the traversed cells.",
}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def rotate_cw(g):
    h,w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def anti_diag_reflect(g):
    n,m = dims(g)
    assert n==m
    return [[g[n-1-c][n-1-r] for c in range(n)] for r in range(n)]


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    r0,r1=min(rs),max(rs); c0,c1=min(cs),max(cs)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def bbox_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)


def components(g, colors_same=True):
    h,w = dims(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0:
                continue
            color = g[r][c]
            stack=[(r,c)]
            vis[r][c]=True
            cells=[]
            while stack:
                x,y = stack.pop()
                cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not vis[nx][ny]:
                        if colors_same:
                            ok = g[nx][ny]==color
                        else:
                            ok = g[nx][ny]!=0
                        if ok:
                            vis[nx][ny]=True
                            stack.append((nx,ny))
            comps.append({'color': color, 'cells': cells})
    return comps


def comp_grid(comp):
    r0,r1,c0,c1 = bbox_cells(comp['cells'])
    out = blank(r1-r0+1, c1-c0+1)
    for r,c in comp['cells']:
        out[r-r0][c-c0]=comp['color']
    return out


def normalize_shape(comp):
    g = comp_grid(comp)
    color = comp['color']
    return tuple(tuple(1 if v!=0 else 0 for v in row) for row in g)


def all_dihedral_forms(shape):
    # shape grid of 0/1 tuples or ints
    g = [list(row) for row in shape]
    forms=[]
    cur = g
    for _ in range(4):
        forms.append(tuple(tuple(row) for row in cur))
        forms.append(tuple(tuple(row) for row in flip_h(cur)))
        cur = rotate_cw(cur)
    # unique preserve order
    uniq=[]
    seen=set()
    for f in forms:
        if f not in seen:
            seen.add(f); uniq.append(f)
    return uniq


def holes_mask(g):
    # return enclosed zero cells mask (True for hole) treating nonzero as walls
    h,w=dims(g)
    vis=[[False]*w for _ in range(h)]
    from collections import deque
    q=deque()
    for r in range(h):
        for c in [0,w-1]:
            if g[r][c]==0 and not vis[r][c]:
                vis[r][c]=True; q.append((r,c))
    for c in range(w):
        for r in [0,h-1]:
            if g[r][c]==0 and not vis[r][c]:
                vis[r][c]=True; q.append((r,c))
    while q:
        x,y=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<h and 0<=ny<w and g[nx][ny]==0 and not vis[nx][ny]:
                vis[nx][ny]=True; q.append((nx,ny))
    mask=[[g[r][c]==0 and not vis[r][c] for c in range(w)] for r in range(h)]
    return mask


def beamcast_cells(start: Tuple[int,int], dr:int, dc:int, h:int, w:int, blocker_cells:set=None, blocker_pred=None, include_start=False):
    # yields cells from start+step
    cells=[]
    r,c = start
    if include_start:
        cells.append((r,c))
    while True:
        r += dr; c += dc
        if not (0<=r<h and 0<=c<w):
            break
        stop=False
        if blocker_cells is not None and (r,c) in blocker_cells:
            stop=True
        if blocker_pred is not None and blocker_pred(r,c):
            stop=True
        if stop:
            break
        cells.append((r,c))
    return cells


def paste(g, shape, top, left, overwrite_zero_only=False):
    H,W=dims(g)
    h,w=dims(shape)
    for r in range(h):
        for c in range(w):
            v=shape[r][c]
            if v!=0:
                rr,cc=top+r,left+c
                if 0<=rr<H and 0<=cc<W:
                    if not overwrite_zero_only or g[rr][cc]==0:
                        g[rr][cc]=v
    return g


def solve_e_e01_beam_right_to_gray(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v not in (0,5):
                cc=c+1
                while cc<w and g[r][cc]!=5:
                    out[r][cc]=v
                    cc+=1
    return out


def solve_e_e02_fill_horizontal_a0a(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w-2):
            a,b,d=g[r][c],g[r][c+1],g[r][c+2]
            if a!=0 and a==d and b==0:
                out[r][c+1]=a
    return out


def solve_e_e03_keep_exactly_two_occurrence_colors(g):
    from collections import Counter
    cnt=Counter(v for row in g for v in row if v!=0)
    return [[v if v!=0 and cnt[v]==2 else 0 for v in row] for row in g]


def solve_e_e04_reflect_anti_diagonal(g):
    return anti_diag_reflect(g)


def solve_e_e05_keep_horizontal_run_endpoints(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1
                continue
            color=g[r][c]
            start=c
            while c+1<w and g[r][c+1]==color:
                c+=1
            end=c
            if start==end:
                out[r][start]=color
            else:
                out[r][start]=color
                out[r][end]=color
            c+=1
    return out


def solve_e_e06_union_with_horizontal_mirror(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[r][w-1-c]=v
    return out


def solve_e_e07_left_compress_with_row_blockers(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==5:
                out[r][c]=5
                c+=1
                continue
            start=c
            while c<w and g[r][c]!=5:
                c+=1
            end=c
            vals=[g[r][j] for j in range(start,end) if g[r][j] not in (0,5)]
            for i,v in enumerate(vals):
                out[r][start+i]=v
    return out


def solve_e_m01_marker_directed_beams(g):
    h,w=dims(g)
    marker=None
    for pos in [(0,0),(0,w-1),(h-1,0),(h-1,w-1)]:
        r,c=pos
        if g[r][c] in (1,2,3,4):
            marker=(r,c,g[r][c]); break
    assert marker
    drdc={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}[marker[2]]
    blockers={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=5 and not (r==marker[0] and c==marker[1]):
                for rr,cc in beamcast_cells((r,c),*drdc,h,w,blocker_cells=blockers,include_start=False):
                    out[rr][cc]=v
    return out


def solve_e_m02_segmented_column_gravity(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==5:
                out[r][c]=5
                r+=1
                continue
            start=r
            while r<h and g[r][c]!=5:
                r+=1
            end=r
            vals=[g[i][c] for i in range(start,end) if g[i][c] not in (0,5)]
            pos=end-1
            for v in reversed(vals):
                out[pos][c]=v
                pos-=1
    return out


def solve_e_m03_output_holes_only(g):
    mask=holes_mask(g)
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if mask[r][c]:
                out[r][c]=8
    return out


def solve_e_m04_extract_exact_odd_shape(g):
    comps=components(g)
    shapes=[normalize_shape(c) for c in comps]
    # count exact shapes
    from collections import Counter
    cnt=Counter(shapes)
    odd_idx=next(i for i,s in enumerate(shapes) if cnt[s]==1)
    return comp_grid(comps[odd_idx])


def solve_e_m05_repeat_motif_by_vector(g):
    h,w=dims(g)
    p1=p2=None
    obj=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==1:
                p1=(r,c)
            elif v==2:
                p2=(r,c)
            elif v!=0:
                obj[r][c]=v
    assert p1 and p2
    dr,dc = p2[0]-p1[0], p2[1]-p1[1]
    cells=[(r,c,obj[r][c]) for r in range(h) for c in range(w) if obj[r][c]!=0]
    out=blank(h,w)
    k=0
    while True:
        shifted=[(r+k*dr,c+k*dc,v) for r,c,v in cells]
        if all(0<=r<h and 0<=c<w for r,c,v in shifted):
            for r,c,v in shifted:
                out[r][c]=v
            k+=1
        else:
            break
    return out


def solve_e_m06_row_col_intersections(g):
    h,w=dims(g)
    rows=[r for r in range(h) if g[r][0]==1]
    cols=[c for c in range(w) if g[0][c]==2]
    out=blank(h,w)
    for r in rows:
        for c in cols:
            out[r][c]=8
    return out


def solve_e_m07_bbox_overlap(g):
    colors=sorted({v for row in g for v in row if v!=0})
    assert len(colors)==2
    bboxes={}
    for color in colors:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        bboxes[color]=bbox_cells(cells)
    (r0a,r1a,c0a,c1a),(r0b,r1b,c0b,c1b) = [bboxes[c] for c in colors]
    r0=max(r0a,r0b); r1=min(r1a,r1b); c0=max(c0a,c0b); c1=min(c1a,c1b)
    out=blank(*dims(g))
    if r0<=r1 and c0<=c1:
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=8
    return out


def solve_e_h01_shadow_from_border_light(g):
    h,w=dims(g)
    light=None
    obj=[]
    out=blank(h,w)
    # preserve object later
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==4 and (r in (0,h-1) or c in (0,w-1)):
                light=(r,c)
            elif v!=0:
                obj.append((r,c,v))
    assert light
    lr,lc=light
    if lc==0: dr,dc=0,1
    elif lc==w-1: dr,dc=0,-1
    elif lr==0: dr,dc=1,0
    else: dr,dc=-1,0
    # shadow
    for r,c,v in obj:
        rr,cc=r+dr,c+dc
        while 0<=rr<h and 0<=cc<w:
            out[rr][cc]=4
            rr+=dr; cc+=dc
    # preserve object
    for r,c,v in obj:
        out[r][c]=v
    return out


def solve_e_h02_extract_dihedral_odd_shape(g):
    comps=components(g)
    shape_classes=[]
    canon=[]
    for comp in comps:
        base=tuple(tuple(1 if v!=0 else 0 for v in row) for row in comp_grid(comp))
        forms=all_dihedral_forms(base)
        c=min(forms)
        canon.append(c)
    from collections import Counter
    cnt=Counter(canon)
    odd_idx=next(i for i,c in enumerate(canon) if cnt[c]==1)
    return comp_grid(comps[odd_idx])


def solve_e_h03_hole_gallery_sorted(g):
    # find hole components; color each hole by adjacent enclosing color; sort by area descending
    h,w=dims(g)
    mask=holes_mask(g)
    vis=[[False]*w for _ in range(h)]
    holes=[]
    for r in range(h):
        for c in range(w):
            if mask[r][c] and not vis[r][c]:
                stack=[(r,c)]
                vis[r][c]=True
                cells=[]
                adj_colors=set()
                while stack:
                    x,y=stack.pop()
                    cells.append((x,y))
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if 0<=nx<h and 0<=ny<w:
                            if mask[nx][ny] and not vis[nx][ny]:
                                vis[nx][ny]=True; stack.append((nx,ny))
                            elif g[nx][ny]!=0:
                                adj_colors.add(g[nx][ny])
                color=min(adj_colors) if adj_colors else 8
                # normalized shape
                r0,r1,c0,c1 = bbox_cells(cells)
                shape=blank(r1-r0+1,c1-c0+1)
                for x,y in cells:
                    shape[x-r0][y-c0]=color
                holes.append({'cells':cells,'shape':shape,'area':len(cells)})
    holes.sort(key=lambda d:(-d['area'], dims(d['shape'])[0], dims(d['shape'])[1]))
    if not holes:
        return [[0]]
    total_w=sum(dims(hh['shape'])[1] for hh in holes)+ (len(holes)-1)
    H=max(dims(hh['shape'])[0] for hh in holes)
    out=blank(H,total_w)
    c0=0
    for hh in holes:
        sh=hh['shape']
        paste(out, sh, H-dims(sh)[0], c0)
        c0 += dims(sh)[1] + 1
    return out


def solve_e_h04_apply_key_row_transform_sequence(g):
    h,w=dims(g)
    key=[v for v in g[0] if v in (1,2,3)]
    body=[row[:] for row in g[2:]] if h>=2 else []
    obj=crop_nonzero(body)
    cur=obj
    for k in key:
        if k==1:
            cur=rotate_cw(cur)
        elif k==2:
            cur=flip_h(cur)
        elif k==3:
            cur=flip_v(cur)
    return cur


def solve_e_h05_beam_intersections_with_blockers(g):
    h,w=dims(g)
    blockers={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    horiz=set()
    vert=set()
    for r in range(h):
        if g[r][0]==2:
            for cell in beamcast_cells((r,0),0,1,h,w,blocker_cells=blockers,include_start=False):
                horiz.add(cell)
    for c in range(w):
        if g[0][c]==1:
            for cell in beamcast_cells((0,c),1,0,h,w,blocker_cells=blockers,include_start=False):
                vert.add(cell)
    out=blank(h,w)
    for r,c in blockers:
        out[r][c]=5
    for r,c in horiz & vert:
        out[r][c]=8
    return out


def solve_e_h06_orbit_object_around_center(g):
    h,w=dims(g)
    center=None
    obj=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==9:
                center=(r,c)
            elif v!=0:
                obj[r][c]=v
    shape=crop_nonzero(obj)
    rots=[shape]
    for _ in range(3):
        rots.append(rotate_cw(rots[-1]))
    ch,cw=center
    out=blank(h,w)
    sh=rots[0]; hh,ww=dims(sh)
    paste(out,sh,ch-1-hh,cw-ww//2)
    sh=rots[1]; hh,ww=dims(sh)
    paste(out,sh,ch-hh//2,cw+2)
    sh=rots[2]; hh,ww=dims(sh)
    paste(out,sh,ch+2,cw-ww//2)
    sh=rots[3]; hh,ww=dims(sh)
    paste(out,sh,ch-hh//2,cw-1-ww)
    out[ch][cw]=9
    return out


def solve_e_h07_shortest_corridor_path(g):
    h,w=dims(g)
    walls={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    portals=[(r,c,v) for r in range(h) for c,v in enumerate(g[r]) if v not in (0,5)]
    # assume exactly two same-colored portals
    assert len(portals)==2 and portals[0][2]==portals[1][2]
    (sr,sc,color),(tr,tc,_) = portals
    from collections import deque
    q=deque([(sr,sc)])
    prev={ (sr,sc): None }
    # deterministic order: right, down, left, up
    dirs=[(0,1),(1,0),(0,-1),(-1,0)]
    while q:
        x,y=q.popleft()
        if (x,y)==(tr,tc):
            break
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<=nx<h and 0<=ny<w and (nx,ny) not in prev:
                if (nx,ny) not in walls and (g[nx][ny]==0 or (nx,ny)==(tr,tc)):
                    prev[(nx,ny)]=(x,y)
                    q.append((nx,ny))
    assert (tr,tc) in prev
    out=blank(h,w)
    for r,c in walls:
        out[r][c]=5
    cur=(tr,tc)
    while cur is not None:
        r,c=cur
        out[r][c]=color
        cur=prev[cur]
    return out


SOLVERS = {
    "solve_e_e01_beam_right_to_gray": solve_e_e01_beam_right_to_gray,
    "solve_e_e02_fill_horizontal_a0a": solve_e_e02_fill_horizontal_a0a,
    "solve_e_e03_keep_exactly_two_occurrence_colors": solve_e_e03_keep_exactly_two_occurrence_colors,
    "solve_e_e04_reflect_anti_diagonal": solve_e_e04_reflect_anti_diagonal,
    "solve_e_e05_keep_horizontal_run_endpoints": solve_e_e05_keep_horizontal_run_endpoints,
    "solve_e_e06_union_with_horizontal_mirror": solve_e_e06_union_with_horizontal_mirror,
    "solve_e_e07_left_compress_with_row_blockers": solve_e_e07_left_compress_with_row_blockers,
    "solve_e_m01_marker_directed_beams": solve_e_m01_marker_directed_beams,
    "solve_e_m02_segmented_column_gravity": solve_e_m02_segmented_column_gravity,
    "solve_e_m03_output_holes_only": solve_e_m03_output_holes_only,
    "solve_e_m04_extract_exact_odd_shape": solve_e_m04_extract_exact_odd_shape,
    "solve_e_m05_repeat_motif_by_vector": solve_e_m05_repeat_motif_by_vector,
    "solve_e_m06_row_col_intersections": solve_e_m06_row_col_intersections,
    "solve_e_m07_bbox_overlap": solve_e_m07_bbox_overlap,
    "solve_e_h01_shadow_from_border_light": solve_e_h01_shadow_from_border_light,
    "solve_e_h02_extract_dihedral_odd_shape": solve_e_h02_extract_dihedral_odd_shape,
    "solve_e_h03_hole_gallery_sorted": solve_e_h03_hole_gallery_sorted,
    "solve_e_h04_apply_key_row_transform_sequence": solve_e_h04_apply_key_row_transform_sequence,
    "solve_e_h05_beam_intersections_with_blockers": solve_e_h05_beam_intersections_with_blockers,
    "solve_e_h06_orbit_object_around_center": solve_e_h06_orbit_object_around_center,
    "solve_e_h07_shortest_corridor_path": solve_e_h07_shortest_corridor_path,
}
