"""Reference helper library and 21 reference solve functions for the tenth custom ARC puzzle bank.

New primitive introduced in this set:
  trace_beam(grid, start, direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'})
Trace a ray through passable cells; slash and backslash mirror cells turn the direction, and the beam stops at walls or the grid boundary.
"""
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

Grid = List[List[int]]
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]
dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def copyg(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    h,w=dims(g)
    return 0 <= r < h and 0 <= c < w

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def norm_cells(cells):
    r1,c1,r2,c2=bbox(cells)
    return sorted((r-r1,c-c1) for r,c in cells)

def rotate_pts(pts, k=1):
    pts=list(pts)
    for _ in range(k%4):
        maxr=max(r for r,c in pts)
        pts=[(c, maxr-r) for r,c in pts]
        rmin=min(r for r,c in pts)
        cmin=min(c for r,c in pts)
        pts=[(r-rmin,c-cmin) for r,c in pts]
    return sorted(pts)

def mirror_h_pts(pts):
    pts=list(pts)
    maxc=max(c for r,c in pts)
    return sorted((r, maxc-c) for r,c in pts)

def mirror_v_pts(pts):
    pts=list(pts)
    maxr=max(r for r,c in pts)
    return sorted((maxr-r, c) for r,c in pts)

def rect_frame_cells(r1,c1,r2,c2):
    cells=[]
    for c in range(c1,c2+1):
        cells.append((r1,c)); cells.append((r2,c))
    for r in range(r1+1,r2):
        cells.append((r,c1)); cells.append((r,c2))
    return sorted(set(cells))

def components(grid, colors=None, connectivity=4, include_zero=False, ignore=None):
    if ignore is None:
        ignore=set()
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs=dirs4 if connectivity==4 else dirs8
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or (r,c) in ignore:
                continue
            seen[r][c]=True
            v=grid[r][c]
            if v==0 and not include_zero:
                continue
            if colors is not None and v not in colors:
                continue
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and (nr,nc) not in ignore and grid[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            out.append({"color": v, "cells": sorted(cells)})
    return out

mirror_turn = {
    '/': {(0,1):(-1,0),(0,-1):(1,0),(-1,0):(0,1),(1,0):(0,-1)},
    '\\': {(0,1):(1,0),(0,-1):(-1,0),(-1,0):(0,-1),(1,0):(0,1)},
}
def trace_beam(grid, start, direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'}, include_start=False, max_steps=None):
    if max_steps is None:
        h,w=dims(grid)
        max_steps=h*w*8
    r,c=start
    dr,dc=direction
    path=[]
    if include_start:
        path.append((r,c))
    steps=0
    while steps < max_steps:
        nr,nc=r+dr,c+dc
        if not inb(grid,nr,nc):
            break
        v=grid[nr][nc]
        if v in walls:
            break
        if v not in passable and v not in mirrors:
            break
        path.append((nr,nc))
        if v in mirrors:
            dr,dc = mirror_turn[mirrors[v]][(dr,dc)]
        r,c=nr,nc
        steps += 1
    return path

def solve_S10_E1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}):
                    if out[rr][cc]==0:
                        out[rr][cc]=7
    return out

def solve_S10_E2(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        pos=defaultdict(list)
        for c,v in enumerate(grid[r]):
            if v!=0:
                pos[v].append(c)
        for v, cols in pos.items():
            if len(cols)==2:
                c1,c2=cols
                if all(grid[r][c]==0 for c in range(c1+1,c2)):
                    for c in range(c1,c2+1):
                        out[r][c]=v
    return out

def solve_S10_E3(grid):
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    r1,c1,r2,c2=bbox(cells)
    return [row[c1:c2+1] for row in grid[r1:r2+1]]

def solve_S10_E4(grid):
    h,w=dims(grid)
    anchor=next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1)
    obj_cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,1)]
    color=next(v for row in grid for v in row if v not in (0,1))
    r1,c1,r2,c2=bbox(obj_cells)
    dr,dc=anchor[0]-r1, anchor[1]-c1
    out=blank(h,w,0)
    for r,c in obj_cells:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=color
    return out

def solve_S10_E5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        if not any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out

def solve_S10_E6(grid):
    out=copyg(grid)
    pos=defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for v, cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2 and abs(c1-c2)%2==0:
                out[r1][(c1+c2)//2]=8
            elif c1==c2 and abs(r1-r2)%2==0:
                out[(r1+r2)//2][c1]=8
    return out

def solve_S10_E7(grid):
    h,w=dims(grid)
    counts=Counter(v for row in grid for v in row if v!=0)
    color=max(sorted(counts), key=lambda v: counts[v])
    n=counts[color]
    out=blank(h,w,0)
    for c in range(min(n,w)):
        out[h-1][c]=color
    return out

def solve_S10_M1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out

def solve_S10_M2(grid):
    out=copyg(grid)
    for comp in components(grid, colors={5}):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        frame=set(rect_frame_cells(r1,c1,r2,c2))
        if set(cells)!=frame:
            continue
        seeds=[grid[r][c] for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,5)]
        if len(set(seeds))!=1:
            continue
        fill=seeds[0]
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if out[r][c]==0:
                    out[r][c]=fill
    return out

def solve_S10_M3(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        old=grid[0][c]
        new=grid[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    out=copyg(grid)
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out

def solve_S10_M4(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    out=blank(h,w,0)
    body=[row[:] for row in grid[1:]]
    comps=components(body, colors={3})
    for comp in comps:
        if len(comp['cells'])==target:
            for r,c in comp['cells']:
                out[r+1][c]=8
            break
    return out

def solve_S10_M5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        vals=[grid[r][c] for r in range(h) if grid[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out

def solve_S10_M6(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==0 or v==5:
                continue
            rr=r+1
            while rr<h and grid[rr][c]==0:
                out[rr][c]=v
                rr+=1
    return out

def solve_S10_M7(grid):
    h,w=dims(grid)
    div=next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    left=[row[:div] for row in grid]
    right=[row[div+1:] for row in grid]
    oh,ow=len(left), len(left[0])
    out=blank(oh,ow,0)
    for r in range(oh):
        for c in range(ow):
            if left[r][c]!=right[r][c]:
                out[r][c]=8
    return out

def solve_S10_H1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out

def solve_S10_H2(grid):
    h,w=dims(grid)
    tmpl=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    base=norm_cells(tmpl)
    code_to_rot={2:0,4:1,6:2,9:3}
    out=blank(h,w,0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==1 and c-1>=0 and grid[r][c-1] in code_to_rot:
                rot=code_to_rot[grid[r][c-1]]
                pts=rotate_pts(base, rot)
                for dr,dc in pts:
                    rr,cc=r+dr,c+dc
                    if inb(out,rr,cc):
                        out[rr][cc]=8
    return out

def solve_S10_H3(grid):
    comps=components(grid)
    sig_to_comps=defaultdict(list)
    for comp in comps:
        sig=tuple(norm_cells(comp['cells']))
        sig_to_comps[sig].append(comp)
    out=blank(len(grid), len(grid[0]), 0)
    target=None
    for sig, comps2 in sig_to_comps.items():
        if len(comps2)==1:
            target=comps2[0]
            break
    if target is not None:
        for r,c in target['cells']:
            out[r][c]=8
    return out

def solve_S10_H4(grid):
    h,w=dims(grid)
    divs=[c for c in range(w) if all(grid[r][c]==5 for r in range(h))]
    d1,d2=divs[0],divs[1]
    p1=[row[:d1] for row in grid]
    p2=[row[d1+1:d2] for row in grid]
    p3=[row[d2+1:] for row in grid]
    ph,pw=len(p1), len(p1[0])
    out=blank(ph,pw,0)
    for r in range(ph):
        for c in range(pw):
            vals=[p1[r][c], p2[r][c], p3[r][c]]
            non=[v for v in vals if v!=0]
            counts=Counter(non)
            if counts:
                v,n=max(counts.items(), key=lambda kv: kv[1])
                if n>=2:
                    out[r][c]=v
    return out

def solve_S10_H5(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        old=grid[0][c]
        new=grid[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    out=copyg(grid)
    body=[row[:] for row in grid[2:]]
    for comp in components(body, colors={5}):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        frame=set(rect_frame_cells(r1,c1,r2,c2))
        if set(cells)!=frame:
            continue
        seeds=[body[r][c] for r in range(r1+1,r2) for c in range(c1+1,c2) if body[r][c] not in (0,5)]
        if len(set(seeds))!=1:
            continue
        seed=seeds[0]
        fill=mapping[seed]
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                out[r+2][c]=fill
    return out

def solve_S10_H6(grid):
    h,w=dims(grid)
    divr=next(r for r in range(h) if all(grid[r][c]==5 for c in range(w)))
    divc=next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    qh,qw=divr,divc
    quads={
        'TL': (0,0),
        'TR': (0,divc+1),
        'BL': (divr+1,0),
        'BR': (divr+1,divc+1),
    }
    canon=None
    color=None
    for name,(r0,c0) in quads.items():
        cells=[(r-r0,c-c0) for r in range(r0,r0+qh) for c in range(c0,c0+qw) if grid[r][c] not in (0,5)]
        if not cells:
            continue
        color=grid[r0+cells[0][0]][c0+cells[0][1]]
        pts=norm_cells(cells)
        if name=='TR':
            pts=mirror_h_pts(pts)
        elif name=='BL':
            pts=mirror_v_pts(pts)
        elif name=='BR':
            pts=mirror_v_pts(mirror_h_pts(pts))
        canon=pts
        break
    out=copyg(grid)
    for name,(r0,c0) in quads.items():
        existing=[(r,c) for r in range(r0,r0+qh) for c in range(c0,c0+qw) if grid[r][c] not in (0,5)]
        if existing:
            continue
        pts=canon
        if name=='TR':
            pts=mirror_h_pts(canon)
        elif name=='BL':
            pts=mirror_v_pts(canon)
        elif name=='BR':
            pts=mirror_v_pts(mirror_h_pts(canon))
        for dr,dc in pts:
            out[r0+dr][c0+dc]=color
    return out

def solve_S10_H7(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    anchor=next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2)
    comps=components([row[:] for row in grid[1:]], colors={3})
    chosen=None
    for comp in comps:
        if len(comp['cells'])==target:
            chosen=comp['cells']
            break
    out=blank(h,w,0)
    if chosen is None:
        return out
    abs_cells=[(r+1,c) for r,c in chosen]
    r1,c1,r2,c2=bbox(abs_cells)
    dr,dc=anchor[0]-r1, anchor[1]-c1
    for r,c in abs_cells:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out
