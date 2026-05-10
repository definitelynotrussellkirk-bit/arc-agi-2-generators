"""
ARC-style puzzle bank continuation 19: 21 more puzzles (E127-E133, M127-M133, H127-H133).

This batch leans into interval completion, border classification, bbox abstraction, explicit-axis reflection,
room filling, panel-transform inference, prototype stamping, edit-delta transfer, prototype-family matching,
and conflict-aware merges.

Notable motifs:
- interval_fill(row): E127
- axis_reflect(axis, shape): M127
- transform_recolor_infer(example_before, example_after, query): H127
- edit_delta_relative(before, after, query): H129
- family_match(prototypes, query): H131
- conflict_merge(a, b): H132
"""
from __future__ import annotations
from collections import deque
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]

def clone(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

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

def split_panel_row1(g, count, sep=1):
    h,w=dims(g)
    pw=(w-sep*(count-1))//count
    panels=[]; c=0
    for i in range(count):
        panels.append([row[c:c+pw] for row in g])
        c+=pw
        if i<count-1:
            c+=sep
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
    return frozenset((r-r0,c-c0) for r,c in cells), next(v for row in g for v in row if v!=0)

def apply_support(supp, color):
    maxr=max(r for r,c in supp) if supp else 0
    maxc=max(c for r,c in supp) if supp else 0
    out=blank(maxr+1, maxc+1)
    for r,c in supp:
        out[r][c]=color
    return out

def transform_support(supp, fn):
    g=apply_support(supp, 1)
    tg=fn(g)
    ns,_=normalize_support(tg)
    return ns

def solve_E127(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        nz=[c for c in range(w) if grid[r][c]!=0]
        if len(nz)==2 and grid[r][nz[0]]==grid[r][nz[1]]:
            a,b=nz; color=grid[r][a]
            for c in range(a,b+1):
                out[r][c]=color
    return out

def solve_E128(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out

def solve_E129(grid):
    h,w=dims(grid)
    assert h==w
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                out[c][r]=grid[r][c]
    return out

def solve_E130(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        if len(cells)>1:
            for r,c in cells:
                out[r][c]=color
    return out

def solve_E131(grid):
    h,w=dims(grid)
    color=max(grid[0])
    out=blank(h,w)
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1:
                out[r][c]=color
    return out

def solve_E132(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        nz=[c for c in range(w) if grid[r][c]!=0]
        if len(nz)==2 and grid[r][nz[0]]==grid[r][nz[1]]:
            a,b=nz
            if (a+b)%2==0:
                out[r][(a+b)//2]=grid[r][a]
    return out

def solve_E133(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        r0,r1,c0,c1=bbox(cells)
        rr=(r0+r1)//2; cc_=(c0+c1)//2
        out[rr][cc_]=color
    return out

def solve_M127(grid):
    h,w=dims(grid)
    axis=None
    for c in range(w):
        if all(grid[r][c]==8 for r in range(h)):
            axis=c; break
    out=blank(h,w)
    for r in range(h):
        out[r][axis]=8
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,8):
                out[r][c]=v
                mc=2*axis-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def solve_M128(grid):
    h,w=dims(grid)
    # walls are 5
    seen=set(); out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen: 
                continue
            # room = connected cells not wall
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            seeds=set()
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.add(grid[x][y])
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if len(seeds)==1:
                color=next(iter(seeds))
                for x,y in cells:
                    if out[x][y]==0:
                        out[x][y]=color
    return out

def solve_M129(grid):
    ex_in, ex_out, query = split_panel_row1(grid,3,sep=1)
    name=infer_transform(ex_in, ex_out)
    if name is None:
        raise ValueError("no transform")
    return TRANSFORMS[name](query)

def solve_M130(grid):
    h,w=dims(grid)
    comps=[(color,cells) for color,cells in cc(grid, ignore=(0,1))]
    if not comps:
        return blank(h,w)
    # largest component as prototype
    proto_color, proto_cells=max(comps, key=lambda t: len(t[1]))
    proto=crop_cells(grid, proto_cells)
    # bbox top-left of proto in source
    pr0,pr1,pc0,pc1=bbox(proto_cells)
    # output stamps prototype crop with its top-left anchored at each 1
    out=blank(h,w)
    anchors=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==1]
    ph,pw=dims(proto)
    for ar,ac in anchors:
        for r in range(ph):
            for c in range(pw):
                v=proto[r][c]
                if v!=0:
                    nr,nc=ar+r,ac+c
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out

def solve_M131(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        r0,r1,c0,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out

def solve_M132(grid):
    h,w=dims(grid)
    ar=ac=None
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                ar,ac=r,c
    out[ar][ac]=9
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,9):
                out[r][c]=v
                nr,nc=2*ar-r,2*ac-c
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out

def solve_M133(grid):
    comps=[]
    for color,cells in cc(grid):
        piece=crop_cells(grid,cells)
        area=len(cells)
        r0,r1,c0,c1=bbox(cells)
        comps.append((area,r0,c0,color,piece))
    comps.sort(key=lambda t:(-t[0], t[1], t[2], t[3]))
    if not comps:
        return [[0]]
    heights=[dims(p)[0] for _,_,_,_,p in comps]
    widths=[dims(p)[1] for _,_,_,_,p in comps]
    out=blank(max(heights), sum(widths)+max(0,len(comps)-1))
    c0=0
    for i,(_,_,_,_,piece) in enumerate(comps):
        ph,pw=dims(piece)
        for r in range(ph):
            for c in range(pw):
                if piece[r][c]!=0:
                    out[r][c0+c]=piece[r][c]
        c0+=pw
        if i<len(comps)-1:
            c0+=1

    return out

def solve_H127(grid):
    ex_in, ex_out, query = split_panel_row1(grid,3,sep=1)
    # infer transform by support
    support_ex_in=[[1 if v!=0 else 0 for v in row] for row in ex_in]
    support_ex_out=[[1 if v!=0 else 0 for v in row] for row in ex_out]
    chosen=None
    for name,fn in TRANSFORMS.items():
        t=fn(support_ex_in)
        if dims(t)==dims(support_ex_out) and t==support_ex_out:
            chosen=name; break
    if chosen is None:
        raise ValueError("no support transform")
    tq=TRANSFORMS[chosen](query)
    tex=TRANSFORMS[chosen](ex_in)
    # infer color mapping from transformed example to ex_out
    mapping={}
    h,w=dims(ex_out)
    for r in range(h):
        for c in range(w):
            a=tex[r][c]; b=ex_out[r][c]
            if a!=0 and b!=0:
                mapping[a]=b
    out=clone(tq)
    for r in range(len(out)):
        for c in range(len(out[0])):
            if out[r][c]!=0:
                out[r][c]=mapping.get(out[r][c], out[r][c])
    return out

def solve_H128(grid):
    a,b,res,c,d = split_panel_row1(grid,5,sep=1)
    def occ(g): return [[1 if v!=0 else 0 for v in row] for row in g]
    oa,ob,or_=occ(a),occ(b),occ(res)
    def union(x,y): return [[1 if x[r][c] or y[r][c] else 0 for c in range(len(x[0]))] for r in range(len(x))]
    def inter(x,y): return [[1 if x[r][c] and y[r][c] else 0 for c in range(len(x[0]))] for r in range(len(x))]
    def xor(x,y): return [[1 if (x[r][c]+y[r][c])%2==1 else 0 for c in range(len(x[0]))] for r in range(len(x))]
    ops={"union":union,"intersection":inter,"xor":xor}
    opname=None
    for name,fn in ops.items():
        if fn(oa,ob)==or_:
            opname=name; break
    if opname is None: raise ValueError("no op")
    o=ops[opname](occ(c), occ(d))
    # query color = first nonzero in c or d
    qcolor=0
    for panel in (c,d):
        for row in panel:
            for v in row:
                if v!=0:
                    qcolor=v; break
            if qcolor: break
        if qcolor: break
    out=blank(len(o), len(o[0]))
    for r in range(len(o)):
        for cc_ in range(len(o[0])):
            if o[r][cc_]:
                out[r][cc_]=qcolor
    return out

def solve_H129(grid):
    before, after, query = split_panel_row1(grid,3,sep=1)
    # compute delta relative to bbox of before
    comps=cc(before)
    # assume one component
    color_b, cells_b = comps[0]
    r0,r1,c0,c1=bbox(cells_b)
    support_b={(r-r0,c-c0) for r,c in cells_b}
    color_a, cells_a = cc(after)[0]
    ra0,ra1,ca0,ca1=bbox(cells_a)
    support_a={(r-ra0,c-ca0) for r,c in cells_a}
    delta = support_a - support_b
    # apply to query's main component
    qcolor, qcells = cc(query)[0]
    qr0,qr1,qc0,qc1=bbox(qcells)
    out=clone(query)
    for dr,dc in delta:
        nr,nc=qr0+dr,qc0+dc
        if 0<=nr<len(out) and 0<=nc<len(out[0]):
            out[nr][nc]=qcolor
    return out

def solve_H130(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); room=[]
            seeds=[]
            while q:
                x,y=q.popleft(); room.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            for x,y in room:
                if grid[x][y]==0 and seeds:
                    dists=sorted((abs(x-sr)+abs(y-sc), col) for sr,sc,col in seeds)
                    if len(dists)>=2 and dists[0][0]==dists[1][0] and dists[0][1]!=dists[1][1]:
                        out[x][y]=9
                    else:
                        out[x][y]=dists[0][1]
    return out

def solve_H131(grid):
    p1,p2,p3,query = split_panel_row1(grid,4,sep=1)
    protos=[p1,p2,p3]
    qsupp,qcolor=normalize_support(query)
    match_idx=None
    for i,p in enumerate(protos):
        psupp,_=normalize_support(p)
        fam={transform_support(psupp,fn) for fn in TRANSFORMS.values()}
        if qsupp in fam:
            match_idx=i; break
    if match_idx is None: raise ValueError("no family")
    canon_supp,_=normalize_support(protos[match_idx])
    return apply_support(canon_supp, qcolor)

def solve_H132(grid):
    ex_in, ex_out, x, y = split_panel_row1(grid,4,sep=1)
    name=infer_transform(ex_in, ex_out)
    if name is None: raise ValueError("no transform")
    tx=TRANSFORMS[name](x)
    h,w=dims(tx)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a,b=tx[r][c], y[r][c]
            if a==0 and b==0:
                out[r][c]=0
            elif a==0:
                out[r][c]=b
            elif b==0:
                out[r][c]=a
            elif a==b:
                out[r][c]=a
            else:
                out[r][c]=9
    return out

def solve_H133(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=grid[1:]
    comps=[]
    for color,cells in cc(body):
        piece=crop_cells(body,cells)
        area=len(cells)
        r0,r1,c0,c1=bbox(cells)
        comps.append((area,r0,c0,piece))
    comps.sort(key=lambda t:(t[0], t[1], t[2]))  # ascending area
    recolored=[]
    for i,(area,r0,c0,piece) in enumerate(comps):
        ph,pw=dims(piece)
        rp=blank(ph,pw)
        color=palette[i]
        for r in range(ph):
            for c in range(pw):
                if piece[r][c]!=0:
                    rp[r][c]=color
        recolored.append(rp)
    if not recolored:
        return [[0]]
    out=blank(max(dims(p)[0] for p in recolored), sum(dims(p)[1] for p in recolored)+max(0,len(recolored)-1))
    c0=0
    for i,p in enumerate(recolored):
        ph,pw=dims(p)
        for r in range(ph):
            for c in range(pw):
                if p[r][c]!=0:
                    out[r][c0+c]=p[r][c]
        c0+=pw
        if i<len(recolored)-1:
            c0+=1
    return out

