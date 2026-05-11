"""
ARC-style puzzle bank continuation 3: 21 more puzzles (E15-E21, M15-M21, H15-H21).
Each solve_* function is a reference program for one puzzle.
"""
from __future__ import annotations
from typing import List, Tuple
from collections import deque, defaultdict, Counter

Grid = List[List[int]]

def parse_grid(lines):
    return [[int(ch) for ch in line.strip()] for line in lines]

def grid_to_strings(g):
    return [''.join(str(x) for x in row) for row in g]

def dims(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def components(g):
    h,w=dims(g)
    seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or (r,c) in seen: continue
            col=g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]==col and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col,cells))
    return comps

def crop_cells(cells):
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1)

def hole_cells_of_component(g, cells):
    r0,r1,c0,c1=bbox(cells)
    comp=set(cells)
    seen=set()
    q=deque()
    for r in range(r0,r1+1):
        for c in (c0,c1):
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    for c in range(c0,c1+1):
        for r in (r0,r1):
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    while q:
        x,y=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp and (nx,ny) not in seen:
                seen.add((nx,ny)); q.append((nx,ny))
    holes=[]; visited=set()
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if (r,c) not in comp and (r,c) not in seen and (r,c) not in visited:
                q=deque([(r,c)]); visited.add((r,c)); region=[]
                while q:
                    x,y=q.popleft(); region.append((x,y))
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp and (nx,ny) not in seen and (nx,ny) not in visited:
                            visited.add((nx,ny)); q.append((nx,ny))
                holes.append(region)
    return holes

def horizontal_runs(g):
    h,w=dims(g)
    runs=[]
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            v=g[r][c]; start=c
            while c+1<w and g[r][c+1]==v:
                c+=1
            end=c
            runs.append((r,start,end,v))
            c+=1
    return runs

def solve_E15(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0:
                vals=[g[r-1][c],g[r+1][c],g[r][c-1],g[r][c+1]]
                if vals[0]!=0 and len(set(vals))==1:
                    out[r][c]=vals[0]
    return out

def solve_E16(g):
    h,w=dims(g); out=clone(g)
    for c in range(w):
        nz=[(r,g[r][c]) for r in range(h) if g[r][c]!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            (r0,val),(r1,_) = nz
            if all(g[r][c]==0 for r in range(r0+1,r1)):
                for r in range(r0,r1+1):
                    out[r][c]=val
    return out

def solve_E17(g):
    out=clone(g)
    for r,c0,c1,val in horizontal_runs(g):
        if c1-c0+1==3:
            out[r][c0+1]=8
    return out

def solve_E18(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            if r+1<h and g[r+1][c]==0:
                out[r+1][c]=v
            else:
                out[r][c]=v
    return out

def solve_E19(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            nbrs=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if all(not (0<=nr<h and 0<=nc<w and g[nr][nc]!=0) for nr,nc in nbrs):
                for nr,nc in nbrs:
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=v
    return out

def solve_E20(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
                out[r][c+1]=0
                out[r+1][c]=0
                out[r+1][c+1]=vals[0]
    return out

def solve_E21(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            cnt=sum(1 for nr,nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)] if 0<=nr<h and 0<=nc<w and g[nr][nc]==v)
            if cnt==1:
                out[r][c]=8
    return out

def solve_M15(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        if (r1-r0)==(c1-c0):
            for r,c in cells: out[r][c]=col
    return out

def solve_M16(g):
    h,w=dims(g)
    comps=components(g)
    def score(item):
        _,cells=item
        r0,r1,c0,c1=bbox(cells)
        return (abs((r0+r1)-(h-1))+abs((c0+c1)-(w-1)), len(cells), r0, c0)
    chosen=min(comps,key=score)
    out=clone(g)
    for r,c in chosen[1]: out[r][c]=8
    return out

def solve_M17(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for r,c in cells: out[r][c-c0]=col
    return out

def solve_M18(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        out[(r0+r1)//2][(c0+c1)//2]=col
    return out

def solve_M19(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def solve_M20(g):
    out=clone(g)
    for col,cells in components(g):
        for region in hole_cells_of_component(g,cells):
            for r,c in region: out[r][c]=col
    return out

def solve_M21(g):
    h,w=dims(g); by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: by[g[r][c]].append((r,c))
    out=[[0]*w for _ in range(h)]
    for col,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            for r in range(min(r1,r2),max(r1,r2)+1):
                for c in range(min(c1,c2),max(c1,c2)+1):
                    out[r][c]=col
    return out

def solve_H15(g):
    reps=[]
    for col,cells in components(g):
        shape,(H,W)=crop_cells(cells)
        reps.append((col,shape,H,W))
    counts=Counter((frozenset(shape),H,W) for col,shape,H,W in reps)
    odd=[item for item in reps if counts[(frozenset(item[1]),item[2],item[3])]==1]
    assert len(odd)==1
    col,shape,H,W=odd[0]
    out=[[0]*W for _ in range(H)]
    for r,c in shape: out[r][c]=col
    return out

def solve_H16(g):
    h,w=dims(g)
    comps=[(col,cells) for col,cells in components(g) if col!=9]
    assert len(comps)==1
    col,cells=comps[0]
    shape,(H,W)=crop_cells(cells)
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=[[0]*w for _ in range(h)]
    for mr,mc in markers:
        for r,c in shape:
            out[mr+r][mc+c]=col
    return out

def solve_H17(g):
    comps=components(g); assert len(comps)==2
    (col1,cells1),(col2,cells2)=comps
    shape1,(H1,W1)=crop_cells(cells1)
    shape2,(H2,W2)=crop_cells(cells2)
    H=max(H1,H2); W=max(W1,W2)
    s1=set(shape1); s2=set(shape2)
    out=[[0]*W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if (r,c) in s1 and (r,c) in s2: out[r][c]=8
            elif (r,c) in s1: out[r][c]=col1
            elif (r,c) in s2: out[r][c]=col2
    return out

def solve_H18(g):
    h,w=dims(g)
    axis_cols={c for r in range(h) for c in range(w) if g[r][c]==7}
    assert len(axis_cols)==1
    axis=next(iter(axis_cols))
    out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=7:
                out[r][c]=v
                mc=2*axis-c
                if 0<=mc<w: out[r][mc]=v
    return out

def solve_H19(g):
    items=[]
    for col,cells in components(g):
        shape,(H,W)=crop_cells(cells)
        holes=len(hole_cells_of_component(g,cells))
        items.append((holes,col,shape,H,W))
    items.sort(key=lambda x:(x[0],x[1]))
    total_w=sum(W for _,_,_,_,W in items)+max(0,len(items)-1)
    max_h=max(H for _,_,_,H,_ in items)
    out=[[0]*total_w for _ in range(max_h)]
    cur=0
    for holes,col,shape,H,W in items:
        for r,c in shape:
            out[r][cur+c]=col
        cur += W+1
    return out

def solve_H20(g):
    comps=components(g)
    items=[]
    common=None
    for col,cells in comps:
        shape,(H,W)=crop_cells(cells)
        items.append((col,shape,H,W,bbox(cells)[0],bbox(cells)[2]))
        if common is None: common=frozenset(shape)
        else: assert frozenset(shape)==common
    pivot=min(items,key=lambda t:(t[4],t[5]))
    horiz=[it for it in items if it[4]==pivot[4] and it[5]!=pivot[5]]
    vert=[it for it in items if it[5]==pivot[5] and it[4]!=pivot[4]]
    assert horiz and vert
    col,shape,H,W,_,_=pivot
    mr=vert[0][4]; mc=horiz[0][5]
    out=clone(g)
    for r,c in shape: out[mr+r][mc+c]=col
    return out

def solve_H21(g):
    comps=components(g)
    col=comps[0][0]
    union=set()
    for _,cells in comps:
        shape,(H,W)=crop_cells(cells)
        union |= set(shape)
    H=max(r for r,c in union)+1
    W=max(c for r,c in union)+1
    out=[[0]*W for _ in range(H)]
    for r,c in union: out[r][c]=col
    return out
