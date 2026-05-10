"""Reference solvers for the third 21-task ARC-style puzzle bank."""


def blank(h, w, val=0):
    return [[val for _ in range(w)] for _ in range(h)]


def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def paste(g, shape, top, left):
    H, W = dims(g)
    h, w = dims(shape)
    for r in range(h):
        for c in range(w):
            v = shape[r][c]
            if v != 0:
                rr, cc = top + r, left + c
                assert 0 <= rr < H and 0 <= cc < W, (rr,cc,H,W)
                g[rr][cc] = v
    return g


def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate_180(g):
    return [row[::-1] for row in g[::-1]]


def rotate_times(g, k):
    out = g
    for _ in range(k % 4):
        out = rotate_cw(out)
    return out


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


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


def components(g):
    h,w=dims(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0:
                continue
            color=g[r][c]
            stack=[(r,c)]
            vis[r][c]=True
            cells=[]
            while stack:
                x,y=stack.pop()
                cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not vis[nx][ny] and g[nx][ny]==color:
                        vis[nx][ny]=True
                        stack.append((nx,ny))
            comps.append({"color": color, "cells": cells})
    return comps


def component_grid(comp):
    r0,r1,c0,c1 = bbox_cells(comp["cells"])
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in comp["cells"]:
        out[r-r0][c-c0]=comp["color"]
    return out


def count_nonzero(g):
    return sum(v!=0 for row in g for v in row)


def make_shape(coords, color):
    rs=[r for r,c in coords]; cs=[c for r,c in coords]
    h=max(rs)+1; w=max(cs)+1
    out=blank(h,w)
    for r,c in coords:
        out[r][c]=color
    return out


def points_grid(h, w, points):
    g=blank(h,w)
    for r,c,color in points:
        g[r][c]=color
    return g


def rect(color, h, w):
    return [[color]*w for _ in range(h)]


def frame(color, h, w):
    assert h>=3 and w>=3
    g=blank(h,w)
    for r in range(h):
        g[r][0]=color
        g[r][w-1]=color
    for c in range(w):
        g[0][c]=color
        g[h-1][c]=color
    return g


def is_frame(comp):
    cells=set(comp["cells"])
    r0,r1,c0,c1=bbox_cells(comp["cells"])
    h=r1-r0+1; w=c1-c0+1
    if h<3 or w<3:
        return False
    border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
    return cells==border


def recolor(shape, color):
    return [[color if v!=0 else 0 for v in row] for row in shape]


def solve_c_e1_seed_to_3x3(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr,nc=r+dr,c+dc
                        if 0<=nr<h and 0<=nc<w:
                            out[nr][nc]=color
    return out


def solve_c_e2_keep_bottommost_per_column(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        chosen=None
        for r in range(h-1,-1,-1):
            if g[r][c]!=0:
                chosen=(r,g[r][c])
                break
        if chosen:
            r,color=chosen
            out[r][c]=color
    return out


def solve_c_e3_right_pack_rows(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        out[r][w-len(vals):]=vals
    return out


def solve_c_e4_complete_2x2_L(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                color=nz[0]
                if vals[0]==0: out[r][c]=color
                if vals[1]==0: out[r][c+1]=color
                if vals[2]==0: out[r+1][c]=color
                if vals[3]==0: out[r+1][c+1]=color
    return out


def solve_c_e5_full_cross_from_seed(g):
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    assert len(seeds)>=1
    # examples use one seed or same-colored non-conflicting; later seeds overwrite but generators avoid conflict
    for r,c,color in seeds:
        for rr in range(h):
            out[rr][c]=color
        for cc in range(w):
            out[r][cc]=color
    return out


def solve_c_e6_fill_vertical_segments(g):
    h,w=dims(g)
    out=copy_grid(g)
    for c in range(w):
        positions=[(r,g[r][c]) for r in range(h) if g[r][c]!=0]
        # support multiple pairs by color if exactly two of a color in a column and nothing else between them
        bycolor={}
        for r,color in positions:
            bycolor.setdefault(color, []).append(r)
        for color,rows in bycolor.items():
            if len(rows)==2:
                r0,r1=sorted(rows)
                # all cells between are zero or same color endpoints only?
                if all(g[r][c]==0 for r in range(r0+1,r1)):
                    for r in range(r0,r1+1):
                        out[r][c]=color
    return out


def solve_c_e7_rotate_180(g):
    return rotate_180(g)


def solve_c_m1_recolor_by_aspect(g):
    out=blank(*dims(g))
    for comp in components(g):
        r0,r1,c0,c1=bbox_cells(comp["cells"])
        h=r1-r0+1; w=c1-c0+1
        if h>w:
            color=2
        elif w>h:
            color=3
        else:
            color=4
        for r,c in comp["cells"]:
            out[r][c]=color
    return out


def solve_c_m2_keep_frames_only(g):
    out=blank(*dims(g))
    for comp in components(g):
        if is_frame(comp):
            for r,c in comp["cells"]:
                out[r][c]=comp["color"]
    return out


def solve_c_m3_object_and_hmirror_strip(g):
    obj=crop_nonzero(g)
    mir=flip_h(obj)
    h1,w1=dims(obj); h2,w2=dims(mir)
    h=max(h1,h2)
    out=blank(h,w1+1+w2)
    paste(out,obj,0,0)
    paste(out,mir,0,w1+1)
    return out


def solve_c_m4_keep_even_area_objects(g):
    out=blank(*dims(g))
    for comp in components(g):
        if len(comp["cells"])%2==0:
            for r,c in comp["cells"]:
                out[r][c]=comp["color"]
    return out


def solve_c_m5_keep_largest_per_color(g):
    out=blank(*dims(g))
    groups={}
    for comp in components(g):
        groups.setdefault(comp["color"], []).append(comp)
    for color, comps in groups.items():
        comps_sorted=sorted(comps, key=lambda comp: (len(comp["cells"]), -bbox_cells(comp["cells"])[0], -bbox_cells(comp["cells"])[2]), reverse=True)
        best=comps_sorted[0]
        for r,c in best["cells"]:
            out[r][c]=color
    return out


def solve_c_m6_column_majority_row(g):
    h,w=dims(g)
    out=[[0]*w]
    for c in range(w):
        counts={}
        for r in range(h):
            v=g[r][c]
            if v!=0:
                counts[v]=counts.get(v,0)+1
        if counts:
            color=max(counts.items(), key=lambda kv: (kv[1], -kv[0]))[0]
            out[0][c]=color
    return out


def solve_c_m7_rotate_objects_in_square_boxes(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        r0,r1,c0,c1=bbox_cells(comp["cells"])
        sub=component_grid(comp)
        sh,sw=dims(sub)
        assert sh==sw, "generator should only use square bboxes"
        rot=rotate_cw(sub)
        paste(out,rot,r0,c0)
    return out


def solve_c_h1_stamp_rotated_template(g):
    h,w=dims(g)
    markers=[]
    g2=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in (1,2,3,4):
                # singleton marker
                same_neighbors=0
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]==v:
                        same_neighbors+=1
                if same_neighbors==0:
                    markers.append((r,c,v))
                    g2[r][c]=0
    template=crop_nonzero(g2)
    out=blank(h,w)
    for r,c,v in markers:
        stamp=rotate_times(template, v-1)
        paste(out,stamp,r,c)
    return out


def solve_c_h2_concat_frame_interiors(g):
    frames=sorted([comp for comp in components(g) if is_frame(comp)], key=lambda comp: bbox_cells(comp["cells"])[2])
    interiors=[]
    for comp in frames:
        r0,r1,c0,c1=bbox_cells(comp["cells"])
        interior=[row[c0+1:c1] for row in g[r0+1:r1]]
        interiors.append(interior)
    if not interiors:
        return [[0]]
    H=max(len(x) for x in interiors)
    W=sum(len(x[0]) for x in interiors)+max(0,len(interiors)-1)
    out=blank(H,W)
    cur=0
    for i,sub in enumerate(interiors):
        paste(out,sub,0,cur)
        cur+=len(sub[0])
        if i+1<len(interiors):
            cur+=1
    return out


def solve_c_h3_recolor_objects_by_marker_rank(g):
    h,w=dims(g)
    markers=[(c,g[0][c]) for c in range(w) if g[0][c]!=0]
    g2=copy_grid(g)
    for c,_ in markers:
        g2[0][c]=0
    objs=components(g2)
    objs_sorted=sorted(objs, key=lambda comp: (len(comp["cells"]), bbox_cells(comp["cells"])[0], bbox_cells(comp["cells"])[2]))
    assert len(objs_sorted)==len(markers)
    out=blank(h,w)
    for comp,(c,color) in zip(objs_sorted, sorted(markers)):
        for r,cc in comp["cells"]:
            out[r][cc]=color
    return out


def solve_c_h4_quadrant_mosaic(g):
    h,w=dims(g)
    mid_r=(h-1)/2.0
    mid_c=(w-1)/2.0
    slots={"TL":None,"TR":None,"BL":None,"BR":None}
    for comp in components(g):
        rs=[r for r,c in comp["cells"]]; cs=[c for r,c in comp["cells"]]
        cr=sum(rs)/len(rs); cc=sum(cs)/len(cs)
        key=("T" if cr<mid_r else "B")+("L" if cc<mid_c else "R")
        slots[key]=component_grid(comp)
    top_h=max((dims(x)[0] for x in [slots["TL"],slots["TR"]] if x is not None), default=1)
    bot_h=max((dims(x)[0] for x in [slots["BL"],slots["BR"]] if x is not None), default=1)
    left_w=max((dims(x)[1] for x in [slots["TL"],slots["BL"]] if x is not None), default=1)
    right_w=max((dims(x)[1] for x in [slots["TR"],slots["BR"]] if x is not None), default=1)
    out=blank(top_h+1+bot_h, left_w+1+right_w)
    if slots["TL"] is not None: paste(out, slots["TL"], 0, 0)
    if slots["TR"] is not None: paste(out, slots["TR"], 0, left_w+1)
    if slots["BL"] is not None: paste(out, slots["BL"], top_h+1, 0)
    if slots["BR"] is not None: paste(out, slots["BR"], top_h+1, left_w+1)
    return out


def solve_c_h5_flip_contents_by_frame_parity(g):
    out=copy_grid(g)
    for comp in components(g):
        if is_frame(comp):
            r0,r1,c0,c1=bbox_cells(comp["cells"])
            interior=[row[c0+1:c1] for row in g[r0+1:r1]]
            trans=flip_h(interior) if comp["color"]%2==1 else flip_v(interior)
            # blank interior then paste transformed
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=0
            paste(out, trans, r0+1, c0+1)
    return out


def solve_c_h6_perimeter_sort_rotated_strip(g):
    objs=[]
    for comp in components(g):
        sub=component_grid(comp)
        sh,sw=dims(sub)
        if sh>sw:
            sub=rotate_cw(sub)
            sh,sw=dims(sub)
        per=2*(sh+sw)
        r0,r1,c0,c1=bbox_cells(comp["cells"])
        objs.append((per, r0, c0, sub))
    objs.sort(key=lambda x: (-x[0], x[1], x[2]))  # descending perimeter, then reading order
    H=sum(dims(sub)[0] for _,_,_,sub in objs)+max(0,len(objs)-1)
    W=max(dims(sub)[1] for _,_,_,sub in objs)
    out=blank(H,W)
    cur=0
    for i,(_,_,_,sub) in enumerate(objs):
        paste(out,sub,cur,0)
        cur+=dims(sub)[0]
        if i+1<len(objs):
            cur+=1
    return out


def solve_c_h7_select_nth_largest_by_marker_count(g):
    h,w=dims(g)
    n=sum(1 for c in range(w) if g[0][c]==9)
    g2=copy_grid(g)
    for c in range(w):
        if g2[0][c]==9:
            g2[0][c]=0
    objs=components(g2)
    objs_sorted=sorted(objs, key=lambda comp: (len(comp["cells"]), bbox_cells(comp["cells"])[0], bbox_cells(comp["cells"])[2]), reverse=True)
    chosen=objs_sorted[n-1]
    return component_grid(chosen)

