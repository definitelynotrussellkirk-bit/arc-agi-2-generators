"""
ARC-style puzzle bank continuation 18: 21 more puzzles (E120-E126, M120-M126, H120-H126).

This batch leans into row metadata, mirror completion, legend strips, vector transport, mask cropping,
anchor stamping, example-inferred transforms, transform+recolor composition, inferred binary operations,
stencil transfer, nearest-seed fills, prototype-family matching, packed inventories, and transform-then-merge.

Notable motifs:
- row_header_dispatch(row): E120
- mask_crop_normalize(mask, source): M122
- operation_from_example(a, b, r): H121
- stencil_delta_transfer(before, after, query): H122
- prototype_family_match(library, query): H124
- transform_then_conflict_merge(example_before, example_after, x, y): H126
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def cc(g, ignore=(0,), same_color=True):
    h,w=dims(g)
    seen=set()
    out=[]
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

def cc_any(g, ignore=(0,)):
    return cc(g, ignore=ignore, same_color=False)

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


TRANSFORMS = {
    "id": lambda g: g,
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "anti_transpose": anti_transpose,
}

def split_panel_row(g, count, sep=5):
    h,w=dims(g)
    pw=(w-(count-1))//count
    panels=[]; c=0
    for i in range(count):
        panels.append([row[c:c+pw] for row in g])
        c+=pw
        if i<count-1:
            # assume separator
            c+=1
    return panels

def merge_op(a,b):
    h,w=dims(a); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            x,y=a[r][c],b[r][c]
            if x==0 and y==0: out[r][c]=0
            elif x==0: out[r][c]=y
            elif y==0: out[r][c]=x
            elif x==y: out[r][c]=x
            else: out[r][c]=9
    return out

def infer_transform(a,b):
    for name,f in TRANSFORMS.items():
        if f(a)==b:
            return name,f
    raise ValueError("no transform")

def canonical_shape(panel):
    cells=[(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v!=0]
    if not cells: return frozenset()
    r0,r1,c0,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def op_intersection_eq(a,b):
    h,w=dims(a); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if a[r][c]!=0 and a[r][c]==b[r][c]:
                out[r][c]=a[r][c]
    return out

def op_xor(a,b):
    h,w=dims(a); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            x,y=a[r][c],b[r][c]
            if (x!=0) ^ (y!=0):
                out[r][c]=x or y
    return out

def op_left_minus(a,b):
    h,w=dims(a); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if a[r][c]!=0 and b[r][c]==0:
                out[r][c]=a[r][c]
    return out


OPS = {
    "intersection_eq": op_intersection_eq,
    "xor": op_xor,
    "left_minus": op_left_minus,
    "conflict_merge": merge_op,
}

def solve_E120(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        header=grid[r][0]
        if header!=0:
            markers=[c for c in range(1,w) if grid[r][c]==1]
            if len(markers)==1:
                out[r][0]=0
                out[r][markers[0]]=header
    return out

def solve_E121(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                idx=vals.index(0)
                rr=r+idx//2; cc_=c+idx%2
                out[rr][cc_]=nz[0]
    return out

def solve_E122(grid):
    h,w=dims(grid)
    comps=cc(grid)
    if not comps:
        return blank(h,w)
    comps_sorted=sorted(comps, key=lambda t: len(t[1]), reverse=True)
    keep=set(comps_sorted[0][1])
    out=blank(h,w)
    for color,cells in comps:
        if set(cells)==keep:
            for r,c in cells:
                out[r][c]=color
    return out

def solve_E123(grid):
    out=clone(grid)
    h,w=dims(grid)
    axes=[c for c in range(w) if all(grid[r][c]==9 for r in range(h))]
    assert len(axes)==1
    a=axes[0]
    for r in range(h):
        for c in range(a):
            v=grid[r][c]
            if v not in (0,9):
                mc=2*a-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def solve_E124(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==0: 
                continue
            neigh=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            same=[]; zeros=[]
            for rr,cc_ in neigh:
                if 0<=rr<h and 0<=cc_<w:
                    if grid[rr][cc_]==v: same.append((rr,cc_))
                    elif grid[rr][cc_]==0: zeros.append((rr,cc_))
            if len(same)==3 and len(zeros)>=1:
                # fill only if exactly one cardinal direction within bounds is zero and others same?
                # Determine directions
                vals=[]
                for rr,cc_ in neigh:
                    if 0<=rr<h and 0<=cc_<w:
                        vals.append(grid[rr][cc_])
                    else:
                        vals.append(None)
                if sum(x==v for x in vals)==3 and sum(x==0 for x in vals)==1:
                    idx=vals.index(0)
                    rr,cc_=neigh[idx]
                    out[rr][cc_]=v
    return out

def solve_E125(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            cells=[grid[r+i][c+j] for i in range(3) for j in range(3)]
            border=[cells[k] for k in [0,1,2,3,5,6,7,8]]
            center=cells[4]
            nz=[v for v in border if v!=0]
            if len(nz)==8 and len(set(nz))==1 and center==0:
                out[r+1][c+1]=nz[0]
    return out

def solve_E126(grid):
    h,w=dims(grid)
    out=blank(h,w)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                r0,r1_=sorted([r1,r2]); c0,c1_=sorted([c1,c2])
                for c in range(c0,c1_+1):
                    out[r0][c]=color
                    out[r1_][c]=color
                for r in range(r0,r1_+1):
                    out[r][c0]=color
                    out[r][c1_]=color
    return out

def solve_M120(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        s=grid[0][c]; t=grid[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    out=blank(h,w)
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            out[r][c]=mapping.get(v,v)
    return out

def solve_M121(grid):
    h,w=dims(grid)
    pos1=pos2=None
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==1: pos1=(r,c)
            elif grid[r][c]==2: pos2=(r,c)
    dr=pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,1,2):
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out

def solve_M122(grid):
    mask,src = split_panel_row(grid,2,sep=5)
    cells=[]
    colors={}
    h,w=dims(mask)
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0 and src[r][c]!=0:
                cells.append((r,c))
                colors[(r,c)]=src[r][c]
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for (r,c),v in colors.items():
        out[r-r0][c-c0]=v
    return out

def solve_M123(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body)
    comps_sorted=sorted(comps, key=lambda t: len(t[1]))  # ascending
    out=blank(h,w)
    for idx,(color,cells) in enumerate(comps_sorted):
        newc=palette[idx]
        for r,c in cells:
            out[r+1][c]=newc
    return out

def solve_M124(grid):
    h,w=dims(grid)
    comps=cc_any(grid, ignore=(0,))
    proto=None
    for color,cells in comps:
        vals=[grid[r][c] for r,c in cells]
        if 9 in vals and len(cells)>1:
            proto=cells
            break
    assert proto is not None
    anchor=[(r,c) for r,c in proto if grid[r][c]==9][0]
    rel=[(r-anchor[0], c-anchor[1], grid[r][c]) for r,c in proto if grid[r][c]!=9]
    targets=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    out=blank(h,w)
    for ar,ac in targets:
        for dr,dc,v in rel:
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

def solve_M125(grid):
    h,w=dims(grid)
    seen=set()
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=set()
            while q:
                x,y=q.popleft(); cells.append((x,y))
                v=grid[x][y]
                if v not in (0,5): seeds.add(v)
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if len(seeds)==1:
                color=next(iter(seeds))
                for x,y in cells:
                    if out[x][y]==0:
                        out[x][y]=color
    return out

def solve_M126(grid):
    a,b,q=split_panel_row(grid,3,sep=5)
    _,f=infer_transform(a,b)
    return f(q)

def solve_H120(grid):
    a,b,c,d,q=split_panel_row(grid,5,sep=5)
    _,f=infer_transform(a,b)
    # infer recolor map from c->d by position
    mapping={}
    h,w=dims(c)
    for r in range(h):
        for col in range(w):
            x,y=c[r][col],d[r][col]
            if x!=0 and y!=0:
                mapping[x]=y
    tq=f(q)
    out=clone(tq)
    h2,w2=dims(out)
    for r in range(h2):
        for c_ in range(w2):
            if out[r][c_]!=0:
                out[r][c_]=mapping.get(out[r][c_], out[r][c_])
    return out

def solve_H121(grid):
    a,b,r,x,y = split_panel_row(grid,5,sep=5)
    chosen=None
    for name,f in OPS.items():
        if f(a,b)==r:
            chosen=f
            break
    assert chosen is not None
    return chosen(x,y)

def solve_H122(grid):
    before,after,q = split_panel_row(grid,3,sep=5)
    # assume each panel has one colored object
    cb=[cells for color,cells in cc(before)][0]
    ca=[cells for color,cells in cc(after)][0]
    qb=[cells for color,cells in cc(q)][0]
    r0b,r1b,c0b,c1b=bbox(cb)
    r0a,r1a,c0a,c1a=bbox(ca)
    # additions relative to bbox, assuming after bbox same size or larger enough to contain before
    rel_before={(r-r0b,c-c0b) for r,c in cb}
    rel_after={(r-r0a,c-c0a) for r,c in ca}
    added=rel_after-rel_before
    qcolor=next(v for row in q for v in row if v!=0)
    r0q,r1q,c0q,c1q=bbox(qb)
    out=clone(q)
    for dr,dc in added:
        nr,nc=r0q+dr,c0q+dc
        if 0<=nr<len(out) and 0<=nc<len(out[0]):
            out[nr][nc]=qcolor
    return out

def solve_H123(grid):
    h,w=dims(grid)
    out=clone(grid)
    # find rooms of non-wall cells
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if not seeds:
                continue
            for x,y in cells:
                if grid[x][y]==0:
                    dists=[]
                    for sr,sc,col in seeds:
                        d=abs(sr-x)+abs(sc-y)  # same room, no walls inside component
                        dists.append((d,col))
                    mind=min(d for d,col in dists)
                    cols={col for d,col in dists if d==mind}
                    if len(cols)==1:
                        out[x][y]=next(iter(cols))
    return out

def solve_H124(grid):
    p1,p2,p3,q = split_panel_row(grid,4,sep=5)
    libs=[p1,p2,p3]
    qcells=[(r,c) for r,row in enumerate(q) for c,v in enumerate(row) if v!=0]
    qcolor=next(v for row in q for v in row if v!=0)
    qcanon=canonical_shape(q)
    chosen=None
    for lib in libs:
        # compare under symmetries
        for name,f in TRANSFORMS.items():
            if canonical_shape(f(lib))==qcanon:
                chosen=lib
                break
        if chosen is not None:
            break
    assert chosen is not None
    out=blank(*dims(chosen))
    for r,row in enumerate(chosen):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=qcolor
    return out

def solve_H125(grid):
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body)
    # sort by bbox height descending, then width descending
    items=[]
    for color,cells in comps:
        r0,r1,c0,c1=bbox(cells)
        h=r1-r0+1; w=c1-c0+1
        shape=blank(h,w)
        for r,c in cells:
            shape[r-r0][c-c0]=1
        items.append((h,w,shape))
    items.sort(key=lambda t:(-t[0],-t[1]))
    heights=[h for h,w,shape in items]
    total_h=max(heights) if items else 1
    total_w=sum(t[1] for t in items)+max(0,len(items)-1)
    out=blank(total_h,total_w)
    cur=0
    for idx,(h,w,shape) in enumerate(items):
        color=palette[idx]
        for r in range(h):
            for c in range(w):
                if shape[r][c]:
                    out[r][cur+c]=color
        cur+=w+1
    return out

def solve_H126(grid):
    a,b,x,y = split_panel_row(grid,4,sep=5)
    _,f=infer_transform(a,b)
    ty=f(y)
    return merge_op(x,ty)

PUZZLE_SOLVERS = {
    'E120': solve_E120,
    'E121': solve_E121,
    'E122': solve_E122,
    'E123': solve_E123,
    'E124': solve_E124,
    'E125': solve_E125,
    'E126': solve_E126,
    'M120': solve_M120,
    'M121': solve_M121,
    'M122': solve_M122,
    'M123': solve_M123,
    'M124': solve_M124,
    'M125': solve_M125,
    'M126': solve_M126,
    'H120': solve_H120,
    'H121': solve_H121,
    'H122': solve_H122,
    'H123': solve_H123,
    'H124': solve_H124,
    'H125': solve_H125,
    'H126': solve_H126,
}
