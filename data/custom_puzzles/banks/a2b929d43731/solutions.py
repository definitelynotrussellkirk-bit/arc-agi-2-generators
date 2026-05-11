
"""
ARC-style puzzle bank continuation 12: 21 more puzzles (E78-E84, M78-M84, H78-H84).

This batch leans into local completion, support-relative translation, axis and
point symmetry, marker-conditioned transforms, sweep shadows, analogy panels,
prototype stamping, counted vector copies, compartment fills, and header-driven
dispatch.

Notable motifs:
- support_drop(shape, line): M78
- marker_dispatch_transform(marker, panel): M80
- counted_vector_copy(object, vector, k): H81
- header_dispatch(row_header, col_header, mask): H84
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import List, Tuple

Grid = List[List[int]]

def blank(h:int,w:int,v:int=0)->Grid:
    return [[v]*w for _ in range(h)]

def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0])

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def bbox(cells):
    pts=list(cells)
    rs=[r for r,c in pts]
    cs=[c for r,c in pts]
    return min(rs), max(rs), min(cs), max(cs)

def components(g:Grid, ignore=(0,)):
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
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny]==v:
                        seen.add((nx,ny))
                        q.append((nx,ny))
            out.append((v,cells))
    return out

def rot90(grid:Grid)->Grid:
    h,w=dims(grid)
    return [[grid[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(grid:Grid)->Grid:
    return [row[::-1] for row in grid[::-1]]

def rot270(grid:Grid)->Grid:
    return rot90(rot180(grid))

def flip_h(grid:Grid)->Grid:
    return [row[::-1] for row in grid]

def flip_v(grid:Grid)->Grid:
    return grid[::-1]

def apply_xor(a:Grid,b:Grid)->Grid:
    h,w=dims(a)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            aa=a[r][c]!=0
            bb=b[r][c]!=0
            if aa != bb:
                out[r][c]=2
    return out

def solve_E78(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][1]==cells[1][1]:
            c=cells[0][1]
            a,b=sorted([cells[0][0], cells[1][0]])
            if all(g[r][c]==0 for r in range(a+1,b)):
                for r in range(a,b+1):
                    out[r][c]=color
    return out

def solve_E79(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out

def solve_E80(g):
    out=blank(*dims(g),0)
    for v,cells in components(g):
        if len(cells)>=2:
            for r,c in cells:
                out[r][c]=v
    return out

def solve_E81(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        s=set(cells)
        for r,c in cells:
            for dr,dc in ((1,1),(1,-1)):
                if (r+dr,c+dc) in s:
                    rs=sorted([r,r+dr])
                    cs=sorted([c,c+dc])
                    if rs[1]-rs[0]==1 and cs[1]-cs[0]==1:
                        for rr in rs:
                            for cc in cs:
                                out[rr][cc]=color
    return out

def solve_E82(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            border=[]
            for rr in range(r-1,r+2):
                for cc in range(c-1,c+2):
                    if (rr,cc)!=(r,c):
                        border.append(g[rr][cc])
            if border[0]!=0 and all(v==border[0] for v in border):
                out[r][c]=border[0]
    return out

def solve_E83(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out

def solve_E84(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep=r
            break
    out=clone(g)
    if sep is None:
        return out
    for r in range(sep):
        rr=sep+1+(sep-1-r)
        if 0<=rr<h:
            for c in range(w):
                if out[rr][c]==0:
                    out[rr][c]=g[r][c]
    return out

def solve_M78(g):
    h,w=dims(g)
    out=blank(h,w,0)
    support_row=None
    for r in range(h):
        if any(v==9 for v in g[r]) and all(v in (0,9) for v in g[r]):
            support_row=r
            for c,v in enumerate(g[r]):
                if v==9:
                    out[r][c]=9
    cells=[]
    maxr=-10
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cells.append((r,c,v))
                maxr=max(maxr,r)
    if not cells or support_row is None:
        return clone(g)
    delta=(support_row-1)-maxr
    for r,c,v in cells:
        out[r+delta][c]=v
    return out

def solve_M79(g):
    h,w=dims(g)
    out=clone(g)
    axis=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            axis=c
            break
    if axis is None:
        return out
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cc=2*axis-c
                if 0<=cc<w:
                    out[r][cc]=v
    return out

def solve_M80(g):
    h,w=dims(g)
    marker=g[0][0]
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(1,h)):
            sep=c
            break
    if sep is None:
        return clone(g)
    src=[row[1:sep] for row in g[1:]]
    if marker==2:
        trans=flip_h(src)
    elif marker==3:
        trans=rot90(src)
    else:
        trans=src
    out=clone(g)
    th=len(g)-1
    tw=w-sep-1
    for r in range(th):
        for c in range(tw):
            out[r+1][sep+1+c]=trans[r][c]
    return out

def solve_M81(g):
    h,w=dims(g)
    out=clone(g)
    obj=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,7):
                obj.append((r,c,v))
    if not obj:
        return out
    maxc=max(c for r,c,v in obj)
    for shift in range(1,w-maxc):
        for r,c,v in obj:
            if c+shift<w:
                out[r][c+shift]=v
    return out

def solve_M82(g):
    key=g[0][0]
    target=None
    for v,cells in components(g, ignore=(0,)):
        if v==key and (0,0) not in cells:
            if target is None or len(cells)>len(target):
                target=cells
    if target is None:
        return [[key]]
    r0,r1,c0,c1=bbox(target)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def solve_M83(g):
    h,w=dims(g)
    out=clone(g)
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    if not anchors:
        return out
    ar,ac=anchors[0]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                rr,cc=2*ar-r,2*ac-c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out

def solve_M84(g):
    h,w=dims(g)
    out=clone(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c
            break
    if sep is None:
        return out
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    border_color=None
    for r in range(h):
        for v in right[r]:
            if v!=0:
                border_color=v
                break
        if border_color is not None:
            break
    for r in range(h):
        for c,v in enumerate(left[r]):
            if v!=0:
                out[r][sep+1+c]=border_color
    return out

def solve_H78(g):
    h,w=dims(g)
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[w]
    panels=[[row[s:e] for row in g] for s,e in zip(starts,ends)]
    _,_,C,D=panels
    trans=rot90(C)
    out=clone(g)
    s=starts[3]
    for r in range(h):
        for c in range(len(D[0])):
            out[r][s+c]=trans[r][c]
    return out

def solve_H79(g):
    h,w=dims(g)
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[w]
    panels=[[row[s:e] for row in g] for s,e in zip(starts,ends)]
    _,_,_,Q1,Q2,OUT=panels
    res=apply_xor(Q1,Q2)
    out=clone(g)
    s=starts[5]
    for r in range(h):
        for c in range(len(OUT[0])):
            out[r][s+c]=res[r][c]
    return out

def solve_H80(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep=r
            break
    top=g[:sep]
    ht,wt=dims(top)
    sepcols=[c for c in range(wt) if all(top[r][c]==9 for r in range(ht))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[wt]
    boxes=[[row[s:e] for row in top] for s,e in zip(starts,ends)]
    protos={}
    for box in boxes:
        key=box[1][1]
        cells=[(r-1,c-1) for r in range(3) for c in range(3) if box[r][c]!=0]
        protos[key]=cells
    out=clone(g)
    base=sep+1
    for r in range(base,h):
        for c,v in enumerate(g[r]):
            if v in protos:
                for dr,dc in protos[v]:
                    rr,cc=r+dr,c+dc
                    if base<=rr<h and 0<=cc<w:
                        out[rr][cc]=v
    return out

def solve_H81(g):
    h,w=dims(g)
    out=blank(h,w,0)
    p1=p2=None
    k=0
    obj=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==1:
                p1=(r,c)
                out[r][c]=1
            elif v==2:
                p2=(r,c)
                out[r][c]=2
            elif v==3:
                k+=1
                out[r][c]=3
            elif v!=0:
                obj.append((r,c,v))
    if not p1 or not p2:
        return clone(g)
    dr,dc=p2[0]-p1[0],p2[1]-p1[1]
    for mult in range(k+1):
        for r,c,v in obj:
            rr,cc=r+mult*dr,c+mult*dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out

def solve_H82(g):
    h,w=dims(g)
    seprows=[r for r in range(h) if all(v==9 for v in g[r])]
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    csep=sepcols[0]
    r1,r2=seprows
    topL=[row[:csep] for row in g[:r1]]
    topR=[row[csep+1:] for row in g[:r1]]
    midL=[row[:csep] for row in g[r1+1:r2]]
    midR=[row[csep+1:] for row in g[r1+1:r2]]
    botL=[row[:csep] for row in g[r2+1:]]
    botR=[row[csep+1:] for row in g[r2+1:]]

    def identity(x): return clone(x)
    candidates=[identity,rot90,rot180,rot270,flip_h,flip_v]
    geom=identity
    for fn in candidates:
        if fn(topL)==topR:
            geom=fn
            break

    cmap={}
    mh,mw=dims(midL)
    for r in range(mh):
        for c in range(mw):
            a,b=midL[r][c],midR[r][c]
            if a!=0:
                cmap[a]=b

    tmp=geom(botL)
    res=[[cmap.get(v,v) if v!=0 else 0 for v in row] for row in tmp]

    out=clone(g)
    brs=r2+1
    for r in range(len(botR)):
        for c in range(len(botR[0])):
            out[brs+r][csep+1+c]=res[r][c]
    return out

def solve_H83(g):
    h,w=dims(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if r in (0,h-1) or c in (0,w-1):
                v=g[r][c]
                if v not in (0,5):
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=r+dr,c+dc
                        if 0<=nr<h and 0<=nc<w and g[nr][nc]==0 and (nr,nc) not in seen:
                            q=deque([(nr,nc)])
                            seen.add((nr,nc))
                            cells=[]
                            while q:
                                x,y=q.popleft()
                                cells.append((x,y))
                                for ddx,ddy in ((1,0),(-1,0),(0,1),(0,-1)):
                                    xx,yy=x+ddx,y+ddy
                                    if 0<=xx<h and 0<=yy<w and g[xx][yy]==0 and (xx,yy) not in seen:
                                        seen.add((xx,yy))
                                        q.append((xx,yy))
                            for x,y in cells:
                                out[x][y]=v
    return out

def solve_H84(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for c in range(w):
        out[0][c]=g[0][c]
    for r in range(h):
        out[r][0]=g[r][0]
    for r in range(1,h):
        for c in range(1,w):
            v=g[r][c]
            if v==1:
                out[r][c]=g[r][0]
            elif v==2:
                out[r][c]=g[0][c]
    return out
