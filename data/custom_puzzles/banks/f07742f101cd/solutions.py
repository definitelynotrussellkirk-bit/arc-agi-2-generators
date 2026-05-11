"""
ARC-style puzzle bank continuation 20: 21 more puzzles (E134-E140, M134-M140, H134-H140).

This batch leans into metadata dispatch, wall shadows, panel analogy, bbox-relative edit transfer,
family matching under symmetry, transform composition, and keyed prototype legends.

Notable motifs:
- wall_shadow(shape, wall): M134
- panel_analogy_apply(A, B, C): M140, H134, H137, H138
- bbox_delta_transfer(before, after, query): H135
- family_canonicalize(prototypes, query): H136
- prototype_key_stamp(dictionary, seeds): H140
"""
from __future__ import annotations
from collections import deque
from typing import List

Grid = List[List[int]]


def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)


def cc(g, ignore=(0,), same_color=True):
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c] in ignore: continue
            color=g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny] not in ignore and ((not same_color) or g[nx][ny]==color):
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((color,cells))
    return out


def crop_cells(g, cells):
    r0,r1,c0,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out


def rot90(g): return [list(row) for row in zip(*g[::-1])]


def rot180(g): return [row[::-1] for row in g[::-1]]


def rot270(g): return [list(row) for row in zip(*g)][::-1]


def flip_h(g): return [row[::-1] for row in g]


def flip_v(g): return g[::-1]


def transpose(g): return [list(row) for row in zip(*g)]


def anti_transpose(g):
    h,w=dims(g); out=[[0]*h for _ in range(w)]
    for r in range(h):
        for c in range(w):
            out[w-1-c][h-1-r]=g[r][c]
    return out


def split_panels_row(g, count, sep=8):
    h,w=dims(g)
    pw=(w-(count-1))//count
    panels=[]; c=0
    for i in range(count):
        panels.append([row[c:c+pw] for row in g]); c+=pw
        if i<count-1: c+=1
    return panels


def infer_transform(a,b):
    for name,fn in TRANSFORMS.items():
        tb=fn(a)
        if dims(tb)==dims(b) and tb==b:
            return name
    return None


def normalize_support(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return frozenset(), None
    r0,r1,c0,c1=bbox(cells)
    supp=frozenset((r-r0,c-c0) for r,c in cells)
    color=next(v for row in g for v in row if v!=0)
    return supp,color


def apply_support(supp,color):
    maxr=max([r for r,c in supp], default=0)
    maxc=max([c for r,c in supp], default=0)
    out=blank(maxr+1,maxc+1)
    for r,c in supp:
        out[r][c]=color
    return out


def transform_support(supp, fn):
    g=apply_support(supp,1)
    tg=fn(g)
    ns,_=normalize_support(tg)
    return ns


def apply_recolor(g,mapping):
    return [[mapping.get(v,v) if v!=0 else 0 for v in row] for row in g]


TRANSFORMS = {
    "id": lambda g: clone(g),
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "anti_transpose": anti_transpose,
}


def solve_E134(grid):
    h,w=dims(grid)
    color=next(v for v in grid[0] if v!=0)
    out=blank(h,w)
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1:
                out[r][c]=color
    return out


def solve_E135(grid):
    out=clone(grid)
    h,w=dims(grid)
    for c in range(w):
        nz=[r for r in range(h) if grid[r][c]!=0]
        if len(nz)==2 and grid[nz[0]][c]==grid[nz[1]][c]:
            a,b=nz; color=grid[a][c]
            for r in range(a,b+1):
                out[r][c]=color
    return out


def solve_E136(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        vals=[v for v in grid[r] if v!=0]
        out[r][:len(vals)] = vals
    return out


def solve_E137(grid):
    h,w=dims(grid)
    axis=None
    for r in range(h):
        if all(v==8 for v in grid[r]):
            axis=r; break
    out=blank(h,w)
    out[axis]=[8]*w
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v not in (0,8):
                out[r][c]=v
                rr=2*axis-r
                if 0<=rr<h:
                    out[rr][c]=v
    return out


def solve_E138(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v!=0:
                for rr,cc_ in [(r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    if 0<=rr<h and 0<=cc_<w:
                        out[rr][cc_]=v
    return out


def solve_E139(grid):
    counts={}
    for row in grid:
        for v in row:
            if v!=0:
                counts[v]=counts.get(v,0)+1
    major=max(counts, key=lambda k:(counts[k], -k))
    return [[v if v==major else 0 for v in row] for row in grid]


def solve_E140(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            border=[grid[r][c],grid[r][c+1],grid[r][c+2],grid[r+1][c],grid[r+1][c+2],grid[r+2][c],grid[r+2][c+1],grid[r+2][c+2]]
            if border[0]!=0 and len(set(border))==1 and grid[r+1][c+1]==0:
                out[r+1][c+1]=border[0]
    return out


def solve_M134(grid):
    h,w=dims(grid)
    out=clone(grid)
    # detect full wall row or col of 8s
    wall_row=next((r for r in range(h) if all(v==8 for v in grid[r])), None)
    wall_col=next((c for c in range(w) if all(grid[r][c]==8 for r in range(h))), None)
    if wall_col is not None:
        non8=[c for r in range(h) for c,v in enumerate(grid[r]) if v not in (0,8)]
        side='left' if non8 and max(non8)<wall_col else 'right'
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v not in (0,8):
                    if side=='left':
                        for cc_ in range(c, wall_col):
                            if out[r][cc_]==0: out[r][cc_]=v
                    else:
                        for cc_ in range(wall_col+1, c+1):
                            if out[r][cc_]==0: out[r][cc_]=v
    elif wall_row is not None:
        non8=[r for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
        side='top' if non8 and max(non8)<wall_row else 'bottom'
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v not in (0,8):
                    if side=='top':
                        for rr in range(r, wall_row):
                            if out[rr][c]==0: out[rr][c]=v
                    else:
                        for rr in range(wall_row+1, r+1):
                            if out[rr][c]==0: out[rr][c]=v
    return out


def solve_M135(grid):
    # crop interior of the only 8-frame rectangle
    h,w=dims(grid)
    cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==8]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0+1:c1] for row in grid[r0+1:r1]]


def solve_M136(grid):
    k=sum(1 for v in grid[0] if v==1)
    cells=[(r,c) for r in range(1,len(grid)) for c,v in enumerate(grid[r]) if v!=0]
    proto=crop_cells(grid,cells)
    ph,pw=dims(proto)
    out=blank(ph, k*pw+(k-1))
    x=0
    for i in range(k):
        for r in range(ph):
            for c in range(pw):
                out[r][x+c]=proto[r][c]
        x += pw
        if i<k-1: x += 1
    return out


def solve_M137(grid):
    a,b=split_panels_row(grid,2,sep=8)
    h,w=dims(a)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if a[r][c]==1:
                out[r][c]=b[r][c]
    return out


def solve_M138(grid):
    h,w=dims(grid)
    cells=[(r,c,v) for r in range(h) for c,v in enumerate(grid[r]) if v!=0]
    ar,ac = next((r,c) for r,c,v in cells if v==9)
    out=clone(grid)
    for r,c,v in cells:
        if v==9: continue
        rr,cc_=2*ar-r,2*ac-c
        if 0<=rr<h and 0<=cc_<w:
            out[rr][cc_]=v
    return out


def solve_M139(grid):
    comps=[]
    for color,cells in cc(grid):
        comps.append((len(cells), color, crop_cells(grid,cells)))
    comps.sort(key=lambda t:(-t[0], t[1]))
    h=max(len(g) for _,_,g in comps)
    w=sum(len(g[0]) for _,_,g in comps)+(len(comps)-1)
    out=blank(h,w)
    x=0
    for _,_,g in comps:
        gh,gw=dims(g)
        for r in range(gh):
            for c in range(gw):
                out[r][x+c]=g[r][c]
        x += gw+1
    return out


def solve_M140(grid):
    a,b,c = split_panels_row(grid,3,sep=8)
    name=infer_transform(a,b)
    return TRANSFORMS[name](c)


def solve_H134(grid):
    a,b,c = split_panels_row(grid,3,sep=8)
    for name,fn in TRANSFORMS.items():
        ta=fn(a)
        if dims(ta)!=dims(b): 
            continue
        mapping={}
        ok=True
        for r in range(len(ta)):
            for cc_ in range(len(ta[0])):
                va,vb=ta[r][cc_],b[r][cc_]
                if va==0 and vb==0:
                    continue
                if va==0 or vb==0:
                    ok=False; break
                if va in mapping and mapping[va]!=vb:
                    ok=False; break
                mapping[va]=vb
            if not ok: break
        if ok:
            return apply_recolor(fn(c), mapping)
    raise ValueError('no transform+recolor found')


def solve_H135(grid):
    before,after,query = split_panels_row(grid,3,sep=8)
    bcells=[(r,c) for r,row in enumerate(before) for c,v in enumerate(row) if v!=0]
    acells=[(r,c) for r,row in enumerate(after) for c,v in enumerate(row) if v!=0]
    qcells=[(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v!=0]
    br0,br1,bc0,bc1=bbox(bcells)
    ar0,ar1,ac0,ac1=bbox(acells)
    qr0,qr1,qc0,qc1=bbox(qcells)
    before_set={(r-br0,c-bc0) for r,c in bcells}
    after_set={(r-ar0,c-ac0) for r,c in acells}
    added=after_set-before_set
    out=clone(query)
    color=next(v for row in query for v in row if v!=0)
    for dr,dc in added:
        rr,cc_=qr0+dr,qc0+dc
        if 0<=rr<len(query) and 0<=cc_<len(query[0]):
            out[rr][cc_]=color
    return out


def solve_H136(grid):
    p1,p2,q = split_panels_row(grid,3,sep=8)
    s1,_=normalize_support(p1)
    s2,_=normalize_support(p2)
    sq,qcolor=normalize_support(q)
    # compare query against transformed families
    for base in [s1,s2]:
        for name,fn in TRANSFORMS.items():
            if transform_support(base, fn)==sq:
                return apply_support(base,qcolor)
    raise ValueError('no family match')


def solve_H137(grid):
    a,b,q = split_panels_row(grid,3,sep=8)
    name=infer_transform(a,b)
    tq=TRANSFORMS[name](q)
    h,w=dims(q) if dims(q)==dims(tq) else dims(tq)
    # assume same dims due chosen transform on square panel
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            va=q[r][c]
            vb=tq[r][c]
            if va!=0 and vb!=0:
                out[r][c]=9
            else:
                out[r][c]=va or vb
    return out


def solve_H138(grid):
    a,b,c,q = split_panels_row(grid,4,sep=8)
    t1=infer_transform(a,b)
    t2=infer_transform(b,c)
    return TRANSFORMS[t2](TRANSFORMS[t1](q))


def solve_H139(grid):
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=[(len(cells), idx, cells) for idx,(color,cells) in enumerate(cc(body, ignore=(0,), same_color=True))]
    comps.sort(key=lambda t:(-t[0], t[1]))
    out=blank(len(body), len(body[0]))
    for i,(_,_,cells) in enumerate(comps):
        color=palette[i]
        for r,c in cells:
            out[r][c]=color
    return out


def solve_H140(grid):
    top=grid[:3]
    body=[row[:] for row in grid[4:]]  # row 3 is all 8 separator
    p1,p2,p3 = split_panels_row(top,3,sep=8)
    protos={}
    for p in [p1,p2,p3]:
        color=next(v for row in p for v in row if v!=0)
        supp,_=normalize_support(p)
        # anchor at center of 3x3
        rel=[(r-1,c-1) for r,c in supp]
        protos[color]=rel
    h,w=dims(body)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(body[r]):
            if v!=0:
                for dr,dc in protos[v]:
                    rr,cc_=r+dr,c+dc
                    if 0<=rr<h and 0<=cc_<w:
                        out[rr][cc_]=v
    return out
