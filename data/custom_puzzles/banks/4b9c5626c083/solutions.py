"""
ARC-style puzzle bank continuation 15: 21 more puzzles (E99-E105, M99-M105, H99-H105).

This batch leans into vector-guided translation, header-driven recoloring, count-based tiling,
room filling, example-inferred panel transforms, replayed panel edits, prototype dispatch,
blocked sweeping, anchor orbits, and geodesic nearest-seed filling.

Notable motifs:
- guide_vector_move(object, src_marker, dst_marker): M99
- panel_edit_replay(example_before, example_after, query): H100
- prototype_dispatch_rot(prototypes, labels, query): H101
- object_sweep_until_block(shape, direction, walls): H103
- geodesic_voronoi_fill(seeds, walls): H105
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def bbox_of_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def connected_components(g, ignore=(0,), same_color=True):
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c] in ignore:
                continue
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

def rot90(g):
    return [list(row) for row in zip(*g[::-1])]

def rot180(g):
    return [row[::-1] for row in g[::-1]]

def rot270(g):
    return [list(row) for row in zip(*g)][::-1]

def flip_h(g): # horizontal mirror left-right
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def transpose(g):
    return [list(row) for row in zip(*g)]

def apply_transform(g, name):
    if name=="id": return [row[:] for row in g]
    if name=="rot90": return rot90(g)
    if name=="rot180": return rot180(g)
    if name=="rot270": return rot270(g)
    if name=="flip_h": return flip_h(g)
    if name=="flip_v": return flip_v(g)
    if name=="transpose": return transpose(g)
    if name=="anti_transpose": return flip_h(transpose(g))
    raise ValueError(name)

def paste(g, top,left, sub, transparent=0):
    h,w=dims(sub)
    for r in range(h):
        for c in range(w):
            v=sub[r][c]
            if v!=transparent:
                g[top+r][left+c]=v
    return g

def split_panels_row(grid, n, sep_color=5, count=3):
    panels=[]
    start=0
    for i in range(count):
        panel=[row[start:start+n] for row in grid]
        panels.append(panel)
        start += n
        if i < count-1:
            # skip separator
            start += 1
    return panels

def panels5(grid):
    h,w=dims(grid)
    n=h
    panels=[]
    start=0
    for i in range(5):
        panels.append([row[start:start+n] for row in grid])
        start += n
        if i<4: start += 1
    return panels

def occupancy(g):
    return {(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0}

def recolor_shape(g,color):
    return [[color if v!=0 else 0 for v in row] for row in g]

def rotate_offset(dr,dc,quarters):
    for _ in range(quarters%4):
        dr,dc = dc,-dr
    return dr,dc

def solve_E99(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][0]==cells[1][0]:
            r=cells[0][0]
            a,b=sorted([cells[0][1],cells[1][1]])
            if all(grid[r][c]==0 for c in range(a+1,b)):
                for c in range(a,b+1):
                    out[r][c]=color
    return out

def solve_E100(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2:
                a,b=sorted([c1,c2])
                if (b-a)%2==0 and all(grid[r1][c]==0 for c in range(a+1,b)):
                    out[r1][(a+b)//2]=color
            elif c1==c2:
                a,b=sorted([r1,r2])
                if (b-a)%2==0 and all(grid[r][c1]==0 for r in range(a+1,b)):
                    out[(a+b)//2][c1]=color
    return out

def solve_E101(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r+1][c],grid[r][c+1],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                color=nz[0]
                if vals[0]==0: out[r][c]=color
                if vals[1]==0: out[r+1][c]=color
                if vals[2]==0: out[r][c+1]=color
                if vals[3]==0: out[r+1][c+1]=color
    return out

def solve_E102(grid):
    h,w=dims(grid)
    comps=connected_components(grid)
    if not comps:
        return blank(h,w)
    best=max(comps, key=lambda vc:(len(vc[1]), -min(r for r,c in vc[1]), -min(c for r,c in vc[1])))
    out=blank(h,w)
    color,cells=best
    for r,c in cells:
        out[r][c]=color
    return out

def solve_E103(grid):
    h,w=dims(grid)
    out=blank(h,w)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                by[grid[r][c]].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                rlo,rhi=sorted([r1,r2]); clo,chi=sorted([c1,c2])
                for c in range(clo,chi+1):
                    out[rlo][c]=color; out[rhi][c]=color
                for r in range(rlo,rhi+1):
                    out[r][clo]=color; out[r][chi]=color
    return out

def solve_E104(grid):
    h,w=dims(grid)
    assert h==w
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                out[c][r]=v
    return out

def solve_E105(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid):
        if all(0<r<h-1 and 0<c<w-1 for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out

def solve_M99(grid):
    h,w=dims(grid)
    p8=p9=None
    obj=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==8: p8=(r,c)
            elif v==9: p9=(r,c)
            elif v!=0: obj.append((r,c,v))
    dr=p9[0]-p8[0]; dc=p9[1]-p8[1]
    out=blank(h,w)
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out

def solve_M100(grid):
    h,w=dims(grid)
    out=blank(h,w)
    headers=grid[0]
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]!=0:
                out[r][c]=headers[c]
    return out

def solve_M101(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v==9)
    cells=[(r,c) for r in range(1,h) for c in range(w) if grid[r][c]!=0]
    r0,r1,c0,c1=bbox_of_cells(cells)
    obj=[row[c0:c1+1] for row in grid[r0:r1+1]]
    oh,ow=dims(obj)
    out=blank(oh, ow*k + (k-1))
    x=0
    for i in range(k):
        paste(out,0,x,obj)
        x += ow+1
    return out

def solve_M102(grid):
    h,w=dims(grid)
    anchor=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                anchor=(r,c)
    out=blank(h,w)
    best=None
    for color,cells in connected_components(grid, ignore=(0,9)):
        dist=min(abs(r-anchor[0])+abs(c-anchor[1]) for r,c in cells)
        key=(dist, len(cells), min(r for r,c in cells), min(c for r,c in cells))
        if best is None or key < best[0]:
            best=(key,color,cells)
    if best:
        _,color,cells=best
        for r,c in cells:
            out[r][c]=color
    return out

def solve_M103(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=1 and (r,c) not in seen:
                q=deque([(r,c)]); seen.add((r,c)); room=[]; seeds={}
                while q:
                    x,y=q.popleft(); room.append((x,y))
                    if grid[x][y]!=0:
                        seeds[grid[x][y]]=seeds.get(grid[x][y],0)+1
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=1 and (nx,ny) not in seen:
                            seen.add((nx,ny)); q.append((nx,ny))
                if len(seeds)==1:
                    color=next(iter(seeds))
                    for x,y in room:
                        if out[x][y]==0:
                            out[x][y]=color
    return out

def solve_M104(grid):
    h,w=dims(grid)
    marker=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9: marker=(r,c)
            elif v!=0: cells.append((r,c))
    r0,r1,c0,c1=bbox_of_cells(cells)
    sub=[row[c0:c1+1] for row in grid[r0:r1+1]]
    out=blank(h,w)
    paste(out,marker[0],marker[1],sub)
    return out

def solve_M105(grid):
    h,w=dims(grid)
    out=blank(h,w)
    dirs={1:(-1,0), 2:(1,0), 3:(0,-1), 4:(0,1)}
    used=set()
    for r in range(h):
        for c in range(w):
            code=grid[r][c]
            if code in dirs:
                dr,dc=dirs[code]
                sr,sc=r-dr,c-dc  # seed sits opposite to travel direction: marker is just beyond seed
                if 0<=sr<h and 0<=sc<w and grid[sr][sc] not in (0,1,2,3,4):
                    color=grid[sr][sc]
                    x,y=sr,sc
                    while 0<=x<h and 0<=y<w:
                        out[x][y]=color
                        x+=dr; y+=dc
    return out

def solve_H99(grid):
    h,w=dims(grid)
    n=h
    A,B,C = split_panels_row(grid,n,count=3)
    transforms=["rot90","rot180","rot270","flip_h","flip_v","transpose"]
    chosen=None
    for t in transforms:
        if apply_transform(A,t)==B:
            chosen=t
            break
    if chosen is None:
        raise ValueError("no transform match")
    return apply_transform(C,chosen)

def solve_H100(grid):
    h,w=dims(grid)
    n=h
    A,B,C = split_panels_row(grid,n,count=3)
    out=clone(C)
    for r in range(n):
        for c in range(n):
            if A[r][c]==0 and B[r][c]!=0:
                out[r][c]=B[r][c]
            elif A[r][c]!=0 and B[r][c]==0:
                out[r][c]=0
            elif A[r][c]!=B[r][c] and A[r][c]!=0 and B[r][c]!=0:
                out[r][c]=B[r][c]
    return out

def solve_H101(grid):
    n=len(grid)
    P1,L1,P2,L2,Q = panels5(grid)
    label1=next(v for row in L1 for v in row if v!=0)
    label2=next(v for row in L2 for v in row if v!=0)
    q_occ=occupancy(Q)
    p1_vars=[occupancy(apply_transform(P1,t)) for t in ["id","rot90","rot180","rot270"]]
    p2_vars=[occupancy(apply_transform(P2,t)) for t in ["id","rot90","rot180","rot270"]]
    if q_occ in p1_vars:
        return recolor_shape(Q,label1)
    if q_occ in p2_vars:
        return recolor_shape(Q,label2)
    raise ValueError("query matches no prototype")

def solve_H102(grid):
    n=len(grid)-1
    col_headers=grid[0][1:]
    row_headers=[grid[r][0] for r in range(1,n+1)]
    body=[row[1:] for row in grid[1:]]
    row_order=sorted(range(n), key=lambda i: row_headers[i])
    col_order=sorted(range(n), key=lambda i: col_headers[i])
    return [[body[r][c] for c in col_order] for r in row_order]

def solve_H103(grid):
    h,w=dims(grid)
    dirs={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}
    code_cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] in dirs]
    if len(code_cells)!=1:
        raise ValueError("need exactly one direction marker")
    r0,c0,code=code_cells[0]
    walls={(r,c) for r in range(h) for c in range(w) if grid[r][c]==8}
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,8,1,2,3,4)]
    dr,dc=dirs[code]
    out=blank(h,w)
    for r,c in walls:
        out[r][c]=8
    cur=obj[:]
    while True:
        for r,c,v in cur:
            out[r][c]=v
        nxt=[(r+dr,c+dc,v) for r,c,v in cur]
        if any(not (0<=r<h and 0<=c<w) or (r,c) in walls for r,c,v in nxt):
            break
        cur=nxt
    return out

def solve_H104(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v==1)
    anchor=None
    shape=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v not in (0,1):
                shape.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w)
    out[ar][ac]=9
    for quarter in range(k):
        for r,c,v in shape:
            if (r,c)==anchor: 
                continue
            dr,dc=r-ar,c-ac
            nr_off,nc_off=rotate_offset(dr,dc,quarter)
            nr,nc=ar+nr_off,ac+nc_off
            if 0<=nr<h and 0<=nc<w and not (nr==ar and nc==ac):
                out[nr][nc]=v
    return out

def solve_H105(grid):
    h,w=dims(grid)
    walls={(r,c) for r in range(h) for c in range(w) if grid[r][c]==1}
    seeds=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,1)]
    dist_maps={}
    for sr,sc,color in seeds:
        q=deque([(sr,sc)])
        dist={(sr,sc):0}
        while q:
            r,c=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in walls and (nr,nc) not in dist:
                    dist[(nr,nc)] = dist[(r,c)] + 1
                    q.append((nr,nc))
        dist_maps[(sr,sc,color)] = dist
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0:
                best=None; best_colors=[]
                for seed,dist in dist_maps.items():
                    if (r,c) in dist:
                        d=dist[(r,c)]
                        color=seed[2]
                        if best is None or d<best:
                            best=d; best_colors=[color]
                        elif d==best and color not in best_colors:
                            best_colors.append(color)
                if best is not None and len(best_colors)==1:
                    out[r][c]=best_colors[0]
    return out
