
"""
ARC-style puzzle bank continuation 7: 21 more puzzles (E43-E49, M43-M49, H43-H49).
This batch leans into row/column metadata, local object transforms, analogy panels,
ray casting, and distance-based fills. Two notable reusable motifs here are
ray_emit_until (used in E48 and H46) and nearest_seed_fill (used in H49).
"""
from __future__ import annotations
from typing import List
from collections import deque

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def clone(g):
    return [row[:] for row in g]

def same_color_components(g):
    h,w=dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0 or (r,c) in seen:
                continue
            q=deque([(r,c)])
            seen.add((r,c))
            cells=[]
            while q:
                x,y=q.popleft()
                cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]==col and (nx,ny) not in seen:
                        seen.add((nx,ny))
                        q.append((nx,ny))
            comps.append((col,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def normalize(cells):
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1), (r0,c0)

def split_h_panels(g, pw, sep=9):
    h,w=dims(g)
    panels=[]
    c=0
    while c<w:
        panels.append([row[c:c+pw] for row in g])
        c += pw
        if c < w:
            c += 1
    return panels

def join_h_panels(panels, sep=9):
    h=len(panels[0])
    pw=len(panels[0][0])
    n=len(panels)
    g=blank(h, n*pw + (n-1), 0)
    c=0
    for i,p in enumerate(panels):
        for r in range(h):
            for j in range(pw):
                g[r][c+j]=p[r][j]
        c += pw
        if i < n-1:
            for r in range(h):
                g[r][c]=sep
            c += 1
    return g

def rotate_panel_cw(p):
    return [list(row) for row in zip(*p[::-1])]

def solve_E43(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r][c+2] and g[r][c+1]==0:
                out[r][c+1]=g[r][c]
    return out

def solve_E44(g: Grid) -> Grid:
    n=len(g)
    out=blank(n,n)
    for r in range(n):
        for c in range(n):
            out[n-1-c][n-1-r]=g[r][c]
    return out

def solve_E45(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        key=g[r][0]
        for c in range(1,w):
            if g[r][c]==8 and key!=0:
                out[r][c]=key
    return out

def solve_E46(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        vals=[x for x in g[r] if x!=0]
        out[r][w-len(vals):]=vals
    return out

def solve_E47(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            cells=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[x for x in cells if x!=0]
            if len(nz)==3 and len(set(nz))==1:
                v=nz[0]
                if g[r][c]==0: out[r][c]=v
                if g[r][c+1]==0: out[r][c+1]=v
                if g[r+1][c]==0: out[r+1][c]=v
                if g[r+1][c+1]==0: out[r+1][c+1]=v
    return out

def solve_E48(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        c=0
        while c < w-1:
            if g[r][c]==1 and g[r][c+1] not in (0,1,9):
                col=g[r][c+1]
                k=c+1
                while k < w and g[r][k] != 9:
                    if g[r][k] in (0,col):
                        out[r][k]=col
                    k += 1
                c=k
            else:
                c += 1
    return out

def solve_E49(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    half=w//2
    for r in range(h):
        for c in range(half):
            if g[r][c]!=0:
                out[r][w-1-c]=g[r][c]
    return out

def solve_M43(g: Grid) -> Grid:
    h,w=dims(g)
    k=sum(1 for x in g[0] if x==1)
    out=blank(h,w)
    body=[row[:] for row in g[1:]]
    for col,cells in same_color_components(body):
        if len(cells)==k:
            for r,c in cells:
                out[r+1][c]=col
    return out

def solve_M44(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for col,cells in same_color_components(g):
        shape,(hh,ww),(r0,c0)=normalize(cells)
        tshape={(c,hh-1-r) for r,c in shape}
        for dr,dc in tshape:
            out[r0+dr][c0+dc]=col
    return out

def solve_M45(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for col,cells in same_color_components(g):
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=col
    return out

def solve_M46(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    p1=p2=None
    cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                p1=(r,c)
            elif g[r][c]==2:
                p2=(r,c)
            elif g[r][c]==3:
                cells.append((r,c))
    dr,dc=p2[0]-p1[0], p2[1]-p1[1]
    for r,c in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=3
    return out

def solve_M47(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    mapping={}
    for c in range(w):
        if g[0][c]!=0:
            mapping[g[0][c]]=g[1][c]
    for r in range(2,h):
        for c in range(w):
            if g[r][c] in mapping:
                out[r][c]=mapping[g[r][c]]
    return out

def solve_M48(g: Grid) -> Grid:
    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    (r1,c1),(r2,c2)=pts
    r0,r3=sorted([r1,r2])
    c0,c3=sorted([c1,c2])
    return [row[c0:c3+1] for row in g[r0:r3+1]]

def solve_M49(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    ar,ac=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9][0]
    out[ar][ac]=9
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                nr,nc=2*ar-r,2*ac-c
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out

def solve_H43(g: Grid) -> Grid:
    left,mid,right=split_h_panels(g,5)
    out_right=blank(5,5)
    for r in range(5):
        for c in range(5):
            a,b=left[r][c], mid[r][c]
            if a!=0 and b!=0:
                out_right[r][c]=8
            elif a!=0:
                out_right[r][c]=a
            elif b!=0:
                out_right[r][c]=b
    return join_h_panels([left,mid,out_right])

def solve_H44(g: Grid) -> Grid:
    out=clone(g)
    bl=[row[:5] for row in g[6:11]]
    br=rotate_panel_cw(bl)
    for r in range(5):
        for c in range(5):
            out[6+r][6+c]=br[r][c]
    return out

def solve_H45(g: Grid) -> Grid:
    h,w=dims(g)
    proto2=[row[0:3] for row in g[0:3]]
    proto3=[row[4:7] for row in g[0:3]]
    out=blank(h,w)
    for r in range(4):
        for c in range(w):
            out[r][c]=g[r][c]
    for r in range(4,h):
        for c in range(w):
            if g[r][c]==2:
                for dr in range(3):
                    for dc in range(3):
                        if r+dr<h and c+dc<w and proto2[dr][dc]==2:
                            out[r+dr][c+dc]=2
            elif g[r][c]==3:
                for dr in range(3):
                    for dc in range(3):
                        if r+dr<h and c+dc<w and proto3[dr][dc]==3:
                            out[r+dr][c+dc]=3
    return out

def solve_H46(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    horiz=set()
    vert=set()
    for r in range(h):
        if g[r][0]==2:
            c=1
            while c < w and g[r][c] != 9:
                horiz.add((r,c))
                c += 1
    for c in range(w):
        if g[0][c]==3:
            r=1
            while r < h and g[r][c] != 9:
                vert.add((r,c))
                r += 1
    for r,c in horiz | vert:
        if g[r][c]==9:
            continue
        if (r,c) in horiz and (r,c) in vert:
            out[r][c]=8
        elif (r,c) in horiz:
            out[r][c]=2
        elif (r,c) in vert:
            out[r][c]=3
    return out

def solve_H47(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    p1=p2=None
    cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                p1=(r,c)
            elif g[r][c]==2:
                p2=(r,c)
            elif g[r][c]==4:
                cells.append((r,c))
    dr,dc=p2[0]-p1[0], p2[1]-p1[1]
    moved=[(r+dr,c+dc) for r,c in cells if 0<=r+dr<h and 0<=c+dc<w]
    if not moved:
        return out
    rs=[r for r,c in moved]
    cs=[c for r,c in moved]
    for r in range(min(rs), max(rs)+1):
        for c in range(min(cs), max(cs)+1):
            out[r][c]=4
    return out

def solve_H48(g: Grid) -> Grid:
    p1,p2,p3,p4=split_h_panels(g,5)
    outp=blank(5,5)
    for r in range(5):
        for c in range(5):
            cnt=sum(1 for p in [p1,p2,p3] if p[r][c]!=0)
            if cnt >= 2:
                outp[r][c]=8
    return join_h_panels([p1,p2,p3,outp])

def solve_H49(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    for r in range(h):
        for c in range(w):
            best=None
            colors=[]
            for sr,sc,v in seeds:
                d=abs(sr-r)+abs(sc-c)
                if best is None or d < best:
                    best=d
                    colors=[v]
                elif d == best:
                    colors.append(v)
            out[r][c]=colors[0] if len(set(colors))==1 else 0
    return out
