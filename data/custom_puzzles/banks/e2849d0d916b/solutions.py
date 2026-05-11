"""
ARC-style puzzle bank continuation 17: 21 more puzzles (E113-E119, M113-M119, H113-H119).

This batch leans into symbolic legends, simple symmetry, anchored stamping, panel majority logic,
bbox-relative edit transfer, geodesic seed filling, prototype family dispatch, and transform composition.

Notable motifs:
- legend_strip_recolor(source_row, target_row, body): M113
- anchor_stamp(prototype_with_anchor, target_markers): M116
- panel_majority_vote(p1, p2, p3): M117
- cutout_stencil_transfer(example_before, example_after, query): H115
- conflict_merge(a, b): H116
- compose_inferred_transforms(a, b, c, d, q): H119
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

def rot90(g):
    return [list(row) for row in zip(*g[::-1])]

def rot180(g):
    return [row[::-1] for row in g[::-1]]

def rot270(g):
    return [list(row) for row in zip(*g)][::-1]

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def transpose(g):
    return [list(row) for row in zip(*g)]

def anti_transpose(g):
    h,w=dims(g)
    out=[[0]*h for _ in range(w)]
    for r in range(h):
        for c in range(w):
            out[w-1-c][h-1-r]=g[r][c]
    return out

def split_panel_row(g, count, sep=5):
    h,w=dims(g)
    # infer panel width
    # count panels separated by single sep columns
    pw=(w-(count-1))//count
    panels=[]
    c=0
    for i in range(count):
        panels.append([row[c:c+pw] for row in g])
        c+=pw
        if i<count-1:
            assert all(row[c]==sep for row in g)
            c+=1
    return panels

def find_rect_frames(grid, color=5):
    frames=[]
    for col,cells in cc(grid):
        if col!=color:
            continue
        r0,r1,c0,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border:
            frames.append((r0,r1,c0,c1))
    return frames

def cc_any(grid, ignore=(0,)):
    return cc(grid, ignore=ignore, same_color=False)

def normalize_shape(cells):
    r0,r1,c0,c1=bbox(cells)
    return [(r-r0,c-c0) for r,c in cells], (r1-r0+1,c1-c0+1)

def infer_transform(a,b):
    for name,f in TRANSFORMS.items():
        if f(a)==b:
            return name,f
    raise ValueError("no transform")

def merge_op(a,b):
    h,w=dims(a)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            x,y=a[r][c],b[r][c]
            if x==0 and y==0: out[r][c]=0
            elif x==0: out[r][c]=y
            elif y==0: out[r][c]=x
            elif x==y: out[r][c]=x
            else: out[r][c]=9
    return out

def canonical_shape(panel):
    # return set of nonzero cells normalized
    cells=[(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v!=0]
    if not cells: return frozenset()
    r0,r1,c0,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def transformed_variants(panel):
    vars=[]
    for name,f in TRANSFORMS.items():
        p=f(panel)
        vars.append((name,p,canonical_shape(p)))
    return vars

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

def solve_E113(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][0]==cells[1][0]:
            r=cells[0][0]
            a,b=sorted([cells[0][1],cells[1][1]])
            if all(grid[r][c]==0 for c in range(a+1,b)):
                for c in range(a,b+1):
                    out[r][c]=color
    return out

def solve_E114(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if dr==dc and dr!=0:
                step=1 if dr>0 else -1
                if all(grid[r1+i*step][c1+i*step]==0 for i in range(1,abs(dr))):
                    for i in range(abs(dr)+1):
                        out[r1+i*step][c1+i*step]=color
    return out

def solve_E115(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                color=nz[0]
                idx=vals.index(0)
                rr=r+(idx//2); cc_=c+(idx%2)
                out[rr][cc_]=color
    return out

def solve_E116(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out

def solve_E117(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c]==0:
                ns=[grid[r-1][c],grid[r+1][c],grid[r][c-1],grid[r][c+1]]
                if ns[0]!=0 and ns.count(ns[0])==4:
                    out[r][c]=ns[0]
    return out

def solve_E118(grid):
    h,w=dims(grid)
    out=clone(grid)
    # full-height single-color divider column (all same nonzero)
    divider=None
    dcolor=None
    for c in range(w):
        col=[grid[r][c] for r in range(h)]
        if col[0]!=0 and all(v==col[0] for v in col):
            divider=c; dcolor=col[0]; break
    assert divider is not None
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and c!=divider and v!=dcolor:
                mc=2*divider-c
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=v
    return out

def solve_E119(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2 and (c1+c2)%2==0:
                m=(c1+c2)//2
                if grid[r1][m]==0:
                    out[r1][m]=color
            elif c1==c2 and (r1+r2)%2==0:
                m=(r1+r2)//2
                if grid[m][c1]==0:
                    out[m][c1]=color
    return out

def solve_M113(grid):
    out=clone(grid)
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        s=grid[0][c]
        t=grid[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out

def solve_M114(grid):
    out=clone(grid)
    comps=cc(grid)
    proto=None
    for color,cells in comps:
        if color!=5:
            proto=(color,cells)
            break
    assert proto
    pcolor,pcells=proto
    pr0,pr1,pc0,pc1=bbox(pcells)
    shape=[(r-pr0,c-pc0) for r,c in pcells]
    ph,pw=pr1-pr0+1,pc1-pc0+1
    for r0,r1,c0,c1 in find_rect_frames(grid,5):
        ih,iw=(r1-r0-1),(c1-c0-1)
        if ih==ph and iw==pw:
            for dr,dc in shape:
                out[r0+1+dr][c0+1+dc]=pcolor
    return out

def solve_M115(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        touches=set()
        for r,c in cells:
            if r==0: touches.add('top')
            if r==h-1: touches.add('bottom')
            if c==0: touches.add('left')
            if c==w-1: touches.add('right')
        if 'top' in touches:
            new=2
        elif 'bottom' in touches:
            new=3
        elif 'left' in touches:
            new=4
        elif 'right' in touches:
            new=6
        else:
            new=8
        for r,c in cells:
            out[r][c]=new
    return out

def solve_M116(grid):
    out=clone(grid)
    comps=cc_any(grid)
    proto_cells=None
    anchor=None
    targets=[]
    for _,cells in comps:
        colors=[grid[r][c] for r,c in cells]
        if 8 in colors and len(cells)>1:
            proto_cells=cells
            anchor=[(r,c) for r,c in cells if grid[r][c]==8][0]
        elif len(cells)==1 and grid[cells[0][0]][cells[0][1]]==8:
            targets.append(cells[0])
    assert proto_cells is not None
    rel=[(r-anchor[0], c-anchor[1], grid[r][c]) for r,c in proto_cells]
    h,w=dims(grid)
    for tr,tc in targets:
        for dr,dc,val in rel:
            nr,nc=tr+dr,tc+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=val
    return out

def solve_M117(grid):
    panels=split_panel_row(grid,3,sep=5)
    h,w=dims(panels[0])
    out=blank(h,w)
    # choose majority of occupancy; color = max nonzero among occupied? maybe fixed 2 if occupied.
    # Use dominant nonzero color among panels if >=2 nonzero and same? To keep simple use color from nonzero cells if at least two agree or one nonzero repeated.
    for r in range(h):
        for c in range(w):
            vals=[p[r][c] for p in panels]
            nz=[v for v in vals if v!=0]
            if len(nz)>=2:
                # choose most common nonzero color
                counts=defaultdict(int)
                for v in nz: counts[v]+=1
                v=max(counts, key=lambda k:(counts[k], k))
                out[r][c]=v
    return out

def solve_M118(grid):
    comps=cc(grid)
    items=[]
    for idx,(color,cells) in enumerate(comps):
        shape,(h,w)=normalize_shape(cells)
        items.append((len(cells), idx, color, shape, h, w))
    items.sort(key=lambda x:(-x[0], x[1]))
    H=max(h for _,_,_,_,h,w in items) if items else 0
    W=sum(w for _,_,_,_,h,w in items)+max(0,len(items)-1)
    out=blank(H,W)
    x=0
    for area,idx,color,shape,h,w in items:
        for r,c in shape:
            out[r][x+c]=color
        x+=w+1
    return out

def solve_M119(grid):
    panels=split_panel_row(grid,4,sep=5)
    qpanel=panels[0]
    q=None
    for row in qpanel:
        for v in row:
            if v!=0:
                q=v; break
        if q is not None: break
    assert q is not None
    best=max(panels[1:], key=lambda p: sum(v==q for row in p for v in row))
    return best

def solve_H113(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    _,f = infer_transform(a,b)
    return f(c)

def solve_H114(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    mapping={}
    h,w=dims(a)
    for r in range(h):
        for col in range(w):
            va,vb=a[r][col],b[r][col]
            if va!=0:
                mapping[va]=vb
    out=clone(c)
    for r in range(h):
        for col in range(w):
            v=c[r][col]
            if v in mapping:
                out[r][col]=mapping[v]
    return out

def solve_H115(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    # compute removed cells relative to bbox of nonzero in a
    cells_a=[(r,col) for r,row in enumerate(a) for col,v in enumerate(row) if v!=0]
    cells_b={(r,col) for r,row in enumerate(b) for col,v in enumerate(row) if v!=0}
    ar0,ar1,ac0,ac1=bbox(cells_a)
    removed=[]
    for r,col in cells_a:
        if (r,col) not in cells_b:
            removed.append((r-ar0, col-ac0))
    out=clone(c)
    cells_c=[(r,col) for r,row in enumerate(c) for col,v in enumerate(row) if v!=0]
    cr0,cr1,cc0,cc1=bbox(cells_c)
    for dr,dc in removed:
        rr,cc_=cr0+dr, cc0+dc
        if 0<=rr<len(out) and 0<=cc_<len(out[0]):
            out[rr][cc_]=0
    return out

def solve_H116(grid):
    a,b,ex,d,e = split_panel_row(grid,5,sep=5)
    # could verify ex equals merge_op(a,b)
    return merge_op(d,e)

def solve_H117(grid):
    h,w=dims(grid)
    out=clone(grid)
    # identify all seeds nonzero not wall
    seeds=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,5):
                seeds.append((r,c,v))
    # BFS distances within non-wall cells
    from collections import deque
    INF=10**9
    dists={}
    for sr,sc,color in seeds:
        dist=[[INF]*w for _ in range(h)]
        q=deque([(sr,sc)])
        dist[sr][sc]=0
        while q:
            r,c=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and grid[nr][nc]!=5 and dist[nr][nc]==INF:
                    dist[nr][nc]=dist[r][c]+1
                    q.append((nr,nc))
        dists[(sr,sc,color)] = dist
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                continue
            best=None; winners=[]
            for key,dist in dists.items():
                d=dist[r][c]
                if best is None or d<best:
                    best=d; winners=[key]
                elif d==best:
                    winners.append(key)
            if len(winners)==1:
                out[r][c]=winners[0][2]
            else:
                out[r][c]=8
    return out

def solve_H118(grid):
    p1,p2,p3,q = split_panel_row(grid,4,sep=5)
    prototypes=[]
    for p in [p1,p2,p3]:
        # label color = unique nonzero color in last row? maybe prototype colored already.
        colors={v for row in p for v in row if v!=0}
        # use max color as label? Hmm we will design prototype panels monochrome colored with label color.
        label=max(colors)
        shape_panel=[[1 if v!=0 else 0 for v in row] for row in p]
        variants={canon for _,_,canon in transformed_variants(shape_panel)}
        prototypes.append((label,variants))
    qshape_panel=[[1 if v!=0 else 0 for v in row] for row in q]
    qcanon=canonical_shape(qshape_panel)
    label=next(lbl for lbl,vars in prototypes if qcanon in vars)
    out=blank(*dims(q))
    for r,row in enumerate(q):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=label
    return out

def solve_H119(grid):
    a,b,c,d,q = split_panel_row(grid,5,sep=5)
    _,f1=infer_transform(a,b)
    _,f2=infer_transform(c,d)
    return f2(f1(q))
