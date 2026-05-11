"""
ARC-style puzzle bank continuation 14: 21 more puzzles (E92-E98, M92-M98, H92-H98).

This batch leans into column-wise metadata, object relocation, panel transforms,
prototype dictionaries, chamber fills, edit-delta transfer, and rank-based
recolor/packing.

Notable motifs:
- panel_transform_from_example(example_src, example_dst, query): H92
- orbit_union(anchor, shape): H94
- edit_delta_transfer(src, dst, query): H96
- rank_recolor_pack(objects, palette): H98
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(grid):
    return len(grid), len(grid[0])

def clone(grid):
    return [row[:] for row in grid]

def bbox_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def crop_bbox(grid, cells):
    r0,r1,c0,c1=bbox_cells(cells)
    return [row[c0:c1+1] for row in grid[r0:r1+1]]

def comps(grid, ignore=(0,)):
    h,w=dims(grid)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v in ignore or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and grid[nx][ny]==v:
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((v,cells))
    return out

def comps_any(grid, ignore=(0,)):
    h,w=dims(grid)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if grid[r][c] in ignore or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and grid[nx][ny] not in ignore:
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append(cells)
    return out

def paste(out,obj,r0,c0):
    H,W=dims(out); h,w=dims(obj)
    for r in range(h):
        for c in range(w):
            if obj[r][c]!=0 and 0<=r0+r<H and 0<=c0+c<W:
                out[r0+r][c0+c]=obj[r][c]
    return out

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

def split_proto_dictionary(grid):
    # row0 contains keys at centers of width-3 prototypes separated by one zero column
    row0=grid[0]
    cols=[c for c,v in enumerate(row0) if v!=0]
    groups=[]
    for c in cols:
        groups.append((row0[c], c-1, c+1))
    return groups

def rotate_point(dr,dc,k):
    if k==0: return dr,dc
    if k==1: return -dc,dr
    if k==2: return -dr,-dc
    if k==3: return dc,-dr

def solve_E92(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][1]==cells[1][1]:
            c=cells[0][1]
            a,b=sorted([cells[0][0],cells[1][0]])
            if all(grid[r][c]==0 for r in range(a+1,b)):
                for r in range(a,b+1):
                    out[r][c]=color
    return out

def solve_E93(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            vals=[grid[r][c],grid[r][c+2],grid[r+2][c],grid[r+2][c+2]]
            if vals[0]!=0 and len(set(vals))==1:
                color=vals[0]
                # interior of corners may be zeros
                # fill border if non-corners are zeros currently
                border=[(r,c),(r,c+1),(r,c+2),(r+1,c),(r+1,c+2),(r+2,c),(r+2,c+1),(r+2,c+2)]
                inner_ok = grid[r+1][c+1]==0
                side_ok = all(grid[x][y] in (0,color) for x,y in border)
                if inner_ok and side_ok:
                    for x,y in border:
                        out[x][y]=color
    return out

def solve_E94(grid):
    out=clone(grid)
    h,w=dims(grid)
    # horizontal 0cc or cc0
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a==0 and b!=0 and b==d:
                out[r][c]=b
            if a!=0 and a==b and d==0:
                out[r][c+2]=a
    # vertical
    for r in range(h-2):
        for c in range(w):
            a,b,d=grid[r][c],grid[r+1][c],grid[r+2][c]
            if a==0 and b!=0 and b==d:
                out[r][c]=b
            if a!=0 and a==b and d==0:
                out[r+2][c]=a
    return out

def solve_E95(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c]!=0:
                continue
            vals=[grid[r-1][c-1],grid[r-1][c+1],grid[r+1][c-1],grid[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out

def solve_E96(grid):
    out=clone(grid)
    h,w=dims(grid)
    header=grid[0]
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1 and header[c]!=0:
                out[r][c]=header[c]
    return out

def solve_E97(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        vals=[v for v in grid[r] if v!=0]
        out[r][:len(vals)] = vals
    return out

def solve_E98(grid):
    out=clone(grid)
    by=defaultdict(list)
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    for c in range(min(c1,c2), max(c1,c2)+1):
                        out[r][c]=color
    return out

def solve_H92(grid):
    h,w=dims(grid)
    # find sep row and col of all 9
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_c=next((c for c in range(w) if all(grid[r][c]==9 for r in range(h))), None)
    if sep_r is None or sep_c is None:
        return clone(grid)
    A=[row[:sep_c] for row in grid[:sep_r]]
    B=[row[sep_c+1:] for row in grid[:sep_r]]
    C=[row[:sep_c] for row in grid[sep_r+1:]]
    trans=[rot90, rot180, rot270, flip_h, flip_v]
    fn=None
    for t in trans:
        if t(A)==B:
            fn=t; break
    if fn is None:
        return clone(grid)
    D=fn(C)
    out=clone(grid)
    for r in range(len(D)):
        for c in range(len(D[0])):
            out[sep_r+1+r][sep_c+1+c]=D[r][c]
    return out

def solve_H93(grid):
    h,w=dims(grid)
    # query is last row
    query=[v for v in grid[-1] if v!=0]
    groups=split_proto_dictionary(grid[:-1])  # but row0 still same if passing whole grid? not used
    # Actually use original grid row0 and rows1:4 as prototypes
    proto={}
    for key,c0,c1 in split_proto_dictionary(grid):
        proto[key]=[row[c0:c1+1] for row in grid[1:4]]
    pieces=[proto[k] for k in query if k in proto]
    if not pieces:
        return [[0]]
    H=3
    W=sum(3 for _ in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur+=4
    return out

def solve_H94(grid):
    h,w=dims(grid)
    anchor=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    if len(anchor)!=1:
        return clone(grid)
    ar,ac=anchor[0]
    out=blank(h,w,0)
    out[ar][ac]=9
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,9)]
    for k in range(4):
        for r,c,v in obj:
            dr,dc=r-ar,c-ac
            rr,cc=rotate_point(dr,dc,k)
            nr,nc=ar+rr,ac+cc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

def solve_H95(grid):
    h,w=dims(grid)
    out=clone(grid)
    # components of cells not wall 9
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,9):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=9 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if not seeds:
                continue
            for x,y in cells:
                if grid[x][y]==0:
                    best=min(seeds, key=lambda s:(abs(s[0]-x)+abs(s[1]-y), s[2], s[0], s[1]))
                    out[x][y]=best[2]
    return out

def solve_H96(grid):
    h,w=dims(grid)
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_c=next((c for c in range(w) if all(grid[r][c]==9 for r in range(h))), None)
    if sep_r is None or sep_c is None:
        return clone(grid)
    A=[row[:sep_c] for row in grid[:sep_r]]
    B=[row[sep_c+1:] for row in grid[:sep_r]]
    C=[row[:sep_c] for row in grid[sep_r+1:]]
    # derive delta additions in bbox coordinates
    def bbox_nonzero(g):
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
        if not cells:
            return None
        return bbox_cells(cells)
    ba=bbox_nonzero(A); bb=bbox_nonzero(B); bc=bbox_nonzero(C)
    if ba is None or bb is None or bc is None:
        return clone(grid)
    ar0,ar1,ac0,ac1=ba
    br0,br1,bc0,bc1=bb
    cr0,cr1,cc0,cc1=bc
    # assume same bbox size example
    adds=[]
    for r in range(max(ar1-ar0+1, br1-br0+1)):
        for c in range(max(ac1-ac0+1, bc1-bc0+1)):
            av=A[ar0+r][ac0+c] if ar0+r<=ar1 and ac0+c<=ac1 else 0
            bv=B[br0+r][bc0+c] if br0+r<=br1 and bc0+c<=bc1 else 0
            if av==0 and bv!=0:
                adds.append((r,c,bv))
    out=clone(grid)
    # start with C copied to D
    for r in range(len(C)):
        for c in range(len(C[0])):
            out[sep_r+1+r][sep_c+1+c]=C[r][c]
    # dominant color in C
    qcolors=[v for row in C for v in row if v!=0]
    qcolor=max(set(qcolors), key=qcolors.count)
    for r,c,v in adds:
        nr,nc=cr0+r,cc0+c
        if 0<=nr<len(C) and 0<=nc<len(C[0]):
            out[sep_r+1+nr][sep_c+1+nc]=qcolor if v!=0 else 0
    return out

def solve_H97(grid):
    h,w=dims(grid)
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_cs=[c for c in range(w) if all(grid[r][c]==9 for r in range(h))]
    if sep_r is None or len(sep_cs)<2:
        return clone(grid)
    c1,c2=sep_cs[:2]
    A=[row[:c1] for row in grid[:sep_r]]
    B=[row[c1+1:c2] for row in grid[:sep_r]]
    C=[row[c2+1:] for row in grid[:sep_r]]
    D=[row[:c1] for row in grid[sep_r+1:]]
    E=[row[c1+1:c2] for row in grid[sep_r+1:]]
    def op_apply(name,X,Y):
        h,w=dims(X); out=blank(h,w,0)
        for r in range(h):
            for c in range(w):
                x=X[r][c]!=0; y=Y[r][c]!=0
                if name=="union" and (x or y):
                    out[r][c]=2
                elif name=="intersection" and (x and y):
                    out[r][c]=2
                elif name=="xor" and (x ^ y):
                    out[r][c]=2
                elif name=="AminusB" and (x and not y):
                    out[r][c]=2
                elif name=="BminusA" and (y and not x):
                    out[r][c]=2
        return out
    choices=["union","intersection","xor","AminusB","BminusA"]
    chosen="union"
    for name in choices:
        if op_apply(name,A,B)==C:
            chosen=name; break
    F=op_apply(chosen,D,E)
    out=clone(grid)
    for r in range(len(F)):
        for c in range(len(F[0])):
            out[sep_r+1+r][c2+1+c]=F[r][c]
    return out

def solve_H98(grid):
    palette=[v for v in grid[0] if v!=0]
    body=grid[1:]
    parts=[]
    for cells in comps_any(body, ignore=(0,)):
        comp_grid=crop_bbox(body,cells)
        parts.append((len(cells), comp_grid))
    parts.sort(key=lambda x:x[0])
    pieces=[]
    for i,(size,p) in enumerate(parts):
        color=palette[i]
        q=clone(p)
        for r in range(len(q)):
            for c in range(len(q[0])):
                if q[r][c]!=0:
                    q[r][c]=color
        pieces.append(q)
    if not pieces:
        return [[0]]
    H=max(len(p) for p in pieces)
    W=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur += len(p[0])+1
    return out

def solve_M92(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    anchors=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==8]
    if len(anchors)!=1:
        return clone(grid)
    ar,ac=anchors[0]
    obj_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c] not in (0,8)]
    if not obj_cells:
        return clone(grid)
    r0,r1,c0,c1=bbox_cells(obj_cells)
    obj=[row[c0:c1+1] for row in grid[r0:r1+1]]
    paste(out,obj,ar,ac)
    return out

def solve_M93(grid):
    out=clone(grid)
    h,w=dims(grid)
    # detect single-color rectangular frame components
    for color,cells in comps(grid, ignore=(0,)):
        r0,r1,c0,c1=bbox_cells(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            inner_colors={grid[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if grid[r][c] not in (0,color)}
            if len(inner_colors)==1:
                fill=next(iter(inner_colors))
                for r in range(r0+1,r1):
                    for c in range(c0+1,c1):
                        out[r][c]=fill
    return out

def solve_M94(grid):
    comps_list=comps_any(grid, ignore=(0,))
    if not comps_list:
        return [[0]]
    cells=max(comps_list, key=len)
    return crop_bbox(grid, cells)

def solve_M95(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    markers=sorted([(r,c) for r in range(h) for c in range(w) if grid[r][c]==8])
    if len(markers)!=2:
        return clone(grid)
    (r1,c1),(r2,c2)=markers
    dr,dc=r2-r1,c2-c1
    obj_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c] not in (0,8)]
    for r,c in obj_cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=grid[r][c]
    return out

def solve_M96(grid):
    out=clone(grid)
    h,w=dims(grid)
    div=None
    for c in range(w):
        if all(grid[r][c]==9 for r in range(h)):
            div=c
            break
    if div is None:
        return clone(grid)
    for r in range(h):
        for c in range(div):
            v=grid[r][c]
            if v not in (0,9):
                mc=div + (div-c)
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def solve_M97(grid):
    h,w=dims(grid)
    target=grid[0][0]
    # ignore guide cell itself
    grid2=clone(grid)
    grid2[0][0]=0
    for color,cells in comps(grid2, ignore=(0,)):
        if color==target:
            return crop_bbox(grid2, cells)
    return [[0]]

def solve_M98(grid):
    header=[v for v in grid[0] if v!=0]
    # find one object per header color
    objs={}
    body=grid[1:]
    for color,cells in comps(body, ignore=(0,)):
        if color in header:
            objs[color]=crop_bbox(body, cells)
    pieces=[objs[c] for c in header if c in objs]
    if not pieces:
        return [[0]]
    H=max(len(p) for p in pieces)
    W=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur += len(p[0])+1
    return out

SOLVERS = {
    'E92': solve_E92,
    'E93': solve_E93,
    'E94': solve_E94,
    'E95': solve_E95,
    'E96': solve_E96,
    'E97': solve_E97,
    'E98': solve_E98,
    'H92': solve_H92,
    'H93': solve_H93,
    'H94': solve_H94,
    'H95': solve_H95,
    'H96': solve_H96,
    'H97': solve_H97,
    'H98': solve_H98,
    'M92': solve_M92,
    'M93': solve_M93,
    'M94': solve_M94,
    'M95': solve_M95,
    'M96': solve_M96,
    'M97': solve_M97,
    'M98': solve_M98,
}