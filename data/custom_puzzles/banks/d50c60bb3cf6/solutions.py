"""
ARC-style puzzle bank continuation 5: 21 more puzzles (E29-E35, M29-M35, H29-H35).
New primitive introduced here: sweep_shadow, which paints the whole swept path of a shape as it is extruded in a direction.
Each solve_* function is a reference program for one puzzle.
"""
from __future__ import annotations
from typing import List
from collections import deque, defaultdict

Grid = List[List[int]]

def parse_grid(lines):
    return [[int(ch) for ch in line.strip()] for line in lines]

def grid_to_strings(g):
    return [''.join(str(x) for x in row) for row in g]

def dims(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def components(g, include_colors=None):
    h,w=dims(g); seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0 or (include_colors is not None and col not in include_colors) or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]==col and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def normalize_shape(cells):
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1)

def rotate90(shape, h, w):
    return {(c, h-1-r) for r,c in shape}, w, h

def outline_cells(cells):
    s=set(cells)
    out=set()
    for r,c in s:
        if any((r+dr,c+dc) not in s for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]):
            out.add((r,c))
    return out

def runs_of_row(row):
    runs=[]
    c=0; w=len(row)
    while c<w:
        v=row[c]
        s=c
        while c+1<w and row[c+1]==v:
            c+=1
        e=c
        runs.append((s,e,v))
        c+=1
    return runs

def find_cross_guides(g):
    h,w=dims(g)
    gr=gc=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            gr=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            gc=c; break
    return gr,gc

def quadrant_bounds(g, quad):
    h,w=dims(g); gr,gc=find_cross_guides(g)
    if quad=='TL':
        return 0,gr,0,gc
    if quad=='TR':
        return 0,gr,gc+1,w
    if quad=='BL':
        return gr+1,h,0,gc
    if quad=='BR':
        return gr+1,h,gc+1,w
    raise

def extract_quad_cells(g, quad):
    r0,r1,c0,c1=quadrant_bounds(g,quad)
    cells=[]
    for r in range(r0,r1):
        for c in range(c0,c1):
            if g[r][c]!=0 and g[r][c]!=9:
                cells.append((g[r][c],r-r0,c-c0))
    return cells, (r1-r0,c1-c0)

def nz_component(g, start):
    h,w=dims(g); q=deque([start]); seen={start}; cells=[]
    while q:
        r,c=q.popleft(); cells.append((r,c))
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc]!=0 and (nr,nc) not in seen:
                seen.add((nr,nc)); q.append((nr,nc))
    return cells

def sweep_shadow(cells, direction, h, w, stop_cells=None):
    """New primitive: extrude a shape cellwise in a direction, painting the whole swept path."""
    dr, dc = direction
    stop_cells = set(stop_cells or [])
    out = set(cells)
    for r, c in cells:
        nr, nc = r + dr, c + dc
        while 0 <= nr < h and 0 <= nc < w and (nr, nc) not in stop_cells:
            out.add((nr, nc))
            nr += dr
            nc += dc
    return out

def rotate_bbox_preserve_offset(cells_rel):
    if not cells_rel:
        return set()
    coords=[(r,c) for _,r,c in cells_rel]
    rs=[r for r,c in coords]; cs=[c for r,c in coords]
    rmin,rmax,cmin,cmax=min(rs),max(rs),min(cs),max(cs)
    shape={(r-rmin,c-cmin) for r,c in coords}
    h,w=rmax-rmin+1,cmax-cmin+1
    rot={(c, h-1-r) for r,c in shape}
    return rot,(rmin,cmin),max(1,w),max(1,h)

ARROW_DIR = {1: (-1, 0), 2: (0, 1), 3: (1, 0), 4: (0, -1)}

def solve_E29(g):
    h,w=dims(g); out=clone(g)
    pos=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                pos[g[r][c]].append((r,c))
    for col,cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if abs(dr)==abs(dc) and abs(dr)>=2:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                ok=True
                for k in range(1,abs(dr)):
                    if g[r1+k*sr][c1+k*sc]!=0:
                        ok=False; break
                if ok:
                    for k in range(1,abs(dr)):
                        out[r1+k*sr][c1+k*sc]=col
    return out

def solve_E30(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v==0: 
                continue
            same=sum(g[r+dr][c+dc]==v for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)])
            if same==3:
                out[r][c]=8
    return out

def solve_E31(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            a,b,c1,d = g[r][c], g[r][c+1], g[r+1][c], g[r+1][c+1]
            vals=[a,b,c1,d]
            if a==d!=0 and b==0 and c1==0:
                out[r][c+1]=a; out[r+1][c]=a
            if b==c1!=0 and a==0 and d==0:
                out[r][c]=b; out[r+1][c+1]=b
    return out

def solve_E32(g):
    h,w=dims(g); out=clone(g)
    dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            # isolated in 8-neighborhood
            iso=True
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]!=0:
                        iso=False
            if iso:
                for dr,dc in dirs:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=v
    return out

def solve_E33(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    # move if down-right empty in original and in bounds
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            nr,nc=r+1,c+1
            if nr<h and nc<w and g[nr][nc]==0:
                out[nr][nc]=v if out[nr][nc]==0 else out[nr][nc]
            else:
                out[r][c]=v if out[r][c]==0 else out[r][c]
    return out

def solve_E34(g):
    h,w=dims(g)
    guide=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            guide=c; break
    out=clone(g)
    if guide is None: return out
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                mc=2*guide-c
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=v
    return out

def solve_E35(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        c0=g[r][0]
        if c0!=0:
            for c in range(1,w):
                if g[r][c]==8:
                    out[r][c]=c0
    return out

def solve_M29(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    out=[[0]*w for _ in range(h)]
    comps=components([row[:] for row in g[1:]])  # body relative coords
    # need original coords
    body=[row[:] for row in g[1:]]
    for col,cells in components(body):
        if len(cells)==k:
            for r,c in cells:
                out[r+1][c]=col
    return out

def solve_M30(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        s,t=g[0][c],g[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    out=clone(g)
    for r in range(2,h):
        for c in range(w):
            v=g[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out

def solve_M31(g):
    h,w=dims(g)
    out=clone(g)
    wall=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            wall=c
            break
    if wall is None:
        return out
    stop={(r,wall) for r in range(h)}
    for col,cells in components([[v if v not in (0,9) else 0 for v in row] for row in g]):
        swept=sweep_shadow(cells,(0,1),h,w,stop)
        for r,c in swept:
            if c!=wall:
                out[r][c]=col
    return out

def solve_M32(g):
    h,w=dims(g)
    rows={r for r in range(h) if 1 in g[r]}
    cols={c for c in range(w) if any(g[r][c]==2 for r in range(h))}
    out=[[0]*w for _ in range(h)]
    for r in rows:
        for c in cols:
            out[r][c]=3
    return out

def solve_M33(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        oc=outline_cells(cells)
        for r,c in oc:
            out[r][c]=col
    return out

def solve_M34(g):
    h,w=dims(g)
    keep=[c for c,v in enumerate(g[0]) if v==1]
    out=[]
    for r in range(1,h):
        out.append([g[r][c] for c in keep])
    return out

def solve_M35(g):
    h,w=dims(g); out=clone(g)
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    if len(anchors)!=1: return out
    a=anchors[0]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                rr,cc=2*a[0]-r, 2*a[1]-c
                if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                    out[rr][cc]=v
    return out

def solve_H29(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    obj_grid=[[v if v>=5 else 0 for v in row] for row in g]
    for col,cells in components(obj_grid):
        arrow=None
        for r,c in cells:
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and g[nr][nc] in ARROW_DIR:
                    arrow=g[nr][nc]
                    break
            if arrow is not None:
                break
        swept=sweep_shadow(cells,ARROW_DIR[arrow],h,w)
        for r,c in swept:
            out[r][c]=col
    return out

def solve_H30(g):
    h,w=dims(g)
    src_runs=[run for run in runs_of_row(g[0]) if run[2]!=0]
    dst_runs=[run for run in runs_of_row(g[1]) if run[2]!=0]
    # map id->slice
    blocks={}
    for s,e,v in src_runs:
        blocks[v]=(s,e+1)
    out=[]
    for r in range(2,h):
        row=[]
        for s,e,v in dst_runs:
            bs,be=blocks[v]
            row.extend(g[r][bs:be])
        out.append(row)
    return out

def solve_H31(g):
    out=clone(g)
    # apply rotate90 clockwise to BL into BR
    cells_rel,_=extract_quad_cells(g,'BL')
    if not cells_rel: 
        return out
    color=cells_rel[0][0]  # assume monochrome shape
    rot,offset,hh,ww=rotate_bbox_preserve_offset(cells_rel)
    roff,coff=offset
    for r,c in rot:
        rr,cc=roff+r, coff+c
        place_r0,place_r1,place_c0,place_c1=quadrant_bounds(out,'BR')
        if place_r0+rr<place_r1 and place_c0+cc<place_c1:
            out[place_r0+rr][place_c0+cc]=color
    return out

def solve_H32(g):
    h,w=dims(g)
    # find anchor 9 in source template; assume one 9 in multi-cell component and maybe other nonzero singleton markers
    anchor=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                # if connected to another nonzero, treat as source anchor
                comp=nz_component(g,(r,c))
                if len(comp)>1:
                    anchor=(r,c); template_comp=comp
                    break
        if anchor: break
    if anchor is None:
        return clone(g)
    # relative shape of all cells in template component relative to anchor
    rel=[(r-anchor[0], c-anchor[1]) for r,c in template_comp]
    template_set=set(template_comp)
    out=[[0]*w for _ in range(h)]
    # destination markers: nonzero cells outside template
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in template_set:
                col=g[r][c]
                for dr,dc in rel:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=col
    return out

def solve_H33(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    chosen=None
    chosen_col=None
    for col,cells in components([row[:] for row in g[1:]]):
        if len(cells)==k:
            chosen={(r+1,c) for r,c in cells}
            chosen_col=col
            break
    if chosen is None:
        return [[0]]
    oc=outline_cells(chosen)
    # crop
    rs=[r for r,c in oc]; cs=[c for r,c in oc]
    r0,r1,c0,c1=min(rs),max(rs),min(cs),max(cs)
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in oc:
        out[r-r0][c-c0]=chosen_col
    return out

def solve_H34(g):
    out=clone(g)
    cells_rel,_=extract_quad_cells(g,'BL')
    if not cells_rel:
        return out
    color=cells_rel[0][0]
    coords=[(r,c) for _,r,c in cells_rel]
    rs=[r for r,c in coords]; cs=[c for r,c in coords]
    rmin,rmax,cmin,cmax=min(rs),max(rs),min(cs),max(cs)
    shape={(r-rmin,c-cmin) for r,c in coords}
    outshape=outline_cells({(r,c) for r,c in shape})
    br0,br1,bc0,bc1=quadrant_bounds(out,'BR')
    for r,c in outshape:
        rr,cc=br0+rmin+r, bc0+cmin+c
        out[rr][cc]=color
    return out

def solve_H35(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        s,t=g[0][c],g[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    keep=[c for c,v in enumerate(g[2]) if v==1]
    out=[]
    for r in range(3,h):
        row=[]
        for c in keep:
            v=g[r][c]
            row.append(mapping.get(v,v))
        out.append(row)
    return out

