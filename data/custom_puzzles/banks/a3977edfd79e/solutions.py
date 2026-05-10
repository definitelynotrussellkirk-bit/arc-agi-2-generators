"""Reference solvers for the second 21-task ARC-style puzzle bank."""
from copy import deepcopy

def blank(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def copy_grid(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def components(g):
    h,w=dims(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or vis[r][c]:
                continue
            color=g[r][c]
            stack=[(r,c)]
            vis[r][c]=True
            cells=[]
            while stack:
                x,y=stack.pop()
                cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not vis[nx][ny] and g[nx][ny]==color:
                        vis[nx][ny]=True
                        stack.append((nx,ny))
            comps.append({'color':color,'cells':cells})
    return comps

def bbox_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def component_grid(comp):
    r0,r1,c0,c1=bbox_cells(comp['cells'])
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in comp['cells']:
        out[r-r0][c-c0]=comp['color']
    return out

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    r0,r1=min(rs),max(rs); c0,c1=min(cs),max(cs)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_color_cells(g,color,exclude=None):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color and (exclude is None or (r,c) not in exclude)]
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox_cells(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=color
    return out

def paste(g, shape, top, left):
    h,w=dims(shape)
    H,W=dims(g)
    for r in range(h):
        for c in range(w):
            v=shape[r][c]
            if v!=0:
                rr,cc=top+r,left+c
                if not (0<=rr<H and 0<=cc<W):
                    raise ValueError(f"paste out of bounds {rr,cc} in {H,W}")
                g[rr][cc]=v
    return g

def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_times(g,k):
    out=g
    for _ in range(k%4):
        out=rotate_cw(out)
    return out

def transpose_square(g):
    h,w=dims(g)
    assert h==w
    return [[g[c][r] for c in range(w)] for r in range(h)]

def is_frame(comp):
    cells=set(comp['cells'])
    r0,r1,c0,c1=bbox_cells(comp['cells'])
    h=r1-r0+1; w=c1-c0+1
    if h<3 or w<3:
        return False
    border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
    return cells==border

def center_coords(container_top, container_left, container_h, container_w, shape_h, shape_w):
    top=container_top + (container_h-shape_h)//2
    left=container_left + (container_w-shape_w)//2
    return top,left

def solve_b2_e1_full_row(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        colors=[v for v in row if v!=0]
        if colors:
            # assume exactly one nonzero color cell in row
            color=colors[0]
            out[r]=[color]*w
    return out

def solve_b2_e2_singletons_to_plus(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color==0: 
                continue
            # isolated singleton in 4-neighborhood
            if all(not (0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]==color) for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]):
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=color
    return out

def solve_b2_e3_remove_border_objects(g):
    h,w=dims(g)
    out=copy_grid(g)
    for comp in components(g):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=0
    return out

def solve_b2_e4_outline_rectangles(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        color=comp['color']
        r0,r1,c0,c1=bbox_cells(comp['cells'])
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
    return out

def solve_b2_e5_shift_down_right(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and r+1<h and c+1<w:
                out[r+1][c+1]=g[r][c]
    return out

def solve_b2_e6_transpose_square(g):
    return transpose_square(g)

def solve_b2_e7_fill_single_gap(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            horiz = c-1>=0 and c+1<w and g[r][c-1]==g[r][c+1]!=0
            vert = r-1>=0 and r+1<h and g[r-1][c]==g[r+1][c]!=0
            if horiz and not vert:
                out[r][c]=g[r][c-1]
            elif vert and not horiz:
                out[r][c]=g[r-1][c]
            elif horiz and vert:
                # examples avoid conflict; if same color, fill it
                if g[r][c-1]==g[r-1][c]:
                    out[r][c]=g[r][c-1]
    return out

def solve_b2_m1_select_color_crop(g):
    marker=g[0][0]
    exclude={(0,0)}
    return crop_color_cells(g, marker, exclude=exclude)

def solve_b2_m2_bbox_outlines(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        color=comp['color']
        r0,r1,c0,c1=bbox_cells(comp['cells'])
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
    return out

def solve_b2_m3_rotate_by_key(g):
    key=g[0][0]
    # crop all nonzero except key
    gg=copy_grid(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    # 1->90 cw, 2->180, 3->270 cw
    return rotate_times(obj, key)

def solve_b2_m4_swap_two_objects(g):
    comps=components(g)
    assert len(comps)==2
    comps_sorted=sorted(comps, key=lambda comp: bbox_cells(comp['cells'])[2])  # leftmost first
    a,b=comps_sorted
    a_r0,a_r1,a_c0,a_c1=bbox_cells(a['cells'])
    b_r0,b_r1,b_c0,b_c1=bbox_cells(b['cells'])
    ashape=component_grid(a)
    bshape=component_grid(b)
    out=blank(*dims(g))
    paste(out, ashape, b_r0, b_c0)
    paste(out, bshape, a_r0, a_c0)
    return out

def solve_b2_m5_recolor_by_size_rank(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda comp: len(comp['cells']))
    palette=[2,4,8]
    out=blank(*dims(g))
    for rank,comp in enumerate(comps_sorted):
        color=palette[rank]
        for r,c in comp['cells']:
            out[r][c]=color
    return out

def solve_b2_m6_corner_marker_select_quadrant(g):
    h,w=dims(g)
    assert h>=6 and w>=6
    # inner body rows 1:h-1, cols1:w-1; assume even dims 4x4 or 6x6 etc
    body=[row[1:w-1] for row in g[1:h-1]]
    bh,bw=dims(body)
    hh,hw=bh//2,bw//2
    marker_positions=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    pos=None
    for r,c in marker_positions:
        if g[r][c]!=0:
            pos=(r,c); break
    if pos==(0,0):
        return [row[:hw] for row in body[:hh]]
    if pos==(0,w-1):
        return [row[hw:] for row in body[:hh]]
    if pos==(h-1,0):
        return [row[:hw] for row in body[hh:]]
    if pos==(h-1,w-1):
        return [row[hw:] for row in body[hh:]]
    raise ValueError("no corner marker")

def solve_b2_m7_column_gravity(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out

def solve_b2_h1_stack_by_area_vertical(g):
    comps=components(g)
    shapes=[component_grid(comp) for comp in comps]
    items=sorted(zip(comps,shapes), key=lambda cs: len(cs[0]['cells']), reverse=True)
    widths=[dims(shape)[1] for comp,shape in items]
    heights=[dims(shape)[0] for comp,shape in items]
    out_h=sum(heights)+max(0,len(items)-1)
    out_w=max(widths) if widths else 1
    out=blank(out_h,out_w)
    r=0
    for idx,(comp,shape) in enumerate(items):
        sh,sw=dims(shape)
        paste(out, shape, r, 0)
        r += sh + 1
    return out

def solve_b2_h2_match_objects_to_frames_by_color(g):
    h,w=dims(g)
    comps=components(g)
    frames=[comp for comp in comps if is_frame(comp)]
    objs=[comp for comp in comps if not is_frame(comp)]
    out=blank(h,w)
    # draw frames
    for frame in frames:
        for r,c in frame['cells']:
            out[r][c]=frame['color']
    # match by color
    for frame in frames:
        color=frame['color']
        matches=[comp for comp in objs if comp['color']==color]
        assert len(matches)==1
        obj_shape=component_grid(matches[0])
        r0,r1,c0,c1=bbox_cells(frame['cells'])
        itop,ileft= r0+1, c0+1
        ih,iw = (r1-r0-1), (c1-c0-1)
        sh,sw=dims(obj_shape)
        top,left=center_coords(itop, ileft, ih, iw, sh, sw)
        paste(out, obj_shape, top, left)
    return out

def solve_b2_h3_replicate_template_by_marker_count(g):
    h,w=dims(g)
    marker_count=sum(1 for v in g[0] if v!=0)
    body=copy_grid(g)
    for c in range(w): body[0][c]=0
    template=crop_nonzero(body)
    th,tw=dims(template)
    out=blank(th, marker_count*tw + max(0,marker_count-1))
    c=0
    for i in range(marker_count):
        paste(out, template, 0, c)
        c += tw + 1
    return out

def solve_b2_h4_pack_by_marker_sequence(g):
    seq=[v for v in g[0] if v!=0]
    body=copy_grid(g)
    for c in range(len(body[0])): body[0][c]=0
    comps=components(body)
    by_color={}
    for comp in comps:
        by_color.setdefault(comp['color'], []).append(comp)
    shapes=[]
    for color in seq:
        assert color in by_color and len(by_color[color])==1
        shapes.append(component_grid(by_color[color][0]))
    out_h=max(dims(shape)[0] for shape in shapes) if shapes else 1
    out_w=sum(dims(shape)[1] for shape in shapes) + max(0,len(shapes)-1)
    out=blank(out_h,out_w)
    c=0
    for shape in shapes:
        paste(out, shape, 0, c)
        c += dims(shape)[1] + 1
    return out

def solve_b2_h5_recolor_object_by_inner_seed(g):
    out=copy_grid(g)
    for frame in [comp for comp in components(g) if is_frame(comp)]:
        r0,r1,c0,c1=bbox_cells(frame['cells'])
        interior=[(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]
        colors={}
        for r,c in interior:
            v=g[r][c]
            if v!=0:
                colors.setdefault(v, []).append((r,c))
        if not colors:
            continue
        # choose singleton color as seed
        seed_color=None
        for color,cells in colors.items():
            if len(cells)==1:
                seed_color=color
                break
        assert seed_color is not None
        for color,cells in colors.items():
            if color==seed_color:
                continue
            for r,c in cells:
                out[r][c]=seed_color
    return out

def solve_b2_h6_match_objects_to_frames_by_size(g):
    h,w=dims(g)
    comps=components(g)
    frames=[comp for comp in comps if is_frame(comp)]
    objs=[comp for comp in comps if not is_frame(comp)]
    frames_sorted=sorted(frames, key=lambda comp: (bbox_cells(comp['cells'])[1]-bbox_cells(comp['cells'])[0]-1) * (bbox_cells(comp['cells'])[3]-bbox_cells(comp['cells'])[2]-1))
    objs_sorted=sorted(objs, key=lambda comp: len(comp['cells']))
    assert len(frames_sorted)==len(objs_sorted)
    out=blank(h,w)
    for frame in frames_sorted:
        for r,c in frame['cells']:
            out[r][c]=frame['color']
    for frame,obj in zip(frames_sorted, objs_sorted):
        shape=component_grid(obj)
        r0,r1,c0,c1=bbox_cells(frame['cells'])
        itop,ileft=r0+1,c0+1
        ih,iw=(r1-r0-1),(c1-c0-1)
        sh,sw=dims(shape)
        top,left=center_coords(itop, ileft, ih, iw, sh, sw)
        paste(out, shape, top, left)
    return out

def solve_b2_h7_swap_frame_contents(g):
    h,w=dims(g)
    frames=[comp for comp in components(g) if is_frame(comp)]
    assert len(frames)==2
    # extract contents inside each frame (nonzero, excluding frame)
    contents=[]
    out=blank(h,w)
    for frame in frames:
        for r,c in frame['cells']:
            out[r][c]=frame['color']
        r0,r1,c0,c1=bbox_cells(frame['cells'])
        interior=blank(r1-r0-1, c1-c0-1)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0:
                    interior[r-(r0+1)][c-(c0+1)] = g[r][c]
        contents.append(crop_nonzero(interior))
    # swap and center
    for frame,shape in zip(frames, contents[::-1]):
        r0,r1,c0,c1=bbox_cells(frame['cells'])
        itop,ileft=r0+1,c0+1
        ih,iw=(r1-r0-1),(c1-c0-1)
        sh,sw=dims(shape)
        top,left=center_coords(itop, ileft, ih, iw, sh, sw)
        paste(out, shape, top, left)
    return out

SOLVERS = {
    'easy_b01': solve_b2_e1_full_row,
    'easy_b02': solve_b2_e2_singletons_to_plus,
    'easy_b03': solve_b2_e3_remove_border_objects,
    'easy_b04': solve_b2_e4_outline_rectangles,
    'easy_b05': solve_b2_e5_shift_down_right,
    'easy_b06': solve_b2_e6_transpose_square,
    'easy_b07': solve_b2_e7_fill_single_gap,
    'medium_b01': solve_b2_m1_select_color_crop,
    'medium_b02': solve_b2_m2_bbox_outlines,
    'medium_b03': solve_b2_m3_rotate_by_key,
    'medium_b04': solve_b2_m4_swap_two_objects,
    'medium_b05': solve_b2_m5_recolor_by_size_rank,
    'medium_b06': solve_b2_m6_corner_marker_select_quadrant,
    'medium_b07': solve_b2_m7_column_gravity,
    'hard_b01': solve_b2_h1_stack_by_area_vertical,
    'hard_b02': solve_b2_h2_match_objects_to_frames_by_color,
    'hard_b03': solve_b2_h3_replicate_template_by_marker_count,
    'hard_b04': solve_b2_h4_pack_by_marker_sequence,
    'hard_b05': solve_b2_h5_recolor_object_by_inner_seed,
    'hard_b06': solve_b2_h6_match_objects_to_frames_by_size,
    'hard_b07': solve_b2_h7_swap_frame_contents,
}

if __name__ == '__main__':
    print('Available solvers:')
    for k in sorted(SOLVERS):
        print(' -', k, '->', SOLVERS[k].__name__)
