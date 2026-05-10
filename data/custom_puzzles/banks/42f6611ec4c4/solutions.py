"""
ARC-style puzzle bank continuation 4: 21 more puzzles (E22-E28, M22-M28, H22-H28).
Each solve_* function is a reference program for one puzzle.
"""
from __future__ import annotations
from typing import List
from collections import deque, defaultdict

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

def crop_cells(cells):
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1)

def components(g):
    h,w=dims(g); seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]==col and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col,cells))
    return comps

def normalize_shape(cells):
    s,(h,w)=crop_cells(cells)
    return s,h,w

def hole_cells_of_component(g, cells):
    r0,r1,c0,c1=bbox(cells)
    comp=set(cells)
    seen=set()
    q=deque()
    for r in range(r0,r1+1):
        for c in [c0,c1]:
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    for c in range(c0,c1+1):
        for r in [r0,r1]:
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    while q:
        x,y=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp and (nx,ny) not in seen:
                seen.add((nx,ny)); q.append((nx,ny))
    holes=[]; vis=set()
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if (r,c) not in comp and (r,c) not in seen and (r,c) not in vis:
                q=deque([(r,c)]); vis.add((r,c)); region=[]
                while q:
                    x,y=q.popleft(); region.append((x,y))
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp and (nx,ny) not in seen and (nx,ny) not in vis:
                            vis.add((nx,ny)); q.append((nx,ny))
                holes.append(region)
    return holes

def horizontal_runs(g):
    h,w=dims(g); runs=[]
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            v=g[r][c]; s=c
            while c+1<w and g[r][c+1]==v:
                c+=1
            e=c
            runs.append((r,s,e,v))
            c+=1
    return runs

def vertical_runs(g):
    h,w=dims(g); runs=[]
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==0:
                r+=1; continue
            v=g[r][c]; s=r
            while r+1<h and g[r+1][c]==v:
                r+=1
            e=r
            runs.append((c,s,e,v))
            r+=1
    return runs

def border_count(cells, h, w):
    s=set()
    for r,c in cells:
        if r==0: s.add('top')
        if r==h-1: s.add('bottom')
        if c==0: s.add('left')
        if c==w-1: s.add('right')
    return len(s)

def is_rect_frame(cells):
    s,h,w=normalize_shape(cells)
    if h<3 or w<3:
        return False
    border={(r,c) for r in range(h) for c in range(w) if r in (0,h-1) or c in (0,w-1)}
    return s==border

def is_horiz_symmetric(cells):
    s,h,w=normalize_shape(cells)
    return s == {(h-1-r,c) for r,c in s}

def perimeter_of_shape(cells):
    s,h,w=normalize_shape(cells)
    per=0
    for r,c in s:
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            if (r+dr,c+dc) not in s:
                per+=1
    return per

def pack_row(shapes_colors, sep=1):
    # list of (shape_set, color, h, w)
    H=max(h for _,_,h,w in shapes_colors) if shapes_colors else 0
    W=sum(w for _,_,h,w in shapes_colors)+sep*(len(shapes_colors)-1 if shapes_colors else 0)
    out=[[0]*W for _ in range(H)]
    x=0
    for shape,color,h,w in shapes_colors:
        for r,c in shape:
            out[r][x+c]=color
        x += w + sep
    return out

def solve_E22(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c]==v and g[r+1][c]==v and g[r][c-1]==v and g[r][c+1]==v:
                out[r][c]=8
    return out

def solve_E23(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                col=nz[0]
                pos=[(r,c),(r,c+1),(r+1,c),(r+1,c+1)]
                for (rr,cc),v in zip(pos,vals):
                    if v==0:
                        out[rr][cc]=col
    return out

def solve_E24(g):
    h,w=dims(g); out=clone(g)
    for r,c0,c1,v in horizontal_runs(g):
        if c1-c0+1==3:
            if c0-1>=0 and g[r][c0-1]==0:
                out[r][c0-1]=v
            if c1+1<w and g[r][c1+1]==0:
                out[r][c1+1]=v
    return out

def solve_E25(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            if c+1<w and g[r][c+1]==0:
                out[r][c+1]=v if out[r][c+1]==0 else out[r][c+1]
            else:
                out[r][c]=v if out[r][c]==0 else out[r][c]
    return out

def solve_E26(g):
    out=clone(g)
    for c,r0,r1,v in vertical_runs(g):
        if r1-r0+1==3:
            out[r0][c]=8; out[r1][c]=8
    return out

def solve_E27(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c-1]==v and g[r-1][c+1]==v and g[r+1][c-1]==v and g[r+1][c+1]==v:
                out[r][c]=8
    return out

def solve_E28(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            nbrs=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if all(not (0<=nr<h and 0<=nc<w and g[nr][nc]!=0) for nr,nc in nbrs):
                if c-1>=0 and out[r][c-1]==0: out[r][c-1]=v
                if c+1<w and out[r][c+1]==0: out[r][c+1]=v
    return out

def solve_M22(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if border_count(cells,h,w)==1:
            for r,c in cells: out[r][c]=col
    return out

def solve_M23(g):
    comps=components(g)
    chosen=max(comps, key=lambda x: ((bbox(x[1])[1]-bbox(x[1])[0]+1), len(x[1]), -bbox(x[1])[0], -bbox(x[1])[2]))
    out=clone(g)
    for r,c in chosen[1]:
        out[r][c]=8
    return out

def solve_M24(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for r,c in cells:
            out[r-r0][c]=col
    return out

def solve_M25(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for rr,cc in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            out[rr][cc]=col
    return out

def solve_M26(g):
    out=clone(g)
    for col,cells in components(g):
        if is_rect_frame(cells):
            r0,r1,c0,c1=bbox(cells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=col
    return out

def solve_M27(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if hole_cells_of_component(g,cells):
            for r,c in cells: out[r][c]=col
    return out

def solve_M28(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if is_horiz_symmetric(cells):
            for r,c in cells: out[r][c]=col
    return out

def solve_H22(g):
    items=[]
    for col,cells in components(g):
        s,h,w=normalize_shape(cells)
        per=perimeter_of_shape(cells)
        r0,r1,c0,c1=bbox(cells)
        items.append((per, r0, c0, s, col, h, w))
    items.sort(key=lambda t:(t[0], t[1], t[2]))
    shapes=[(s,col,h,w) for per,r0,c0,s,col,h,w in items]
    return pack_row(shapes, sep=1)

def solve_H23(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        s,hh,ww=normalize_shape(cells)
        rot={(c, hh-1-r) for r,c in s}
        r0,r1,c0,c1=bbox(cells)
        for r,c in rot:
            out[r0+r][c0+c]=col
    return out

def solve_H24(g):
    comps=components(g)
    # template is unique non-9 component; markers are 9 singletons
    tpl=[(col,cells) for col,cells in comps if col!=9]
    markers=[cells[0] for col,cells in comps if col==9 and len(cells)==1]
    assert len(tpl)==1
    col,cells=tpl[0]
    s,h,w=normalize_shape(cells)
    rot={(c, h-1-r) for r,c in s}
    out=[[0]*len(g[0]) for _ in range(len(g))]
    # stamp rotated shape with top-left at marker
    H,W=dims(g)
    for mr,mc in markers:
        for r,c in rot:
            rr,cc=mr+r,mc+c
            if 0<=rr<H and 0<=cc<W:
                out[rr][cc]=col
    return out

def solve_H25(g):
    groups=defaultdict(list)
    for col,cells in components(g):
        s,h,w=normalize_shape(cells)
        r0,r1,c0,c1=bbox(cells)
        groups[(frozenset(s),h,w)].append((r0,c0,col,cells))
    fam=max(groups.items(), key=lambda kv:(len(kv[1]), len(kv[0][0]), kv[0][1], kv[0][2], -min(item[0] for item in kv[1])))
    key,items=fam
    s,h,w=set(key[0]), key[1], key[2]
    items=sorted(items, key=lambda x:(x[0],x[1]))
    shapes=[(s, col, h, w) for r0,c0,col,cells in items]
    return pack_row(shapes, sep=1)

def solve_H26(g):
    h,w=dims(g)
    # assume one full-width guide row of 9s
    guide=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            guide=r; break
    assert guide is not None
    out=[[0]*w for _ in range(h)]
    # preserve guide? Maybe output only mirrored objects, no guide. Need decide
    # let's not preserve guide to make task clearer? But mirror across guide maybe preserve? Usually preserve maybe yes.
    for c in range(w):
        out[guide][c]=9
    # objects above guide mirrored below and vice versa
    comps=components(g)
    for col,cells in comps:
        if col==9: continue
        for r,c in cells:
            rr = 2*guide - r
            if 0<=rr<h:
                out[rr][c]=col
    return out

def solve_H27(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda x:(-len(x[1]), bbox(x[1])[0], bbox(x[1])[2]))
    (col1,c1),(col2,c2)=comps_sorted[:2]
    s1,h1,w1=normalize_shape(c1); s2,h2,w2=normalize_shape(c2)
    H=max(h1,h2); W=max(w1,w2)
    out=[[0]*W for _ in range(H)]
    for r,c in s1|s2:
        out[r][c]=8
    return out

def solve_H28(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda x:(-len(x[1]), bbox(x[1])[0], bbox(x[1])[2]))
    (col1,c1),(col2,c2)=comps_sorted[:2]
    s1,h1,w1=normalize_shape(c1); s2,h2,w2=normalize_shape(c2)
    H=max(h1,h2); W=max(w1,w2)
    diff=s1 - s2
    out=[[0]*W for _ in range(H)]
    for r,c in diff:
        out[r][c]=col1
    return out

SOLVERS = {
    "E22": solve_E22,
    "E23": solve_E23,
    "E24": solve_E24,
    "E25": solve_E25,
    "E26": solve_E26,
    "E27": solve_E27,
    "E28": solve_E28,
    "M22": solve_M22,
    "M23": solve_M23,
    "M24": solve_M24,
    "M25": solve_M25,
    "M26": solve_M26,
    "M27": solve_M27,
    "M28": solve_M28,
    "H22": solve_H22,
    "H23": solve_H23,
    "H24": solve_H24,
    "H25": solve_H25,
    "H26": solve_H26,
    "H27": solve_H27,
    "H28": solve_H28,
}
