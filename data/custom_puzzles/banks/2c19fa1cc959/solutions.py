"""
ARC-style puzzle bank continuation 10: 21 more puzzles (E64-E70, M64-M70, H64-H70).

This batch leans into interval completion, local legends, sweeping, frame
transplant, panel inference, labeled dispatch, compartment filling,
transform programs, and compact shape packing.

Notable motifs:
- sweep_component_away(anchor, shape): M64
- infer_panel_transform(example_in, example_out, query): H64
- label_dispatch(components, labels, targets): H65
- compartment_seed_fill(frame, walls, seeds): H67
- compose_ops(header, shape): H68
- sort_pack_palette(components, palette): H70
"""

from __future__ import annotations
from typing import List, Tuple, Iterable
from collections import deque

Grid = List[List[int]]

def blank(h:int, w:int, v:int=0)->Grid:
    return [[v]*w for _ in range(h)]

def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0])

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def overlay(dst:Grid, src:Grid, top:int=0, left:int=0, transparent:int=0)->Grid:
    h,w=dims(src)
    for r in range(h):
        for c in range(w):
            v=src[r][c]
            if v != transparent:
                rr,cc=top+r,left+c
                if 0 <= rr < len(dst) and 0 <= cc < len(dst[0]):
                    dst[rr][cc]=v
    return dst

def bbox(cells):
    cells=list(cells)
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def normalize_cells(cells):
    cells=list(cells)
    r0,r1,c0,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1,c1-c0+1), (r0,c0)

def components_by_color(g:Grid, ignore=(0,)):
    h,w=dims(g)
    seen=set()
    comps=[]
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
                    if 0 <= nx < h and 0 <= ny < w and g[nx][ny]==v and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((v,cells))
    return comps

def rotate_cw(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]

def flip_h(g:Grid)->Grid:
    return [row[::-1] for row in g]

def flip_v(g:Grid)->Grid:
    return g[::-1]

def crop_nonzero(g:Grid)->Grid:
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def split_by_separator_cols(g:Grid, sep:int=9):
    h,w=dims(g)
    sep_cols=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    parts=[]
    last=0
    for c in sep_cols+[w]:
        if c>last:
            parts.append([row[last:c] for row in g])
        last=c+1
    return parts, sep_cols

def bfs_same_color(g, start, seen):
    h,w=dims(g)
    sr,sc=start; col=g[sr][sc]
    q=deque([start]); seen.add(start); cells=[]
    while q:
        r,c=q.popleft(); cells.append((r,c))
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            rr,cc=r+dr,c+dc
            if 0<=rr<h and 0<=cc<w and (rr,cc) not in seen and g[rr][cc]==col:
                seen.add((rr,cc)); q.append((rr,cc))
    return cells

def is_frame_component(cells):
    r0,r1,c0,c1=bbox(cells)
    box={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
    return set(cells)==box

def apply_ops(panel, ops):
    g=panel
    for op in ops:
        if op==1:
            g=flip_h(g)
        elif op==2:
            g=flip_v(g)
        elif op==3:
            g=rotate_cw(g)
        elif op==4:
            g=rotate180(g)
    return g

def solve_E64(g):
    out=clone(g); h,w=dims(g)
    for c in range(w):
        by={}
        for r in range(h):
            v=g[r][c]
            if v!=0:
                by.setdefault(v,[]).append(r)
        for color,rows in by.items():
            if len(rows)==2:
                a,b=min(rows),max(rows)
                if all(g[r][c]==0 for r in range(a+1,b)):
                    for r in range(a,b+1):
                        out[r][c]=color
    return out

def solve_E65(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            neigh=[g[r+dr][c+dc] for dr in (-1,0,1) for dc in (-1,0,1) if not (dr==0 and dc==0)]
            if neigh[0]!=0 and all(v==neigh[0] for v in neigh):
                out[r][c]=neigh[0]
    return out

def solve_E66(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        if 9 not in g[r]:
            continue
        p=g[r].index(9)
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cc=2*p-c
                if 0<=cc<w:
                    out[r][cc]=v
    return out

def solve_E67(g):
    out=clone(g)
    by={}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v,[]).append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            rs=sorted({r for r,c in cells}); cs=sorted({c for r,c in cells})
            if len(rs)==2 and len(cs)==2:
                for rr in rs:
                    for cc in cs:
                        out[rr][cc]=color
    return out

def solve_E68(g):
    out=clone(g)
    for r,row in enumerate(g):
        counts={}
        for v in row:
            if v!=0:
                counts[v]=counts.get(v,0)+1
        if len(counts)==2:
            maj=max(counts, key=lambda k: counts[k])
            minc=min(counts.values())
            maxc=max(counts.values())
            if minc==1 and maxc>1:
                odd=[k for k,v in counts.items() if v==1][0]
                for c,v in enumerate(row):
                    if v==odd:
                        out[r][c]=maj
    return out

def solve_E69(g):
    out=clone(g)
    by={}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v,[]).append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=sorted(cells)
            dr=r2-r1; dc=c2-c1
            if abs(dr)==1 and abs(dc)==1:
                rr,cc=r2+dr,c2+dc
                if 0<=rr<len(g) and 0<=cc<len(g[0]):
                    out[rr][cc]=color
    return out

def solve_E70(g):
    out=clone(g); h,w=dims(g)
    headers=g[0]
    for r in range(1,h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=headers[c] if headers[c]!=0 else g[r][c]
    return out

def solve_M64(g):
    out=clone(g)
    h,w=dims(g)
    # component excluding 0 and 9, assume one color component
    comps=[(v,cells) for v,cells in components_by_color(g, ignore=(0,9))]
    assert len(comps)==1
    color,cells=comps[0]
    r0,r1,c0,c1=bbox(cells)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    assert len(anchors)==1
    ar,ac=anchors[0]
    if ac < c0:
        dr,dc = 0,1
    elif ac > c1:
        dr,dc = 0,-1
    elif ar < r0:
        dr,dc = 1,0
    else:
        dr,dc = -1,0
    norm=list(cells)
    k=1
    while True:
        shifted=[(r+dr*k,c+dc*k) for r,c in norm]
        if any(not (0<=r<h and 0<=c<w) for r,c in shifted):
            break
        for r,c in shifted:
            out[r][c]=color
        k+=1
    return out

def solve_M65(g):
    out=clone(g)
    headers=[v for v in g[0] if v!=0]
    comps=[cells for v,cells in components_by_color(g, ignore=(0,)) if v==8]
    comps=sorted(comps, key=lambda cells: (len(cells), bbox(cells)))
    for cells,color in zip(comps, headers):
        for r,c in cells:
            out[r][c]=color
    return out

def solve_M66(g):
    out=clone(g)
    mapping={}
    w=len(g[0])
    for c in range(w):
        a,b=g[0][c],g[1][c]
        if a!=0:
            mapping[a]=b
    for r in range(2,len(g)):
        for c in range(w):
            v=g[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out

def solve_M67(g):
    out=clone(g)
    frames=[cells for v,cells in components_by_color(g, ignore=(0,)) if v==7 and is_frame_component(cells)]
    frames=sorted(frames, key=len)
    small,big=frames[0],frames[1]
    sr0,sr1,sc0,sc1=bbox(small)
    br0,br1,bc0,bc1=bbox(big)
    interior=[row[sc0+1:sc1] for row in g[sr0+1:sr1]]
    ih,iw=len(interior), len(interior[0])
    top=br0+1 + ((br1-br0-1)-ih)//2
    left=bc0+1 + ((bc1-bc0-1)-iw)//2
    overlay(out, interior, top, left, transparent=0)
    return out

def solve_M68(g):
    h,w=dims(g)
    out=blank(h,w,0)
    rows=set()
    cols=set()
    for color,cells in components_by_color(g, ignore=(0,)):
        r0,r1,c0,c1=bbox(cells)
        if color==2:
            rows.update(range(r0,r1+1))
        elif color==3:
            cols.update(range(c0,c1+1))
    for r in rows:
        for c in cols:
            out[r][c]=8
    return out

def solve_M69(g):
    h,w=dims(g)
    sep = next(r for r in range(h) if all(v==9 for v in g[r]))
    top = g[:sep]
    bottom = g[sep+1:]
    # prototypes in top keyed by their nonzero color
    comps=[(v,cells) for v,cells in components_by_color(top, ignore=(0,))]
    protos={}
    for color,cells in comps:
        shp,(sh,sw),_ = normalize_cells(cells)
        protos[color]=(shp,sh,sw)
    key = next(v for row in bottom for v in row if v not in (0,8))
    ar,ac = next((r,c) for r,row in enumerate(bottom) for c,v in enumerate(row) if v==8)
    out=clone(g)
    shp,sh,sw=protos[key]
    for r,c in shp:
        rr,cc=sep+1 + ar + r, ac + c
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=key
    return out

def solve_M70(g):
    h,w=dims(g)
    out=blank(h,w,0)
    rects={}
    for color in (2,3):
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        rects[color]=bbox(cells)
    a0,a1,b0,b1=rects[2]
    c0,c1,d0,d1=rects[3]
    r0,r1=max(a0,c0), min(a1,c1)
    c0_,c1_=max(b0,d0), min(b1,d1)
    if r0<=r1 and c0_<=c1_:
        for r in range(r0,r1+1):
            for c in range(c0_,c1_+1):
                out[r][c]=8
    return out

def solve_H64(g):
    parts,_ = split_by_separator_cols(g, sep=9)
    a,b,c = parts
    cands = [
        rotate_cw,
        rotate180,
        lambda x: rotate_cw(rotate180(x)),
        flip_h,
        flip_v,
    ]
    for fn in cands:
        if fn(a) == b:
            return fn(c)
    return c

def solve_H65(g):
    h,w=dims(g)
    out=blank(h,w,0)
    # preserve target labels on bottom row
    target_cols={}
    for c,v in enumerate(g[h-1]):
        if v in (1,2,3):
            out[h-1][c]=v
            target_cols[v]=c
    seen=set()
    sources=[]
    for r in range(h-1):
        for c in range(w):
            if g[r][c] in (1,2,3):
                label=g[r][c]
                # component starts somewhere to the right
                for cc in range(c+1, min(w, c+4)):
                    if g[r][cc] not in (0,1,2,3):
                        cells=bfs_same_color(g, (r,cc), seen)
                        sources.append((label,cells,g[r][cc]))
                        break
    for label,cells,color in sources:
        shp,(sh,sw),_ = normalize_cells(cells)
        base_col=target_cols[label]
        top = h-1-sh
        left = base_col
        for r,c in shp:
            rr,cc=top+r,left+c
            if 0<=rr<h-1 and 0<=cc<w:
                out[rr][cc]=color
    return out

def solve_H66(g):
    h,w=dims(g)
    n=g[0][0]
    pivot=next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9)
    pr,pc=pivot
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,9) and not (r==0 and c==0)]
    # assume one color
    color = cells[0][2]
    offsets=[(r-pr, c-pc) for r,c,v in cells]
    def rot(dr,dc, k):
        for _ in range(k):
            dr,dc = dc,-dr
        return dr,dc
    out=blank(h,w,0)
    out[pr][pc]=9
    for k in range(n):
        for dr,dc in offsets:
            rr,cc = pr+rot(dr,dc,k)[0], pc+rot(dr,dc,k)[1]
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=color
    return out

def solve_H67(g):
    h,w=dims(g)
    out=clone(g)
    seen=set()
    walls={5,7}
    for r in range(h):
        for c in range(w):
            if g[r][c] in walls or (r,c) in seen:
                continue
            # region of non-wall cells
            q=deque([(r,c)]); seen.add((r,c))
            region=[]; colors=set()
            while q:
                x,y=q.popleft(); region.append((x,y))
                if g[x][y] not in (0,5,7):
                    colors.add(g[x][y])
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny] not in walls and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if len(colors)==1:
                color=next(iter(colors))
                for x,y in region:
                    if out[x][y]==0:
                        out[x][y]=color
    return out

def solve_H68(g):
    ops=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    body=crop_nonzero(body)
    return apply_ops(body, ops)

def solve_H69(g):
    parts,_ = split_by_separator_cols(g, sep=9)
    a,b,c = parts
    mapping={}
    h,w=dims(a)
    for r in range(h):
        for col in range(w):
            va,vb=a[r][col], b[r][col]
            if va!=0:
                mapping[va]=vb
    out=blank(h,w,0)
    for r in range(h):
        for col in range(w):
            v=c[r][col]
            if v!=0:
                out[r][col]=mapping.get(v,v)
    return out

def solve_H70(g):
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    comps=[cells for v,cells in components_by_color(body, ignore=(0,)) if v==8]
    comps=sorted(comps, key=lambda cells: (-len(cells), bbox(cells)))
    shapes=[]
    maxh=0
    for cells,color in zip(comps,palette):
        shp,(sh,sw),_ = normalize_cells(cells)
        shapes.append((shp,sh,sw,color))
        maxh=max(maxh,sh)
    totalw=sum(sw for _,_,sw,_ in shapes) + max(0,len(shapes)-1)
    out=blank(maxh,totalw,0)
    x=0
    for shp,sh,sw,color in shapes:
        top=maxh-sh
        for r,c in shp:
            out[top+r][x+c]=color
        x += sw+1
    return out

SOLVERS = {

    'E64': solve_E64,

    'E65': solve_E65,

    'E66': solve_E66,

    'E67': solve_E67,

    'E68': solve_E68,

    'E69': solve_E69,

    'E70': solve_E70,

    'M64': solve_M64,

    'M65': solve_M65,

    'M66': solve_M66,

    'M67': solve_M67,

    'M68': solve_M68,

    'M69': solve_M69,

    'M70': solve_M70,

    'H64': solve_H64,

    'H65': solve_H65,

    'H66': solve_H66,

    'H67': solve_H67,

    'H68': solve_H68,

    'H69': solve_H69,

    'H70': solve_H70,

}
