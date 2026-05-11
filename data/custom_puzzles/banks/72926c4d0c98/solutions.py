"""
ARC-style puzzle bank continuation 13: 21 more puzzles (E85-E91, M85-M91, H85-H91).

This batch leans into local completion, object relocation, command-conditioned
geometry, prototype stamping, palette remapping, distance-based chamber fills,
masked carry crops, sweep unions, and operation inference from examples.

Notable motifs:
- example_inferred_transform(example_in, example_out, query): H85
- prototype_dictionary_lookup(keys, prototypes, query): H89
- sweep_union_until_wall(object, wall): H90
- binary_op_from_example(A, B, C): H91
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import List, Tuple

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def bbox_cells(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,r1,c0,c1 = bbox_cells(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def rot90(grid):
    h,w=dims(grid)
    return [[grid[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(grid):
    return [row[::-1] for row in grid[::-1]]

def rot270(grid):
    return rot90(rot180(grid))

def flip_h(grid):
    return [row[::-1] for row in grid]

def flip_v(grid):
    return grid[::-1]

def comps_samecolor(g, ignore=(0,)):
    h,w=dims(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in ignore or (r,c) in seen:
                continue
            q=deque([(r,c)])
            seen.add((r,c))
            cells=[]
            while q:
                x,y=q.popleft()
                cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny]==v:
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((v,cells))
    return out

def paste(out, obj, r0, c0):
    h,w=dims(obj)
    H,W=dims(out)
    for r in range(h):
        for c in range(w):
            if obj[r][c]!=0 and 0<=r0+r<H and 0<=c0+c<W:
                out[r0+r][c0+c]=obj[r][c]
    return out

def split_prototype_groups(g):
    # assume row0 has keys centered in 3-wide groups separated by one zero col
    row0=g[0]
    cols=[i for i,v in enumerate(row0) if v!=0]
    groups=[]
    for c in cols:
        groups.append((c-1,c+1,row0[c]))  # start,end,key
    return groups

def solve_E85(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][0]==cells[1][0]:
            r=cells[0][0]
            a,b=sorted([cells[0][1], cells[1][1]])
            if all(g[r][c]==0 for c in range(a+1,b)):
                for c in range(a,b+1):
                    out[r][c]=color
    return out

def solve_E86(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            vals=[g[r-1][c],g[r+1][c],g[r][c-1],g[r][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out

def solve_E87(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and 0 in vals:
                color=nz[0]
                if g[r][c]==0: out[r][c]=color
                if g[r][c+1]==0: out[r][c+1]=color
                if g[r+1][c]==0: out[r+1][c]=color
                if g[r+1][c+1]==0: out[r+1][c+1]=color
    return out

def solve_E88(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r][c+2] and g[r][c+1]==0:
                out[r][c+1]=g[r][c]
    for r in range(h-2):
        for c in range(w):
            if g[r][c]!=0 and g[r][c]==g[r+2][c] and g[r+1][c]==0:
                out[r+1][c]=g[r][c]
    return out

def solve_E89(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r+2][c+2] and g[r+1][c+1]==0:
                out[r+1][c+1]=g[r][c]
    for r in range(h-2):
        for c in range(2,w):
            if g[r][c]!=0 and g[r][c]==g[r+2][c-2] and g[r+1][c-1]==0:
                out[r+1][c-1]=g[r][c]
    return out

def solve_E90(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            border=[]
            ok=True
            for rr in range(r-1,r+2):
                for cc in range(c-1,c+2):
                    if (rr,cc)==(r,c): 
                        continue
                    border.append(g[rr][cc])
            if border[0]!=0 and all(v==border[0] for v in border):
                out[r][c]=border[0]
    return out

def solve_E91(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        if 9 not in g[r]:
            continue
        axis=g[r].index(9)
        for c,v in enumerate(g[r]):
            if v!=0 and v!=9:
                cc=2*axis-c
                if 0<=cc<w and out[r][cc]==0:
                    out[r][cc]=v
    return out

def solve_M85(g):
    h,w=dims(g)
    marker=None
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==9:
                marker=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w,0)
    if not cells or marker is None:
        return clone(g)
    r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
    r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
    obj=blank(r1-r0+1,c1-c0+1,0)
    for r,c,v in cells:
        obj[r-r0][c-c0]=v
    return paste(out,obj,marker[0],marker[1])

def solve_M86(g):
    cmd=g[0][0]
    canvas=clone(g)
    canvas[0][0]=0
    obj=crop_nonzero(canvas)
    if cmd==1:
        out=flip_h(obj)
    elif cmd==2:
        out=rot90(obj)
    elif cmd==3:
        out=rot180(obj)
    else:
        out=obj
    return out

def solve_M87(g):
    comps=comps_samecolor(g)
    if not comps:
        return clone(g)
    comps_sorted=sorted(comps,key=lambda vc: len(vc[1]))
    small_color=comps_sorted[0][0]
    large_cells=max(comps,key=lambda vc: len(vc[1]))[1]
    h,w=dims(g)
    out=blank(h,w,0)
    for r,c in large_cells:
        out[r][c]=small_color
    return out

def solve_M88(g):
    h,w=dims(g)
    seeds=[]
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==9: seeds.append((r,c))
            elif v!=0: cells.append((r,c,v))
    out=clone(g)
    for r,c in seeds: out[r][c]=0
    if not cells:
        return out
    r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
    r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
    obj=blank(r1-r0+1,c1-c0+1,0)
    for r,c,v in cells:
        obj[r-r0][c-c0]=v
    for sr,sc in seeds:
        out=paste(out,obj,sr,sc)
    return out

def solve_M89(g):
    h,w=dims(g)
    out=blank(h,w,0)
    frame=[(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8]
    cells=[(r,c,v) for r in range(h) for c,v in enumerate(g[r]) if v not in (0,8)]
    if not frame:
        return clone(g)
    fr0,fr1,fc0,fc1=bbox_cells(frame)
    for r,c in frame:
        out[r][c]=8
    if cells:
        r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
        r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
        obj=blank(r1-r0+1,c1-c0+1,0)
        for r,c,v in cells:
            obj[r-r0][c-c0]=v
        paste(out,obj,fr0+1,fc0+1)
    return out

def solve_M90(g):
    h,w=dims(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    if sep is None:
        return clone(g)
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    h2,w2=dims(left)
    out=blank(h2,w2,0)
    for r in range(h2):
        for c in range(w2):
            if (left[r][c]!=0) ^ (right[r][c]!=0):
                out[r][c]=2
    return out

def solve_M91(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for color,cells in comps_samecolor(g):
        r0,r1,c0,c1=bbox_cells(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out

def solve_H85(g):
    h,w=dims(g)
    sep_r=None; sep_c=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep_r=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep_c=c; break
    if sep_r is None or sep_c is None:
        return clone(g)
    tl=[row[:sep_c] for row in g[:sep_r]]
    tr=[row[sep_c+1:] for row in g[:sep_r]]
    bl=[row[:sep_c] for row in g[sep_r+1:]]
    funcs=[lambda x:x, rot90, rot180, rot270, flip_h, flip_v]
    found=funcs[0]
    for f in funcs:
        if f(tl)==tr:
            found=f
            break
    br=found(bl)
    out=clone(g)
    for r in range(len(br)):
        for c in range(len(br[0])):
            out[sep_r+1+r][sep_c+1+c]=br[r][c]
    return out

def solve_H86(g):
    src=[v for v in g[0] if v!=0]
    tgt=[v for v in g[1] if v!=0]
    mapping={s:t for s,t in zip(src,tgt)}
    canvas=g[2:]
    out=[]
    for row in canvas:
        out.append([mapping.get(v,v) if v!=0 else 0 for v in row])
    return out

def solve_H87(g):
    h,w=dims(g)
    frame=[(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8]
    if not frame:
        return clone(g)
    r0,r1,c0,c1=bbox_cells(frame)
    seeds=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,8)]
    out=clone(g)
    seeds_sorted=sorted(seeds,key=lambda t:(t[0],t[1]))
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c]==0 and seeds_sorted:
                best=None
                bestkey=None
                for sr,sc,color in seeds_sorted:
                    key=(abs(sr-r)+abs(sc-c), sr, sc)
                    if bestkey is None or key<bestkey:
                        bestkey=key; best=color
                out[r][c]=best
    return out

def solve_H88(g):
    h,w=dims(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    hh,ww=dims(left)
    masked=blank(hh,ww,0)
    for r in range(hh):
        for c in range(ww):
            if left[r][c]!=0 and right[r][c]!=0:
                masked[r][c]=right[r][c]
    return crop_nonzero(masked)

def solve_H89(g):
    h,w=dims(g)
    groups=split_prototype_groups(g)
    protos={}
    for c0,c1,key in groups:
        proto=[row[c0:c1+1] for row in g[1:4]]
        protos[key]=proto
    query=[v for v in g[-1] if v!=0]
    if not query:
        return [[0]]
    out_h=3
    out_w=len(query)*3 + (len(query)-1)
    out=blank(out_h,out_w,0)
    x=0
    for i,key in enumerate(query):
        proto=protos[key]
        for r in range(3):
            for c in range(3):
                out[r][x+c]=proto[r][c]
        x+=4
    return out

def solve_H90(g):
    h,w=dims(g)
    wall={(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8}
    obj=[(r,c,v) for r in range(h) for c,v in enumerate(g[r]) if v not in (0,8)]
    out=blank(h,w,0)
    for r,c in wall:
        out[r][c]=8
    if not obj:
        return out
    t=0
    while True:
        ok=True
        for r,c,v in obj:
            nc=c+t+1
            if nc>=w or (r,nc) in wall:
                ok=False
                break
        if ok:
            t+=1
        else:
            break
    for shift in range(t+1):
        for r,c,v in obj:
            out[r][c+shift]=v
    return out

def solve_H91(g):
    h,w=dims(g)
    sep_r=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep_r=r; break
    sep_cs=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    if sep_r is None or len(sep_cs)<2:
        return clone(g)
    c1,c2=sep_cs[:2]
    A=[row[:c1] for row in g[:sep_r]]
    B=[row[c1+1:c2] for row in g[:sep_r]]
    C=[row[c2+1:] for row in g[:sep_r]]
    D=[row[:c1] for row in g[sep_r+1:]]
    E=[row[c1+1:c2] for row in g[sep_r+1:]]
    def make(op,x,y):
        h,w=dims(x)
        out=blank(h,w,0)
        for r in range(h):
            for c in range(w):
                xx=x[r][c]!=0; yy=y[r][c]!=0
                flag=op(xx,yy)
                if flag: out[r][c]=2
        return out
    ops=[
        ("union", lambda a,b: a or b),
        ("intersection", lambda a,b: a and b),
        ("xor", lambda a,b: (a and not b) or (b and not a))
    ]
    chosen=ops[0][1]
    for name,op in ops:
        if make(op,A,B)==C:
            chosen=op; break
    F=make(chosen,D,E)
    out=clone(g)
    for r in range(len(F)):
        for c in range(len(F[0])):
            out[sep_r+1+r][c2+1+c]=F[r][c]
    return out

SOLVERS = {
    'E85': solve_E85,
    'E86': solve_E86,
    'E87': solve_E87,
    'E88': solve_E88,
    'E89': solve_E89,
    'E90': solve_E90,
    'E91': solve_E91,
    'M85': solve_M85,
    'M86': solve_M86,
    'M87': solve_M87,
    'M88': solve_M88,
    'M89': solve_M89,
    'M90': solve_M90,
    'M91': solve_M91,
    'H85': solve_H85,
    'H86': solve_H86,
    'H87': solve_H87,
    'H88': solve_H88,
    'H89': solve_H89,
    'H90': solve_H90,
    'H91': solve_H91,
}
