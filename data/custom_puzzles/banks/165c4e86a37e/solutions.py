"""
ARC-style puzzle bank continuation 6: 21 more puzzles (E36-E42, M36-M42, H36-H42).
This batch leans into transposition, column gravity, local-frame transforms, panel masking,
and anchor-based reflection. Two notable reusable motifs here are panel_mask(mask, canvas)
and anchor_reflect(shape, anchor), especially in H41 and H42.
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
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col,cells))
    return comps

def nz_components(g, ignore_colors=None):
    ignore_colors=set(ignore_colors or [])
    h,w=dims(g)
    seen=set(); comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or g[r][c] in ignore_colors or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]!=0 and g[nx][ny] not in ignore_colors and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append(cells)
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def normalize(cells):
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1), (r0,c0)

def rotate_shape(shape, h, w, k):
    # shape set of (r,c), rotate k times 90 cw
    s=set(shape)
    hh,ww=h,w
    for _ in range(k%4):
        s={(c,hh-1-r) for r,c in s}
        hh,ww=ww,hh
    return s, hh, ww

def hmirror_shape(shape, h, w):
    return {(r,w-1-c) for r,c in shape}

def vmirror_shape(shape, h, w):
    return {(h-1-r,c) for r,c in shape}

def anti_diag_reflect(shape, n):
    # within n x n square
    return {(n-1-c,n-1-r) for r,c in shape}

def transpose_shape(shape):
    return {(c,r) for r,c in shape}

def fill_holes_shape(shape, h, w):
    # shape set in bbox, single-color solid border/hollow; fill enclosed zeros
    grid=[[1 if (r,c) in shape else 0 for c in range(w)] for r in range(h)]
    seen=[[False]*w for _ in range(h)]
    q=deque()
    for r in range(h):
        for c in range(w):
            if r in (0,h-1) or c in (0,w-1):
                if grid[r][c]==0 and not seen[r][c]:
                    seen[r][c]=True;q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc]==0 and not seen[nr][nc]:
                seen[nr][nc]=True;q.append((nr,nc))
    out=set(shape)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0 and not seen[r][c]:
                out.add((r,c))
    return out

def solve_E36(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    # check both diagonals for endpoints exactly 2 apart
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0: continue
            for dr,dc in [(2,2),(2,-2)]:
                r2,c2=r+dr,c+dc
                if 0<=r2<h and 0<=c2<w and g[r2][c2]==col:
                    rm,cm=r+dr//2,c+dc//2
                    if g[rm][cm]==0:
                        out[rm][cm]=col
    return out

def solve_E37(g):
    h,w=dims(g)
    assert h==w
    return [list(row) for row in zip(*g)]

def solve_E38(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==8:
                out[r][c]=g[0][c]
    return out

def solve_E39(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                v=g[r][c]
                for dr in [0,1]:
                    for dc in [0,1]:
                        if 0<=r+dr<h and 0<=c+dc<w:
                            out[r+dr][c+dc]=v
    return out

def solve_E40(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v==0: continue
            if g[r-1][c-1]==v and g[r+1][c+1]==v:
                out[r][c]=8
            if g[r-1][c+1]==v and g[r+1][c-1]==v:
                out[r][c]=8
    return out

def solve_E41(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[i][c]=v
    return out

def solve_E42(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            border=[]
            for rr in [r-1,r,r+1]:
                for cc in [c-1,c,c+1]:
                    if rr==r and cc==c: 
                        continue
                    border.append(g[rr][cc])
            if border and len(set(border))==1 and border[0]!=0:
                out[r][c]=border[0]
    return out

def solve_M36(g):
    comps=same_color_components(g)
    areas=sorted((len(cells), idx) for idx,(col,cells) in enumerate(comps))
    median_idx=areas[len(areas)//2][1]
    out=blank(*dims(g))
    col,cells=comps[median_idx]
    for r,c in cells:
        out[r][c]=col
    return out

def solve_M37(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        r0,r1,c0,c1=bbox(cells)
        shift=h-1-r1
        for r,c in cells:
            out[r+shift][c]=col
    return out

def solve_M38(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        tshape=transpose_shape(shape)
        # dims swap
        for dr,dc in tshape:
            out[r0+dr][c0+dc]=col
    return out

def solve_M39(g):
    h,w=dims(g)
    header=g[0]
    comps=same_color_components([row[:] for row in g[1:]])  # relative rows 0..h-2
    out=clone(g)
    for col,cells in comps:
        # cells relative to body
        minc=min(c for r,c in cells)
        newcol=header[minc]
        for r,c in cells:
            out[r+1][c]=newcol
    return out

def solve_M40(g):
    h,w=dims(g)
    rows=[g[r][1:] for r in range(h) if g[r][0]==7]
    return rows

def solve_M41(g):
    h,w=dims(g)
    # smallest non-9 same-color component
    comps=same_color_components(g)
    non9=[(col,cells) for col,cells in comps if col!=9]
    col,cells=min(non9, key=lambda x: len(x[1]))
    shape,(hh,ww),_ = normalize(cells)
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in shape:
            out[mr+dr][mc+dc]=col
    return out

def solve_M42(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        assert hh==ww
        ashape=anti_diag_reflect(shape, hh)
        for dr,dc in ashape:
            out[r0+dr][c0+dc]=col
    return out

def solve_H36(g):
    h,w=dims(g)
    gr=gc=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            gr=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            gc=c; break
    out=clone(g)
    r0,r1,c0,c1=gr+1,h,0,gc
    # extract BL subgrid
    sub=[[g[r0+rr][c0+cc] if g[r0+rr][c0+cc]!=9 else 0 for cc in range(c1-c0)] for rr in range(r1-r0)]
    comps=same_color_components(sub)
    if comps:
        col,cells=comps[0]
        shape,(hh,ww),(sr,sc)=normalize(cells)
        filled=fill_holes_shape(shape,hh,ww)
        # place in BR with same relative top-left
        br_start_r, br_start_c = gr+1, gc+1
        for dr,dc in filled:
            out[br_start_r+sr+dr][br_start_c+sc+dc]=col
    return out

def solve_H37(g):
    h,w=dims(g)
    bh=h//3
    perm=[g[i][0] for i in range(3)]
    blocks=[ [row[1:] for row in g[i*bh:(i+1)*bh]] for i in range(3)]
    out=[]
    for p in perm:
        out.extend([row[:] for row in blocks[p-1]])
    return out

def solve_H38(g):
    h,w=dims(g)
    arrow=g[0][0]
    comps=same_color_components(g)
    # template = largest component with color not 0,9,arrow and area>1
    candidates=[(col,cells) for col,cells in comps if col not in (0,9,arrow) and len(cells)>1]
    col,cells=max(candidates,key=lambda x: len(x[1]))
    shape,(hh,ww),_ = normalize(cells)
    rot_map={1:0,2:1,3:2,4:3}
    rshape,nh,nw=rotate_shape(shape,hh,ww,rot_map[arrow])
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in rshape:
            out[mr+dr][mc+dc]=col
    return out

def solve_H39(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    rot_map={1:0,2:1,3:2,4:3}
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        assert hh==ww
        rshape,nh,nw=rotate_shape(shape,hh,ww,rot_map[col])
        for dr,dc in rshape:
            out[r0+dr][c0+dc]=col
    return out

def solve_H40(g):
    h,w=dims(g)
    a,b=g[0][0],g[0][1]
    # template = largest nz component excluding 9 and header row colors in row0? We ignore row0 entirely for extraction except markers maybe none.
    body=[[g[r][c] if r>0 else 0 for c in range(w)] for r in range(h)]
    comps=nz_components(body, ignore_colors={9})
    # choose largest comp that is not marker singletons?
    template=max(comps, key=len)
    r0,r1,c0,c1=bbox(template)
    # capture multicolor bbox from original g
    bbox_cells=[]
    shape_positions=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if g[r][c]!=0 and g[r][c]!=9:
                bbox_cells.append((r-r0,c-c0,g[r][c]))
                shape_positions.append((r-r0,c-c0))
    hh,ww=r1-r0+1,c1-c0+1
    # mirror horizontally and recolor 5->a, 6->b
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc,v in bbox_cells:
            ndc=ww-1-dc
            nv=a if v==5 else b if v==6 else v
            out[mr+dr][mc+ndc]=nv
    return out

def solve_H41(g):
    h,w=dims(g)
    # separator col all 9
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    pw=sep
    out=blank(h,pw)
    for r in range(h):
        for c in range(pw):
            if g[r][c]!=0 and g[r][sep+1+c]!=0:
                out[r][c]=g[r][sep+1+c]
    return out

def solve_H42(g):
    h,w=dims(g)
    # anchor 9 single cell
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    assert len(anchors)==1
    ar,ac=anchors[0]
    comps=same_color_components(g)
    # template is largest non9 component
    col,cells=max([(col,cells) for col,cells in comps if col!=9], key=lambda x: len(x[1]))
    shape,(hh,ww),(r0,c0)=normalize(cells)
    out=blank(h,w)
    # original copy
    placements=[]
    # reflect bbox top-left across anchor point axes
    def refl_h(c0): # across vertical line x=ac
        return 2*ac - c0 - ww + 1
    def refl_v(r0):
        return 2*ar - r0 - hh + 1
    placements.append((r0,c0,shape))
    placements.append((r0,refl_h(c0),hmirror_shape(shape,hh,ww)))
    placements.append((refl_v(r0),c0,vmirror_shape(shape,hh,ww)))
    placements.append((refl_v(r0),refl_h(c0),rotate_shape(shape,hh,ww,2)[0]))
    for pr,pc,pshape in placements:
        for dr,dc in pshape:
            out[pr+dr][pc+dc]=col
    return out
