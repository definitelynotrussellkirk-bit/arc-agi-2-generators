from __future__ import annotations

import collections
import inspect
import json
from pathlib import Path

DIR4=[(-1,0),(1,0),(0,-1),(0,1)]


def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def size(g):
    return len(g), len(g[0]) if g else 0


def strings_from_grid(g):
    return ["".join(str(c) for c in row) for row in g]


def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(g, cells=None, pad=0):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    r0=max(0,r0-pad); c0=max(0,c0-pad); r1=min(len(g)-1,r1+pad); c1=min(len(g[0])-1,c1+pad)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def fill_rect(g,r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color


def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color


def orth_neighbors(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc


def components_of_color(g, color):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]!=color:
                continue
            vis[r][c]=True
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]==color:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            comps.append(cells)
    return comps


def components_nonzero(g, treat_colors_separately=False):
    h,w=size(g)
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0:
                continue
            color=g[r][c]
            vis[r][c]=True
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and g[nr][nc]!=0 and (not treat_colors_separately or g[nr][nc]==color):
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            comps.append((color,cells))
    return comps


def rotate_cw(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate_times(g, k):
    k%=4
    out=g
    for _ in range(k):
        out=rotate_cw(out)
    return out


def flip_h(g):
    return g[::-1]


def flip_v(g):
    return [row[::-1] for row in g]


def reflect_anti_diag(g):
    h,w=size(g)
    assert h==w
    return [[g[w-1-c][h-1-r] for c in range(w)] for r in range(h)]


def crop_nonzero(g):
    return crop_bbox(g)


def cells_dims(cells):
    if not cells:
        return 1,1
    if len(cells[0])==3:
        rs=[r for r,c,v in cells]; cs=[c for r,c,v in cells]
    else:
        rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return max(rs)+1, max(cs)+1


def apply_transform_to_cells(cells, transform):
    if not cells:
        return []
    pts=[]
    for t in cells:
        if len(t)==3:
            pts.append(t)
        else:
            pts.append((t[0],t[1],1))
    h,w=cells_dims(pts)
    out=[]
    for r,c,v in pts:
        if transform=='id':
            nr,nc=r,c
        elif transform=='rot90':
            nr,nc=c,h-1-r
        elif transform=='rot180':
            nr,nc=h-1-r,w-1-c
        elif transform=='rot270':
            nr,nc=w-1-c,r
        elif transform=='flip_h':
            nr,nc=h-1-r,c
        elif transform=='flip_v':
            nr,nc=r,w-1-c
        elif transform=='anti':
            nr,nc=w-1-c,h-1-r
        else:
            raise ValueError(transform)
        out.append((nr,nc,v))
    minr=min(r for r,c,v in out); minc=min(c for r,c,v in out)
    return [(r-minr,c-minc,v) for r,c,v in out]


def normalize_component(g, color=None, cells=None):
    if cells is None:
        if color is None:
            cells=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
        else:
            cells=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
    if not cells:
        return []
    rs=[r for r,c,v in cells]; cs=[c for r,c,v in cells]
    r0,c0=min(rs), min(cs)
    return [(r-r0,c-c0,v) for r,c,v in cells]


def hole_count_of_cells(cells):
    if not cells:
        return 0
    r0,c0,r1,c1=bbox(cells)
    h,w=r1-r0+1, c1-c0+1
    mat=blank(h,w,0)
    for r,c in cells:
        mat[r-r0][c-c0]=1
    vis=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if vis[r][c] or mat[r][c]==1:
                continue
            vis[r][c]=True
            stack=[(r,c)]
            touch=(r==0 or r==h-1 or c==0 or c==w-1)
            while stack:
                rr,cc=stack.pop()
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if not vis[nr][nc] and mat[nr][nc]==0:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
                        if nr==0 or nr==h-1 or nc==0 or nc==w-1:
                            touch=True
            if not touch:
                holes+=1
    return holes


def paste(g, pat, r0, c0):
    out=clone(g)
    if pat and isinstance(pat[0], str):
        pat=grid_from_strings(pat)
    for r,row in enumerate(pat):
        for c,v in enumerate(row):
            if v!=0:
                out[r0+r][c0+c]=v
    return out


def is_solid_rect_component(cells):
    r0,c0,r1,c1=bbox(cells)
    return len(cells)==(r1-r0+1)*(c1-c0+1)


def is_rect_border(cells):
    r0,c0,r1,c1=bbox(cells)
    expected=set()
    for c in range(c0,c1+1):
        expected.add((r0,c)); expected.add((r1,c))
    for r in range(r0,r1+1):
        expected.add((r,c0)); expected.add((r,c1))
    return set(cells)==expected


def trace_polyline(points, mode='hv'):
    out=[]
    if not points:
        return out
    out.append(points[0])
    for (r1,c1),(r2,c2) in zip(points, points[1:]):
        if mode=='hv':
            step = 1 if c2>=c1 else -1
            for c in range(c1+step, c2+step, step):
                out.append((r1,c))
            step = 1 if r2>=r1 else -1
            for r in range(r1+step, r2+step, step):
                out.append((r,c2))
        else:
            step = 1 if r2>=r1 else -1
            for r in range(r1+step, r2+step, step):
                out.append((r,c1))
            step = 1 if c2>=c1 else -1
            for c in range(c1+step, c2+step, step):
                out.append((r2,c))
    seen=[]; used=set()
    for p in out:
        if p not in used:
            used.add(p); seen.append(p)
    return seen


def center_stamp(base, template_cells, frame_box, recolor='keep'):
    out=clone(base)
    if not template_cells:
        return out
    if len(template_cells[0])!=3:
        template_cells=[(r,c,1) for r,c in template_cells]
    th,tw=cells_dims(template_cells)
    r0,c0,r1,c1=frame_box
    ih,iw=r1-r0-1, c1-c0-1
    sr=r0+1 + (ih-th)//2
    sc=c0+1 + (iw-tw)//2
    frame_color=out[r0][c0]
    for rr,cc,v in template_cells:
        r,c=sr+rr, sc+cc
        if 0<=r<len(out) and 0<=c<len(out[0]):
            out[r][c] = frame_color if recolor=='frame' else v
    return out


# New primitive for this set

def trace_polyline_markers(base_grid, marker_groups, mode='hv', intersection_color=None):
    """
    marker_groups: iterable of (color, [(r,c), ...]) where each point list is ordered.
    Draw a polyline through each color's markers using horizontal-then-vertical
    (or vertical-then-horizontal) Manhattan segments. If intersection_color is
    given, cells occupied by 2+ colors are recolored to that value.
    """
    h,w=size(base_grid)
    out=clone(base_grid)
    counts=collections.Counter()
    owners={}
    for color,points in marker_groups:
        for r,c in trace_polyline(points, mode):
            if 0<=r<h and 0<=c<w:
                counts[(r,c)]+=1
                if counts[(r,c)]==1:
                    owners[(r,c)]=color
                elif intersection_color is not None:
                    owners[(r,c)]=intersection_color
    for (r,c),v in owners.items():
        out[r][c]=v
    return out


# === Rules ===

def rule_e43(g):
    h,w=size(g)
    out=clone(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                for dr,dc in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out


def rule_e44(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0:
                continue
            for dr,dc in [(2,2),(2,-2)]:
                nr,nc=r+dr,c+dc
                mr,mc=r+dr//2,c+dc//2
                if 0<=nr<h and 0<=nc<w and g[nr][nc]==v and out[mr][mc]==0:
                    out[mr][mc]=v
    return out


def rule_e45(g):
    h,w=size(g)
    out=blank(h,w)
    for c,v in enumerate(g[0]):
        if v!=0:
            for r in range(h):
                out[r][c]=v
    return out


def rule_e46(g):
    h,w=size(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        if len(cells)!=4:
            continue
        r0,c0,r1,c1=bbox(cells)
        corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}
        if set(cells)==corners:
            fill_rect(out,r0,c0,r1,c1,color)
    return out


def rule_e47(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==0:
                continue
            if any(g[nr][nc]==v for nr,nc in orth_neighbors(r,c,h,w)):
                out[r][c]=v
    return out


def rule_e48(g):
    h,w=size(g)
    assert h==w
    ref=reflect_anti_diag(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]==0 and ref[r][c]!=0:
                out[r][c]=ref[r][c]
    return out


def rule_e49(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=None)


def rule_m43(g):
    sel=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==sel and not (r==0 and c==0)]
    return crop_bbox(g, cells)


def rule_m44(g):
    h,w=size(g)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if len(cells)>=8 and is_rect_border(cells):
            frame=(color,bbox(cells))
            break
    assert frame is not None
    fcolor,(r0,c0,r1,c1)=frame
    interior=sorted((r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]!=0)
    a=interior[0][2]; b=interior[1][2]
    out=blank(h,w)
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            out[r][c]=a if ((r-(r0+1)) + (c-(c0+1)))%2==0 else b
    return out


def rule_m45(g):
    cmd=g[0][0]
    base=clone(g); base[0][0]=0
    cropped=crop_nonzero(base)
    return rotate_times(cropped, {1:0,2:1,3:2,4:3}[cmd])


def rule_m46(g):
    h,w=size(g)
    rows=[g[r][0] for r in range(1,h)]
    cols=g[0][1:]
    out=blank(len(rows), len(cols))
    for r,rv in enumerate(rows):
        for c,cv in enumerate(cols):
            out[r][c]=rv if rv==cv else 0
    return out


def rule_m47(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_solid_rect_component(cells):
            r0,c0,r1,c1=bbox(cells)
            crop=[row[c0:c1+1] for row in g[r0:r1+1]]
            comps.append((len(cells), color, crop))
    comps.sort(key=lambda x:(x[0], x[1]))
    maxh=max(len(crop) for _,_,crop in comps)
    totalw=sum(len(crop[0]) for _,_,crop in comps)+max(0,len(comps)-1)
    out=blank(maxh,totalw)
    x=0
    for _,_,crop in comps:
        h,w=size(crop)
        for r in range(h):
            for c in range(w):
                out[r][x+c]=crop[r][c]
        x += w+1
    return out


def rule_m48(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=None)


def rule_m49(g):
    h,w=size(g)
    source=None
    for comp in components_of_color(g,2):
        if not is_rect_border(comp):
            source=comp
            break
    assert source is not None
    templ=normalize_component(g, cells=[(r,c,2) for r,c in source])
    out=blank(h,w)
    for color in sorted({v for row in g for v in row if v not in (0,2)}):
        for comp in components_of_color(g,color):
            if is_rect_border(comp):
                box=bbox(comp)
                draw_rect_border(out,*box,color)
                out=center_stamp(out, templ, box, recolor='frame')
    return out


def rule_h43(g):
    h,w=size(g)
    sel=g[0][0]
    cmd=g[0][-1]
    comps=[comp for comp in components_of_color(g,sel) if (0,0) not in comp]
    sel_comp=max(comps, key=len)
    templ=normalize_component(g, cells=[(r,c,sel) for r,c in sel_comp])
    templ=apply_transform_to_cells(templ, {1:'id',2:'rot90',3:'rot180',4:'rot270'}[cmd])
    out=blank(h,w)
    for color in sorted({v for row in g for v in row if v not in (0,sel,cmd)}):
        for comp in components_of_color(g,color):
            if (0,0) in comp or (0,w-1) in comp:
                continue
            if is_rect_border(comp):
                box=bbox(comp)
                draw_rect_border(out,*box,color)
                out=center_stamp(out, templ, box, recolor='frame')
    return out


def rule_h44(g):
    comp2=max(components_of_color(g,2), key=len)
    comp3=max(components_of_color(g,3), key=len)
    n2={(r,c) for r,c,_ in normalize_component(g, cells=[(r,c,2) for r,c in comp2])}
    n3={(r,c) for r,c,_ in normalize_component(g, cells=[(r,c,3) for r,c in comp3])}
    pts=sorted(n2 & n3)
    if not pts:
        return [[0]]
    h=max(r for r,c in pts)+1; w=max(c for r,c in pts)+1
    out=blank(h,w)
    for r,c in pts:
        out[r][c]=8
    return out


def rule_h45(g):
    legend=[v for v in g[0] if v!=0][:3]
    h,w=size(g)
    out=blank(h,w)
    out[0]=g[0][:]
    vis=[[False]*w for _ in range(h)]
    for r in range(1,h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0:
                continue
            vis[r][c]=True
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if nr>=1 and not vis[nr][nc] and g[nr][nc]!=0:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            holes=hole_count_of_cells(cells)
            color=legend[min(holes,2)]
            for rr,cc in cells:
                out[rr][cc]=color
    return out


def rule_h46(g):
    h,w=size(g)
    out=blank(h,w)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frame=(color,bbox(cells))
            break
    assert frame is not None
    fcolor,(r0,c0,r1,c1)=frame
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and v!=fcolor and not (r==0 or c==0 or r==h-1 or c==w-1)]
    assert len(seeds)==2
    (rA,cA,vA),(rB,cB,vB)=seeds
    out[rA][cA]=vA; out[rB][cB]=vB
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if (r,c) in [(rA,cA),(rB,cB)]:
                continue
            if abs(r-rA)+abs(c-cA) == abs(r-rB)+abs(c-cB):
                out[r][c]=9
    return out


def rule_h47(g):
    cmd_rot=g[0][0]
    cmd_flip=g[0][-1]
    base=clone(g); base[0][0]=0; base[0][-1]=0
    cropped=crop_nonzero(base)
    out=rotate_times(cropped, {1:0,2:1,3:2,4:3}[cmd_rot])
    out=flip_h(out) if cmd_flip==1 else flip_v(out)
    return out


def rule_h48(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=False):
        crop=crop_bbox(g, cells)
        holes=hole_count_of_cells(cells)
        area=len(cells)
        comps.append((holes, area, color, crop))
    comps.sort(key=lambda x:(x[0], x[1], x[2]))
    maxh=max(len(crop) for _,_,_,crop in comps)
    totalw=sum(len(crop[0]) for _,_,_,crop in comps)+max(0,len(comps)-1)
    out=blank(maxh,totalw)
    x=0
    for _,_,_,crop in comps:
        h,w=size(crop)
        for r in range(h):
            for c in range(w):
                out[r][x+c]=crop[r][c]
        x += w+1
    return out


def rule_h49(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=9)


# === Pattern templates ===
PAT_L = grid_from_strings([
    "20",
    "20",
    "22",
])
PAT_Z = grid_from_strings([
    "330",
    "033",
])
PAT_T = grid_from_strings([
    "444",
    "040",
    "040",
])
PAT_MULTI1 = grid_from_strings([
    "230",
    "233",
    "030",
])
PAT_MULTI2 = grid_from_strings([
    "440",
    "040",
    "044",
])
PAT_MULTI3 = grid_from_strings([
    "560",
    "556",
    "006",
])
SHAPE_0 = grid_from_strings([
    "700",
    "770",
    "070",
])
SHAPE_1 = grid_from_strings([
    "888",
    "808",
    "888",
])
SHAPE_2 = grid_from_strings([
    "9999999",
    "9009009",
    "9009009",
    "9009009",
    "9999999",
])


# === Builders ===

def build_e43(h,w,seeds):
    g=blank(h,w)
    for r,c,color in seeds:
        g[r][c]=color
    return g


def build_e44(h,w,pairs):
    g=blank(h,w)
    for r1,c1,r2,c2,color in pairs:
        g[r1][c1]=color; g[r2][c2]=color
    return g


def build_e45(h,w,headers):
    g=blank(h,w)
    for c,color in headers:
        g[0][c]=color
    return g


def build_e46(h,w,rects):
    g=blank(h,w)
    for r0,c0,r1,c1,color in rects:
        for rr,cc in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            g[rr][cc]=color
    return g


def build_e47(h,w,cells):
    g=blank(h,w)
    for r,c,color in cells:
        g[r][c]=color
    return g


def build_e48(n,cells):
    g=blank(n,n)
    for r,c,color in cells:
        g[r][c]=color
    return g


def build_e49(h,w,color,points):
    g=blank(h,w)
    for r,c in points:
        g[r][c]=color
    return g


def build_m43(h,w,selector,placements):
    g=blank(h,w)
    g[0][0]=selector
    for color, pat, r0, c0 in placements:
        patg=[[color if v!=0 else 0 for v in row] for row in pat]
        g=paste(g, patg, r0, c0)
    return g


def build_m44(h,w,frame,seed_a,seed_b):
    # frame = (r0,c0,r1,c1,color)
    g=blank(h,w)
    r0,c0,r1,c1,color=frame
    draw_rect_border(g,r0,c0,r1,c1,color)
    g[seed_a[0]][seed_a[1]]=seed_a[2]
    g[seed_b[0]][seed_b[1]]=seed_b[2]
    return g


def build_m45(h,w,cmd,pat,r0,c0):
    g=blank(h,w)
    g[0][0]=cmd
    return paste(g, pat, r0, c0)


def build_m46(rows, cols):
    h,w=len(rows)+1, len(cols)+1
    g=blank(h,w)
    for i,v in enumerate(cols, start=1):
        g[0][i]=v
    for i,v in enumerate(rows, start=1):
        g[i][0]=v
    return g


def build_m47(h,w,rects):
    g=blank(h,w)
    for r0,c0,r1,c1,color in rects:
        fill_rect(g,r0,c0,r1,c1,color)
    return g


def build_m48(h,w,groups):
    g=blank(h,w)
    for color,points in groups:
        for r,c in points:
            g[r][c]=color
    return g


def build_m49(h,w,template_pat,template_offset,frames):
    g=blank(h,w)
    g=paste(g, template_pat, *template_offset)
    # template_pat assumed nonzero cells should become color 2
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                g[r][c]=2
    for r0,c0,r1,c1,color in frames:
        draw_rect_border(g,r0,c0,r1,c1,color)
    return g


def build_h43(h,w,selector,cmd,source_pat,source_offset,other_pats,frames):
    g=blank(h,w)
    g[0][0]=selector
    g[0][w-1]=cmd
    # source pattern in selector color
    src=[[selector if v!=0 else 0 for v in row] for row in source_pat]
    g=paste(g, src, *source_offset)
    for color,pat,off in other_pats:
        p=[[color if v!=0 else 0 for v in row] for row in pat]
        g=paste(g, p, *off)
    for r0,c0,r1,c1,color in frames:
        draw_rect_border(g,r0,c0,r1,c1,color)
    return g


def build_h44(h,w,pat2,off2,pat3,off3):
    g=blank(h,w)
    p2=[[2 if v!=0 else 0 for v in row] for row in pat2]
    p3=[[3 if v!=0 else 0 for v in row] for row in pat3]
    g=paste(g,p2,*off2)
    g=paste(g,p3,*off3)
    return g


def build_h45(h,w,legend,placements):
    g=blank(h,w)
    # legend: list of 3 colors in row0 spaced or contiguous
    for i,v in enumerate(legend):
        g[0][i]=v
    for pat,r0,c0 in placements:
        g=paste(g, pat, r0, c0)
    return g


def build_h46(h,w,frame,seeds):
    g=blank(h,w)
    r0,c0,r1,c1,color=frame
    draw_rect_border(g,r0,c0,r1,c1,color)
    for r,c,v in seeds:
        g[r][c]=v
    return g


def build_h47(h,w,cmd_rot,cmd_flip,pat,offset):
    g=blank(h,w)
    g[0][0]=cmd_rot
    g[0][w-1]=cmd_flip
    return paste(g, pat, *offset)


def build_h48(h,w,placements):
    g=blank(h,w)
    for pat,offset in placements:
        g=paste(g, pat, *offset)
    return g


def build_h49(h,w,groups):
    g=blank(h,w)
    for color,points in groups:
        for r,c in points:
            g[r][c]=color
    return g


# === Puzzle definitions ===

def make_puzzle(pid, title, difficulty, skills, staged_hint, written_solution, uses_new_primitive, rule_fn, train_inputs, test_input):
    return {
        'id': pid,
        'title': title,
        'difficulty': difficulty,
        'skills': skills,
        'staged_hint': staged_hint,
        'written_solution': written_solution,
        'uses_new_primitive': uses_new_primitive,
        'program_name': rule_fn.__name__,
        'program_source': inspect.getsource(rule_fn).rstrip(),
        'train': [{'input': strings_from_grid(inp), 'output': strings_from_grid(rule_fn(inp))} for inp in train_inputs],
        'test': {'input': strings_from_grid(test_input), 'output': strings_from_grid(rule_fn(test_input))},
    }


PUZZLES=[]

# Easy 43-49
PUZZLES.append(make_puzzle(
    'E43','Distance-2 Cross Echo','easy',
    ['local projection','fixed offset','same-color expansion'],
    'Ignore the empty cells first. Ask what new cells each seed paints at a fixed distance.',
    'Keep every seed. For each nonzero cell, also paint the cells exactly two steps north, south, east, and west with the same color, when those positions stay inside the grid.',
    False, rule_e43,
    [
        build_e43(8,9,[(1,2,4),(5,6,7)]),
        build_e43(7,10,[(2,4,3),(4,1,6),(1,8,2)]),
        build_e43(9,9,[(0,4,5),(6,6,8)]),
        build_e43(8,8,[(3,3,9),(6,1,2)])
    ],
    build_e43(9,10,[(2,2,4),(4,7,6),(7,4,3)])
))

PUZZLES.append(make_puzzle(
    'E44','Diagonal Midpoint Fill','easy',
    ['diagonal relation','midpoint inference','same-color completion'],
    'Look for same-colored cells that sit at opposite corners of a 3x3 diagonal. Only one cell is missing.',
    'Whenever two identical colors appear with row and column differences of 2 on a diagonal, fill the midpoint between them with that same color. Keep all existing cells.',
    False, rule_e44,
    [
        build_e44(7,8,[(1,1,3,3,2),(1,6,3,4,5)]),
        build_e44(8,8,[(2,2,4,4,7),(5,1,7,3,3)]),
        build_e44(9,9,[(0,2,2,4,6),(3,7,5,5,4),(6,1,8,3,8)]),
        build_e44(8,10,[(1,8,3,6,9),(4,2,6,4,1)])
    ],
    build_e44(9,10,[(1,1,3,3,2),(2,8,4,6,5),(5,2,7,4,7)])
))

PUZZLES.append(make_puzzle(
    'E45','Header Column Flood','easy',
    ['row guide','column selection','constant fill'],
    'Only the top row matters. Treat each nonzero header as an instruction for its whole column.',
    'Copy each nonzero cell in the top row straight down through the entire column. All other columns stay zero.',
    False, rule_e45,
    [
        build_e45(7,9,[(1,2),(4,5),(7,8)]),
        build_e45(8,8,[(0,3),(3,6),(6,9)]),
        build_e45(6,10,[(2,4),(5,7),(8,1)]),
        build_e45(9,7,[(1,8),(5,2)])
    ],
    build_e45(8,10,[(0,6),(4,3),(6,9),(9,2)])
))

PUZZLES.append(make_puzzle(
    'E46','Solid Rectangle From Corners','easy',
    ['corner detection','rectangle completion','solid fill'],
    'Do not search for lines first; search for four same-colored corners that already define a box.',
    'Each color marks the four corners of an axis-aligned rectangle. Fill the full rectangle, including its interior, with that color.',
    False, rule_e46,
    [
        build_e46(8,10,[(1,1,3,4,2),(4,6,6,8,5)]),
        build_e46(9,9,[(0,5,2,7,4),(4,1,7,3,8)]),
        build_e46(7,11,[(1,2,5,5,3)]),
        build_e46(10,10,[(2,2,4,4,7),(5,6,8,8,6)])
    ],
    build_e46(9,11,[(1,1,4,3,2),(2,7,6,9,5)])
))

PUZZLES.append(make_puzzle(
    'E47','Remove Isolated Cells','easy',
    ['local filtering','orthogonal adjacency','noise removal'],
    'Check each colored cell locally. The question is whether it has a same-colored orthogonal friend.',
    'Keep a nonzero cell only if at least one orthogonally adjacent cell has the same color. Delete isolated singletons.',
    False, rule_e47,
    [
        build_e47(8,9,[(1,1,2),(1,2,2),(3,4,5),(5,5,7),(5,6,7),(6,6,7),(2,7,4)]),
        build_e47(7,10,[(0,0,3),(2,2,6),(2,3,6),(4,6,8),(5,6,8),(6,9,1)]),
        build_e47(9,9,[(1,4,9),(2,4,9),(4,1,2),(4,2,2),(4,3,2),(7,7,5)]),
        build_e47(8,8,[(2,1,4),(2,2,4),(3,2,4),(5,5,6),(6,0,3)])
    ],
    build_e47(9,10,[(1,1,2),(1,2,2),(2,8,5),(3,8,5),(5,4,7),(7,7,9),(7,8,9),(7,9,9)])
))

PUZZLES.append(make_puzzle(
    'E48','Anti-Diagonal Mirror Add','easy',
    ['symmetry','anti-diagonal reflection','union'],
    'Treat the anti-diagonal as the fold line. Existing cells stay; reflected cells are only added where blank.',
    'Reflect every nonzero cell across the anti-diagonal and add the reflected copy. If a reflected position is already filled, leave it as it is.',
    False, rule_e48,
    [
        build_e48(7,[(0,1,2),(1,4,5),(4,5,7)]),
        build_e48(8,[(1,1,3),(2,5,6),(5,6,4)]),
        build_e48(9,[(0,6,8),(2,2,5),(6,3,2)]),
        build_e48(6,[(0,0,9),(1,3,4),(4,1,7)])
    ],
    build_e48(8,[(0,2,2),(2,6,5),(4,3,7),(6,5,8)])
))

PUZZLES.append(make_puzzle(
    'E49','Ordered Marker Polyline','easy',
    ['marker order','Manhattan path','polyline tracing'],
    'Sort the markers in reading order and connect them one segment at a time.',
    'Take the markers of the single color, sort them from top to bottom then left to right, and connect consecutive markers with Manhattan segments that go horizontally first and then vertically.',
    True, rule_e49,
    [
        build_e49(8,10,4,[(1,1),(1,6),(5,7)]),
        build_e49(9,9,7,[(0,4),(3,2),(6,6)]),
        build_e49(7,11,2,[(1,8),(4,1),(5,9)]),
        build_e49(8,8,5,[(0,1),(3,5),(6,2),(6,6)])
    ],
    build_e49(9,10,8,[(1,2),(2,8),(6,3),(7,7)])
))

# Medium 43-49
PUZZLES.append(make_puzzle(
    'M43','Selector Crop By Color','medium',
    ['selector cell','component filtering','cropping'],
    'The corner cell is a key, not part of the object. Find everything with that color and crop tightly around it.',
    'Read the top-left cell as the selected color. Ignore that selector cell itself, gather every other cell of that color, and crop the smallest rectangle that contains them.',
    False, rule_m43,
    [
        build_m43(10,12,3,[(3,[[1,1],[0,1]],2,3),(5,[[1,1,1],[0,1,0]],1,8),(3,[[1,0],[1,1]],6,6)]),
        build_m43(9,11,6,[(6,[[1,1,0],[0,1,1]],2,5),(2,[[1,1],[1,0]],5,1),(4,[[1],[1],[1]],1,9)]),
        build_m43(10,10,4,[(4,[[1,1],[1,1]],3,3),(7,[[1,0,1],[0,1,0]],1,7),(4,[[1,0],[1,1]],6,6)]),
        build_m43(9,12,5,[(5,[[1,1,1],[0,1,0]],2,2),(8,[[1,1],[1,1]],5,8),(5,[[1,0],[1,1]],5,4)])
    ],
    build_m43(10,12,2,[(2,[[1,1,0],[0,1,1]],2,4),(7,[[1,1],[1,0]],1,9),(2,[[1,0],[1,1]],6,7)])
))

PUZZLES.append(make_puzzle(
    'M44','Checkerboard Interior Fill','medium',
    ['frame detection','parity fill','seed colors'],
    'Use the border only to find the playable interior. The two interior seed colors tell you the alternating pattern.',
    'Find the hollow rectangular frame. Read the two seed colors inside it and fill the entire interior as a checkerboard anchored so the top-left interior cell matches the left seed.',
    False, rule_m44,
    [
        build_m44(9,11,(1,2,7,8,1),(2,3,4),(2,4,7)),
        build_m44(8,10,(0,1,6,8,5),(1,2,2),(1,3,8)),
        build_m44(10,10,(2,2,8,7,3),(3,3,6),(3,4,9)),
        build_m44(9,12,(1,4,7,10,4),(2,5,7),(2,6,2))
    ],
    build_m44(10,12,(1,1,8,9,6),(2,2,3),(2,3,8))
))

PUZZLES.append(make_puzzle(
    'M45','Command Rotate Crop','medium',
    ['command decoding','cropping','rotation'],
    'The corner digit is not part of the object. Crop the object first, then rotate it.',
    'Ignore the command cell in the top-left. Crop the remaining nonzero object tightly, then rotate it according to the command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.',
    False, rule_m45,
    [
        build_m45(8,10,1,PAT_MULTI1,2,4),
        build_m45(9,9,2,PAT_MULTI2,3,2),
        build_m45(8,11,3,PAT_MULTI3,2,6),
        build_m45(10,10,4,PAT_MULTI1,5,3)
    ],
    build_m45(9,11,2,PAT_MULTI3,3,5)
))

PUZZLES.append(make_puzzle(
    'M46','Border Equality Matrix','medium',
    ['legend decoding','row-column interaction','dynamic output'],
    'Think of the top row as column labels and the first column as row labels. The output only keeps matching pairs.',
    'Build an output matrix from the first column and first row. At each interior position, write the row label if it equals the column label; otherwise write 0.',
    False, rule_m46,
    [
        build_m46([2,5,7,2],[7,2,4,5,2]),
        build_m46([3,8,3],[1,3,8,8]),
        build_m46([6,4,6,1],[6,2,1,4,6]),
        build_m46([9,5,2,9],[2,9,5,5,9])
    ],
    build_m46([4,7,4,2],[7,4,1,2,4])
))

PUZZLES.append(make_puzzle(
    'M47','Rectangle Strip By Area','medium',
    ['object extraction','area ranking','dynamic layout'],
    'Every object is already a solid rectangle. Crop each one and sort them before arranging them.',
    'Extract all solid monochrome rectangles, sort them by area ascending (breaking ties by color), and place their cropped rectangles left to right with a one-column gap between consecutive pieces.',
    False, rule_m47,
    [
        build_m47(10,12,[(1,1,2,2,3),(1,6,3,8,5),(5,2,7,3,7)]),
        build_m47(9,13,[(1,1,1,3,2),(3,7,5,8,8),(5,10,8,11,4)]),
        build_m47(11,11,[(1,5,3,6,6),(5,1,5,4,3),(7,7,9,9,9)]),
        build_m47(10,14,[(2,2,4,4,5),(1,9,2,11,7),(6,6,8,7,2)])
    ],
    build_m47(11,13,[(1,1,2,2,4),(2,7,5,8,6),(6,3,8,6,9)])
))

PUZZLES.append(make_puzzle(
    'M48','Multi-Color Ordered Polylines','medium',
    ['per-color grouping','marker order','path tracing'],
    'Solve one color at a time. Each color has its own ordered marker sequence.',
    'For each color separately, sort its markers in reading order and connect consecutive markers with horizontal-then-vertical Manhattan segments. Combine all traced paths.',
    True, rule_m48,
    [
        build_m48(9,12,[(2,[(1,1),(1,6),(5,7)]),(5,[(2,9),(6,9),(7,3)])]),
        build_m48(10,10,[(3,[(0,4),(4,2),(8,5)]),(7,[(1,8),(5,8),(7,1)])]),
        build_m48(8,13,[(4,[(1,2),(3,10),(6,8)]),(8,[(0,11),(5,11),(6,4)])]),
        build_m48(9,11,[(6,[(1,1),(4,6),(7,2)]),(9,[(0,8),(3,9),(7,9)])])
    ],
    build_m48(10,12,[(2,[(1,2),(2,8),(7,8)]),(7,[(0,10),(5,10),(8,3)])])
))

PUZZLES.append(make_puzzle(
    'M49','Center Template In Frames','medium',
    ['template extraction','frame detection','centering','recoloring'],
    'Separate the source template from the destination frames. The template is replayed centered inside every frame.',
    'Extract the non-frame shape made of 2s, normalize it to its own bounding box, then place a centered copy inside each hollow frame. Recolor the copied template to the frame’s color and keep the frames.',
    False, rule_m49,
    [
        build_m49(11,14,[[1,1,0],[0,1,0],[1,1,1]],(1,1),[(1,8,5,12,6),(6,7,9,11,8)]),
        build_m49(10,13,[[1,1],[1,0],[1,1]],(2,2),[(1,8,6,11,5)]),
        build_m49(12,15,[[1,0,1],[1,1,1]],(3,2),[(1,9,5,13,7),(6,8,10,12,4)]),
        build_m49(11,14,[[1,1,1],[0,1,0]],(4,1),[(1,8,6,12,9),(7,7,9,11,3)])
    ],
    build_m49(12,15,[[1,1,0],[1,1,1],[0,1,0]],(2,2),[(1,9,6,13,5),(7,8,10,12,7)])
))

# Hard 43-49
PUZZLES.append(make_puzzle(
    'H43','Select Rotate And Stamp','hard',
    ['selector command','object extraction','rotation','centering','frame replay'],
    'There are three jobs: select the right source color, transform it, then stamp it into every frame.',
    'Use the top-left cell to choose which source component color to keep. Use the top-right command to rotate that selected component. Normalize the rotated component and center a recolored copy inside every hollow frame, using each frame’s color for the copy.',
    False, rule_h43,
    [
        build_h43(12,15,2,2,[[1,1,0],[1,0,0],[1,1,1]],(2,1),[(3,[[1,1],[0,1]],(6,1))],[(1,9,5,13,6),(6,8,10,12,8)]),
        build_h43(11,14,3,4,[[1,1,1],[0,1,0]],(2,2),[(2,[[1,0],[1,1]],(6,1))],[(1,8,5,12,7)]),
        build_h43(12,16,4,3,[[1,0,1],[1,1,1]],(3,2),[(2,[[1,1],[1,0]],(7,2))],[(1,10,6,14,5),(7,9,10,13,9)]),
        build_h43(11,15,2,1,[[1,1],[1,0],[1,1]],(2,1),[(4,[[1,1,1],[0,1,0]],(6,2))],[(1,9,6,13,8),(7,8,9,12,6)])
    ],
    build_h43(12,15,3,2,[[1,1,0],[0,1,1]],(2,2),[(2,[[1,1],[1,0]],(6,1))],[(1,9,5,13,7),(6,8,10,12,5)])
))

PUZZLES.append(make_puzzle(
    'H44','Normalized Shape Intersection','hard',
    ['object normalization','boolean AND','dynamic output'],
    'Ignore absolute placement. Compare the two shapes only after cropping each to its own origin.',
    'Crop the 2-shape and the 3-shape to their own bounding boxes and align both at the top-left. Output only the cells occupied in both normalized shapes, colored 8.',
    False, rule_h44,
    [
        build_h44(10,12,[[1,1,0],[1,1,1],[0,1,0]],(1,1),[[1,0,1],[1,1,1],[0,1,0]],(5,7)),
        build_h44(9,11,[[1,1],[1,0],[1,1]],(2,2),[[1,1],[0,1],[1,1]],(4,7)),
        build_h44(10,10,[[1,1,1],[0,1,0]],(1,5),[[0,1,0],[1,1,1]],(6,1)),
        build_h44(11,12,[[1,0,1],[1,1,1]],(2,1),[[1,1,1],[1,0,1]],(6,7))
    ],
    build_h44(10,12,[[1,1,0],[1,1,1],[0,1,0]],(1,2),[[1,1,1],[1,0,1],[0,1,0]],(6,7))
))

PUZZLES.append(make_puzzle(
    'H45','Hole-Count Legend Recolor','hard',
    ['topological reasoning','legend mapping','component recoloring'],
    'Read the legend before touching the shapes. Then measure how many enclosed holes each component has.',
    'The first three nonzero cells in the top row give the output colors for components with 0, 1, and 2 holes. Recolor every component below the legend according to its hole count.',
    False, rule_h45,
    [
        build_h45(12,16,[2,5,8],[(SHAPE_0,2,1),(SHAPE_1,2,7),(SHAPE_2,6,9)]),
        build_h45(11,15,[3,6,9],[(SHAPE_1,2,2),(SHAPE_0,3,10),(SHAPE_2,6,5)]),
        build_h45(12,15,[4,7,2],[(SHAPE_2,2,1),(SHAPE_0,7,2),(SHAPE_1,6,9)]),
        build_h45(11,16,[8,1,6],[(SHAPE_0,2,3),(SHAPE_2,5,9),(SHAPE_1,7,1)])
    ],
    build_h45(12,16,[5,2,9],[(SHAPE_1,2,1),(SHAPE_0,3,10),(SHAPE_2,6,8)])
))

PUZZLES.append(make_puzzle(
    'H46','Manhattan Tie Cells In Frame','hard',
    ['distance geometry','frame interior','equidistance'],
    'The new color does not spread from one seed; it marks cells that are balanced between the two seeds.',
    'Keep the frame and the two seeds. Inside the frame, color every cell whose Manhattan distance to the first seed equals its Manhattan distance to the second seed with 9.',
    False, rule_h46,
    [
        build_h46(11,13,(1,1,9,11,4),[(3,3,2),(7,9,3)]),
        build_h46(10,12,(1,2,8,9,5),[(2,4,7),(6,7,2)]),
        build_h46(12,14,(2,1,10,12,6),[(4,3,8),(8,9,5)]),
        build_h46(11,11,(1,1,9,9,3),[(3,7,2),(7,3,6)])
    ],
    build_h46(12,13,(1,1,10,11,7),[(3,4,2),(8,8,5)])
))

PUZZLES.append(make_puzzle(
    'H47','Rotate Then Flip','hard',
    ['command composition','rotation','reflection','cropping'],
    'There are two commands, and order matters. Rotate first, then apply the chosen flip.',
    'Ignore the two command cells in the top corners. Crop the remaining object, rotate it according to the left command (1=id, 2=90° clockwise, 3=180°, 4=270° clockwise), then flip it according to the right command (1=vertical flip across a horizontal axis, 2=horizontal flip across a vertical axis).',
    False, rule_h47,
    [
        build_h47(10,12,2,1,PAT_MULTI1,(3,5)),
        build_h47(9,11,4,2,PAT_MULTI2,(2,4)),
        build_h47(11,13,3,1,PAT_MULTI3,(4,6)),
        build_h47(10,10,1,2,PAT_MULTI1,(5,2))
    ],
    build_h47(11,12,2,2,PAT_MULTI3,(4,5))
))

PUZZLES.append(make_puzzle(
    'H48','Hole-Sorted Component Strip','hard',
    ['component extraction','hole counting','dynamic ordering','layout'],
    'First split the objects, then count holes, then arrange. Do not try to sort raw pixels directly.',
    'Extract the disconnected nonzero components, sort them by hole count ascending and then by area ascending, crop each one tightly, and place the cropped components left to right with one zero column between them.',
    False, rule_h48,
    [
        build_h48(12,20,[(SHAPE_1,(2,1)),(SHAPE_0,(3,9)),(SHAPE_2,(6,12))]),
        build_h48(11,20,[(SHAPE_2,(2,1)),(SHAPE_0,(6,4)),(SHAPE_1,(5,12))]),
        build_h48(12,20,[(SHAPE_0,(2,2)),(SHAPE_1,(2,10)),(SHAPE_2,(6,12))]),
        build_h48(11,20,[(SHAPE_1,(2,4)),(SHAPE_2,(5,11)),(SHAPE_0,(6,1))])
    ],
    build_h48(12,20,[(SHAPE_2,(2,2)),(SHAPE_0,(7,4)),(SHAPE_1,(5,13))])
))

PUZZLES.append(make_puzzle(
    'H49','Polyline Intersections Highlighted','hard',
    ['multi-object tracing','intersection detection','marker order'],
    'First trace each color’s path separately. Only after that decide which cells are overlaps.',
    'Sort each color’s markers in reading order and trace a horizontal-then-vertical Manhattan polyline through them. Color normal path cells with their path color, but recolor any cell used by two or more different paths to 9.',
    True, rule_h49,
    [
        build_h49(10,12,[(2,[(1,1),(1,8),(7,8)]),(5,[(0,5),(6,5),(6,2)])]),
        build_h49(9,11,[(3,[(0,3),(5,3),(5,8)]),(7,[(2,0),(2,6),(7,6)])]),
        build_h49(10,13,[(4,[(1,10),(6,10),(6,3)]),(8,[(0,6),(4,6),(4,11)])]),
        build_h49(9,12,[(6,[(1,1),(1,7),(6,7)]),(2,[(0,4),(5,4),(5,1)])])
    ],
    build_h49(10,13,[(2,[(1,2),(1,9),(7,9)]),(7,[(0,6),(6,6),(6,3)])])
))

assert len(PUZZLES)==21

# === Payload and validation ===
PAYLOAD={
    'set': 7,
    'summary': {
        'set': 7,
        'puzzle_count': 21,
        'train_pair_count': sum(len(p['train']) for p in PUZZLES),
        'avg_train_pairs': round(sum(len(p['train']) for p in PUZZLES)/len(PUZZLES), 2),
        'difficulty_counts': {
            'easy': sum(1 for p in PUZZLES if p['difficulty']=='easy'),
            'medium': sum(1 for p in PUZZLES if p['difficulty']=='medium'),
            'hard': sum(1 for p in PUZZLES if p['difficulty']=='hard'),
        },
        'new_primitive': {
            'name': 'trace_polyline_markers',
            'purpose': 'Given ordered marker groups, draw Manhattan polylines through them and optionally recolor overlaps as intersections.'
        }
    },
    'puzzles': PUZZLES,
}


def validate():
    ns=globals()
    for p in PUZZLES:
        fn=ns[p['program_name']]
        for i,pair in enumerate(p['train'], start=1):
            inp=grid_from_strings(pair['input'])
            got=strings_from_grid(fn(inp))
            if got!=pair['output']:
                raise AssertionError(f"{p['id']} train {i} mismatch\nGOT={got}\nEXP={pair['output']}")
        tinp=grid_from_strings(p['test']['input'])
        got=strings_from_grid(fn(tinp))
        if got!=p['test']['output']:
            raise AssertionError(f"{p['id']} test mismatch")
    return True


def write_markdown(payload, out_path):
    lines=[]
    lines.append('# ARC Additional Puzzle Bank — 21 Puzzles (Set 7)')
    lines.append('')
    lines.append('This seventh pack continues the numbering with **`E43–E49`**, **`M43–M49`**, and **`H43–H49`**.')
    lines.append('')
    tp=payload['summary']['train_pair_count']
    avg=payload['summary']['avg_train_pairs']
    lines.append(f'This set contains **{tp} train pairs across 21 puzzles**, averaging **{avg:.2f} train pairs per puzzle**.')
    lines.append('')
    lines.append('It introduces a new helper primitive for solver-facing implementations:')
    lines.append('')
    lines.append('```text')
    lines.append("trace_polyline_markers(base_grid, marker_groups, mode='hv', intersection_color=None)")
    lines.append('```')
    lines.append('')
    lines.append('Intuition: given ordered marker groups, draw Manhattan polylines through them and optionally recolor cells used by multiple groups as intersections. This primitive is used directly in **E49**, **M48**, and **H49**.')
    lines.append('')
    lines.append('Design goals for this set:')
    lines.append('')
    lines.append('- easy: fixed-offset echoes, diagonal midpoint completion, header-driven filling, corner-based rectangle recovery, local denoising, symmetry completion, and simple ordered routing')
    lines.append('')
    lines.append('- medium: selector crops, parity fills, command transforms, legend matrices, object ranking, multi-color routing, and centered template replay')
    lines.append('')
    lines.append('- hard: chained commands, normalized shape algebra, topological recoloring, distance ties, hole-aware ordering, and path-overlap highlighting')
    lines.append('')
    for difficulty in ['easy','medium','hard']:
        group=[p for p in payload['puzzles'] if p['difficulty']==difficulty]
        lines.append(f'## {difficulty.capitalize()} ({len(group)})')
        lines.append('')
        for p in group:
            lines.append(f"### {p['id']} — {p['title']}")
            lines.append('')
            lines.append(f"**Difficulty:** {p['difficulty']}")
            lines.append('')
            lines.append(f"**Train pairs:** {len(p['train'])}")
            lines.append('')
            lines.append(f"**Skills:** {', '.join(p['skills'])}")
            lines.append('')
            lines.append(f"**Suggested staged path:** {p['staged_hint']}")
            lines.append('')
            for i,pair in enumerate(p['train'], start=1):
                lines.append(f"**Train {i} — input**")
                lines.append('')
                lines.append('```text')
                lines.extend(pair['input'])
                lines.append('```')
                lines.append('')
                lines.append(f"**Train {i} — output**")
                lines.append('')
                lines.append('```text')
                lines.extend(pair['output'])
                lines.append('```')
                lines.append('')
            lines.append('**Test — input**')
            lines.append('')
            lines.append('```text')
            lines.extend(p['test']['input'])
            lines.append('```')
            lines.append('')
            lines.append('**Test — output**')
            lines.append('')
            lines.append('```text')
            lines.extend(p['test']['output'])
            lines.append('```')
            lines.append('')
            lines.append('**Written solution**')
            lines.append('')
            lines.append(p['written_solution'])
            lines.append('')
            lines.append('**Reference program**')
            lines.append('')
            lines.append('```python')
            lines.extend(p['program_source'].splitlines())
            lines.append('```')
            lines.append('')
    Path(out_path).write_text("\n".join(lines))


def write_primitive(out_path):
    lines=[]
    lines.append('# New Primitive Spec — `trace_polyline_markers`')
    lines.append('')
    lines.append('```python')
    lines.append("trace_polyline_markers(base_grid, marker_groups, mode='hv', intersection_color=None)")
    lines.append('```')
    lines.append('')
    lines.append('Purpose: draw one or more Manhattan polylines from ordered marker groups. Each group is a color plus an ordered point list. The primitive traces each consecutive pair of points using horizontal-then-vertical (`hv`) or vertical-then-horizontal (`vh`) routing.')
    lines.append('')
    lines.append('Arguments:')
    lines.append('')
    lines.append('- `base_grid`: output canvas to paint on')
    lines.append('- `marker_groups`: iterable like `[(color, [(r,c), ...]), ...]`')
    lines.append("- `mode`: `'hv'` or `'vh'` for segment routing order")
    lines.append('- `intersection_color`: if not `None`, cells used by 2+ groups are recolored to this value')
    lines.append('')
    lines.append('Why it matters: many ARC-like tasks contain sparse markers that implicitly define a path, wire, or route. This primitive turns that latent geometric instruction into a first-class DSL operation, rather than forcing the solver to rebuild Manhattan routing from raw loops each time.')
    lines.append('')
    lines.append('Used in this set: **E49**, **M48**, and **H49**.')
    Path(out_path).write_text("\n".join(lines))


if __name__ == '__main__':
    validate()
    out_base=Path('/mnt/data')
    py_path=out_base/'arc_additional_puzzles_21_set7.py'
    md_path=out_base/'arc_additional_puzzles_21_set7.md'
    json_path=out_base/'arc_additional_puzzles_21_set7.json'
    prim_path=out_base/'arc_additional_puzzles_21_set7_primitive.md'
    # write python source = this file without helper build script note? write full script
    py_path.write_text(Path(__file__).read_text())
    write_markdown(PAYLOAD, md_path)
    json_path.write_text(json.dumps(PAYLOAD, indent=2))
    write_primitive(prim_path)
    print('wrote', md_path)
    print('wrote', py_path)
    print('wrote', json_path)
    print('wrote', prim_path)
