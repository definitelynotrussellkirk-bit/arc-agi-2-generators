"""
ARC-style puzzle bank continuation 21: 21 more puzzles (E141-E147, M141-M147, H141-H147).

This batch leans into object filtering, guide-derived motion, panel selection, size-ranked recoloring,
transform analogy, support edits, anchor orbits, and tokenized transform execution.

Notable motifs:
- guide_union(shape, guide_a, guide_b): M143
- mask_carry_crop(mask, canvas): M144
- support_recolor_analogy(A, B, C): H141
- counted_orbit(anchor, object, k): H146
- token_transform_execute(tokens, shape): H147
"""
from __future__ import annotations
from collections import deque
from typing import List
import math, heapq

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

def crop_bbox(g, ignore=(0,)):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in ignore]
    if not cells: return [[0]]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_component(g, cells):
    r0,r1,c0,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    color=g[cells[0][0]][cells[0][1]]
    for r,c in cells: out[r-r0][c-c0]=color
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

def split_by_full_sep_cols(g, sep=8):
    h,w=dims(g)
    seps=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    parts=[]; start=0
    for c in seps+[w]:
        parts.append([row[start:c] for row in g])
        start=c+1
    return parts

def support(g):
    return {(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0}

def normalize_support(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return frozenset()
    r0,r1,c0,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def apply_color_map(g, mapping):
    return [[mapping.get(v,v) if v!=0 else 0 for v in row] for row in g]

def pack_h(grids, gap=1):
    if not grids: return [[0]]
    h=max(len(g) for g in grids)
    w=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=blank(h,w)
    c0=0
    for g in grids:
        gh,gw=dims(g)
        for r in range(gh):
            for c in range(gw):
                out[r][c0+c]=g[r][c]
        c0 += gw + gap
    return out

def components_body(grid, start_row=1):
    h,w=dims(grid)
    seen=set(); out=[]
    for r in range(start_row,h):
        for c in range(w):
            if (r,c) in seen or grid[r][c]==0: continue
            color=grid[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if start_row<=nx<h and 0<=ny<w and (nx,ny) not in seen and grid[nx][ny]==color:
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((color,cells))
    return out

def infer_transform_and_color_map(a,b):
    for name,fn in TRANSFORMS.items():
        ta=fn(a)
        if dims(ta)!=dims(b):
            continue
        mapping={}
        ok=True
        for r in range(len(ta)):
            for c in range(len(ta[0])):
                va,vb=ta[r][c],b[r][c]
                if (va==0)!=(vb==0):
                    ok=False; break
                if va!=0:
                    if va in mapping and mapping[va]!=vb:
                        ok=False; break
                    mapping[va]=vb
            if not ok: break
        if ok:
            return name,mapping
    raise ValueError("no transform")

def rotate_point_about_anchor(r,c, ar,ac, quarter_turns):
    x,y=r,c
    for _ in range(quarter_turns%4):
        x,y = ar-(y-ac), ac+(x-ar)
    return x,y

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

def solve_E141(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        nz=[(c,v) for c,v in enumerate(row) if v!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            c0,c1=nz[0][0],nz[1][0]
            color=nz[0][1]
            for c in range(min(c0,c1), max(c0,c1)+1):
                out[r][c]=color
    return out

def solve_E142(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c in range(w):
        for r in range(h):
            if grid[r][c]!=0:
                out[r][c]=grid[r][c]
                break
    return out

def solve_E143(grid):
    h,w=dims(grid)
    div=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    out=clone(grid)
    for r in range(h):
        for c in range(div):
            v=grid[r][c]
            if v not in (0,8):
                mc=div + (div-c)
                if mc<w:
                    out[r][mc]=v
    return out

def solve_E144(grid):
    return crop_bbox(grid)

def solve_E145(grid):
    h,w=dims(grid)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    assert len(seeds)==1
    r,c,v=seeds[0]
    for j in range(w): out[r][j]=v
    for i in range(h): out[i][c]=v
    return out

def solve_E146(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells: out[r][c]=color
    return out

def solve_E147(grid):
    h,w=dims(grid)
    proto=[row[:2] for row in grid[:2]]
    out=blank(h,w)
    for r in range(2,h-1):
        for c in range(2,w-1):
            if grid[r][c]==9:
                for dr in range(2):
                    for dc in range(2):
                        if proto[dr][dc]!=0:
                            out[r+dr][c+dc]=proto[dr][dc]
    return out

def solve_M141(grid):
    h,w=dims(grid)
    wall=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    out=blank(h,w)
    for r in range(h): out[r][wall]=8
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
    side=1 if all(c<wall for r,c,v in cells) else -1
    for r,c,v in cells:
        if side==1:
            for j in range(c, wall):
                out[r][j]=v
        else:
            for j in range(wall+1, c+1):
                out[r][j]=v
    return out

def solve_M142(grid):
    h,w=dims(grid)
    key_cols=[c for c,v in enumerate(grid[0]) if v!=0]
    proto_by_key={}
    for c in key_cols:
        proto_by_key[grid[0][c]]=[grid[1][c:c+2], grid[2][c:c+2]]
    out=blank(h,w)
    for r in range(3,h-1):
        for c in range(w-1):
            key=grid[r][c]
            if key in proto_by_key:
                proto=proto_by_key[key]
                for dr in range(2):
                    for dc in range(2):
                        v=proto[dr][dc]
                        if v!=0:
                            out[r+dr][c+dc]=v
    return out

def solve_M143(grid):
    h,w=dims(grid)
    guides=sorted((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==9)
    (r1,c1),(r2,c2)=guides
    dr,dc=r2-r1,c2-c1
    out=blank(h,w)
    for color,cells in cc(grid, ignore=(0,9)):
        for r,c in cells:
            out[r][c]=color
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=color
    return out

def solve_M144(grid):
    h,w=dims(grid)
    div=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    mask=[row[:div] for row in grid]
    canvas=[row[div+1:] for row in grid]
    selected=[]
    for r in range(h):
        for c in range(div):
            if mask[r][c]!=0 and canvas[r][c]!=0:
                selected.append((r,c,canvas[r][c]))
    if not selected:
        return [[0]]
    rs=[r for r,c,v in selected]; cs=[c for r,c,v in selected]
    r0,r1,c0,c1=min(rs),max(rs),min(cs),max(cs)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c,v in selected:
        out[r-r0][c-c0]=v
    return out

def solve_M145(grid):
    comps=[(len(cells), crop_component(grid,cells)) for color,cells in cc(grid)]
    comps.sort(key=lambda x: x[0])
    return pack_h([g for _,g in comps], gap=1)

def solve_M146(grid):
    palette=[v for v in grid[0] if v!=0]
    comps=components_body(grid,1)
    comps.sort(key=lambda x: len(x[1]))
    out=blank(*dims(grid))
    for rank,(orig,cells) in enumerate(comps):
        color=palette[rank]
        for r,c in cells:
            out[r][c]=color
    return out

def solve_M147(grid):
    marker=None
    shape_cells=[]
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in (8,9):
                marker=v
            elif v!=0:
                shape_cells.append((r,c))
    r0,r1,c0,c1=bbox(shape_cells)
    shape=[row[c0:c1+1] for row in grid[r0:r1+1]]
    return rot90(shape) if marker==8 else flip_h(shape)

def solve_H141(grid):
    a,b,c=split_by_full_sep_cols(grid, sep=8)
    name,mapping=infer_transform_and_color_map(a,b)
    return apply_color_map(TRANSFORMS[name](c), mapping)

def solve_H142(grid):
    before,after,query=split_by_full_sep_cols(grid, sep=8)
    qcolor=next(v for row in query for v in row if v!=0)
    out=clone(query)
    h,w=dims(before)
    for r in range(h):
        for c in range(w):
            b=before[r][c]!=0
            a=after[r][c]!=0
            if b and not a:
                out[r][c]=0
            elif not b and a:
                out[r][c]=qcolor
    return out

def solve_H143(grid):
    a,b,q=split_by_full_sep_cols(grid, sep=8)
    supp_q=normalize_support(q)
    for name,fn in TRANSFORMS.items():
        if normalize_support(fn(a))==supp_q:
            return a
    return b

def solve_H144(grid):
    h,w=dims(grid)
    dist=[[math.inf]*w for _ in range(h)]
    col=[[0]*w for _ in range(h)]
    pq=[]
    for r in range(h):
        for c in range(w):
            if grid[r][c] not in (0,8):
                dist[r][c]=0
                col[r][c]=grid[r][c]
                heapq.heappush(pq,(0,grid[r][c],r,c))
            elif grid[r][c]==8:
                col[r][c]=8
    while pq:
        d,color,r,c=heapq.heappop(pq)
        if d!=dist[r][c] or color!=col[r][c]:
            continue
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc]!=8:
                nd=d+1
                if nd<dist[nr][nc] or (nd==dist[nr][nc] and color<col[nr][nc]):
                    dist[nr][nc]=nd
                    col[nr][nc]=color
                    heapq.heappush(pq,(nd,color,nr,nc))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=8 if grid[r][c]==8 else col[r][c]
    return out

def solve_H145(grid):
    a,b,r,c,d=split_by_full_sep_cols(grid, sep=8)
    ops={
        "union": lambda x,y: x|y,
        "intersection": lambda x,y: x&y,
        "xor": lambda x,y: x^y,
    }
    sa,sb,sr=support(a),support(b),support(r)
    op=None
    for name,fn in ops.items():
        if fn(sa,sb)==sr:
            op=fn; break
    qcolor=next(v for panel in (c,d) for row in panel for v in row if v!=0)
    out=blank(*dims(c))
    for r0,c0 in op(support(c), support(d)):
        out[r0][c0]=qcolor
    return out

def solve_H146(grid):
    k=sum(1 for v in grid[0] if v==1)
    body=[row[:] for row in grid[1:]]
    h,w=dims(body)
    ar,ac=[(r,c) for r,row in enumerate(body) for c,v in enumerate(row) if v==9][0]
    obj=[(r,c,v) for r,row in enumerate(body) for c,v in enumerate(row) if v not in (0,9)]
    out=blank(h,w)
    out[ar][ac]=9
    for turns in range(k+1):
        for r,c,v in obj:
            nr,nc=rotate_point_about_anchor(r,c, ar,ac, turns)
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

def solve_H147(grid):
    tokens=[v for v in grid[0] if v!=0]
    shape=crop_bbox(grid[2:])
    op_map={2:rot90, 3:flip_h, 4:transpose}
    out=shape
    for t in tokens:
        out=op_map[t](out)
    return out
