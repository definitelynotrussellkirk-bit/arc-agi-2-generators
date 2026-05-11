"""Reference solvers for ARC-style additional puzzle bank volume 5.

This volume introduces the helper primitive `slide_component`, a rigid-body
motion primitive that slides a cell set until the next step would collide
with the border or an occupied cell.
"""
from typing import List, Dict, Tuple, Set

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR_MARKER = {1:(-1,0), 2:(0,1), 3:(1,0), 4:(0,-1)}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]
def clone(g):
    return [row[:] for row in g]
def dims(g):
    return len(g), len(g[0])
def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w
def safe(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d
def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)
def components(g, colors=None, bg=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=g[r][c]
            if v==bg or (colors is not None and v not in colors):
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v, "cells":cells, "bbox":bbox(cells)})
    return out
def normalize_cells(cells):
    if not cells: return []
    r0,c0,_,_=bbox(cells)
    return [(r-r0,c-c0) for r,c in cells]
def manhattan(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
def slide_component(cells, occupied, h,w, dr,dc):
    """invented primitive: slide rigid cell set until next step collides"""
    cur=set(cells)
    while True:
        nxt={(r+dr,c+dc) for r,c in cur}
        if any(not (0<=r<h and 0<=c<w) for r,c in nxt):
            return cur
        if nxt & occupied:
            return cur
        cur=nxt
def trace_perimeter(cells):
    S=set(cells)
    return {(r,c) for r,c in S if any((r+dr,c+dc) not in S for dr,dc in DIR4)}
def hole_cells_of_component(comp):
    cells=set(comp["cells"])
    r0,c0,r1,c1=comp["bbox"]
    h=r1-r0+1; w=c1-c0+1
    # flood from bbox boundary through non-component cells
    seen=set()
    stack=[]
    for r in range(h):
        for c in range(w):
            gr,gc=r0+r,c0+c
            if gr==r0 or gr==r1 or gc==c0 or gc==c1:
                if (gr,gc) not in cells and (gr,gc) not in seen:
                    seen.add((gr,gc)); stack.append((gr,gc))
    while stack:
        rr,cc=stack.pop()
        for dr,dc in DIR4:
            nr,nc=rr+dr,cc+dc
            if r0<=nr<=r1 and c0<=nc<=c1 and (nr,nc) not in cells and (nr,nc) not in seen:
                seen.add((nr,nc)); stack.append((nr,nc))
    holes={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if (r,c) not in cells and (r,c) not in seen}
    return holes
def rowcol_closure(cells):
    if not cells: return set()
    r0,c0,r1,c1=bbox(cells)
    rows={r for r,c in cells}
    cols={c for r,c in cells}
    return {(r,c) for r in rows for c in cols}
def transpose_in_bbox(cells):
    if not cells: return set()
    r0,c0,r1,c1=bbox(cells)
    # assume square bbox or allow swapped dims if within same bbox? We'll use square.
    return {(r0+(c-c0), c0+(r-r0)) for r,c in cells}
def bfs_path(grid,start,goal,passable={0}):
    from collections import deque
    h,w=dims(grid)
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        for dr,dc in DIR4:
            nr,nc=cur[0]+dr,cur[1]+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and ((nr,nc)==goal or grid[nr][nc] in passable):
                prev[(nr,nc)]=cur
                q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur); cur=prev[cur]
    return path[::-1]
def raycast_coverage(g, seeds, wall_colors={8}):
    h,w=dims(g)
    cov=[[0]*w for _ in range(h)]
    for r,c in seeds:
        for dr,dc in DIR4:
            rr,cc=r+dr,c+dc
            while 0<=rr<h and 0<=cc<w and g[rr][cc] not in wall_colors:
                if g[rr][cc]==0:
                    cov[rr][cc]+=1
                rr+=dr; cc+=dc
    return cov
def parity_fill_chamber(g, seed, wall=8):
    from collections import deque
    h,w=dims(g)
    dist={seed:0}
    q=deque([seed])
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc]!=wall and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)]+1
                q.append((nr,nc))
    return dist

def solve_E29(g):
    h,w=dims(g)
    reds=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    out=clone(g)
    for r,c in reds:
        out[r][c]=0
    occupied={(r,c) for r in range(h) for c in range(w) if out[r][c]!=0}
    # bottommost first for stacking semantics
    for r,c in sorted(reds, reverse=True):
        pos=slide_component({(r,c)}, occupied, h,w, 1,0)
        nr,nc=next(iter(pos))
        out[nr][nc]=2
        occupied.add((nr,nc))
    return out
def solve_E30(g):
    out=clone(g)
    for comp in components(g, colors={3}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        border={(r0,c) for c in range(c0,c1+1)} | {(r1,c) for c in range(c0,c1+1)} | {(r,c0) for r in range(r0,r1+1)} | {(r,c1) for r in range(r0,r1+1)}
        if cells==border and r1-r0>=2 and c1-c0>=2:
            for p in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
                out[p[0]][p[1]]=4
    return out
def solve_E31(g):
    h,w=dims(g)
    out=clone(g)
    # horizontal
    for r in range(h):
        ones=[c for c in range(w) if g[r][c]==1]
        for i in range(len(ones)-1):
            c1,c2=ones[i],ones[i+1]
            if c2-c1>1 and all(g[r][c]==0 for c in range(c1+1,c2)):
                # ensure endpoints not part of vertical pair by preferring clear local context? examples disjoint
                for c in range(c1,c2+1):
                    out[r][c]=2
    # vertical
    for c in range(w):
        ones=[r for r in range(h) if g[r][c]==1]
        for i in range(len(ones)-1):
            r1,r2=ones[i],ones[i+1]
            if r2-r1>1 and all(g[r][c]==0 for r in range(r1+1,r2)):
                for r in range(r1,r2+1):
                    out[r][c]=2
    return out
def solve_E32(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals.count(7)==3 and vals.count(0)==1:
                idx=vals.index(0)
                rr,cc=[(r,c),(r,c+1),(r+1,c),(r+1,c+1)][idx]
                out[rr][cc]=7
    return out
def solve_E33(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==3:
                up=safe(g,r-1,c)==3; down=safe(g,r+1,c)==3; left=safe(g,r,c-1)==3; right=safe(g,r,c+1)==3
                if sum([up,down,left,right])==2 and (up or down) and (left or right):
                    out[r][c]=6
    return out
def solve_E34(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==1 and safe(g,r-1,c)==1 and safe(g,r+1,c)==1 and safe(g,r,c-1)==1 and safe(g,r,c+1)==1:
                out[r][c]=2
    return out
def solve_E35(g):
    h,w=dims(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out
def solve_M29(g):
    h,w=dims(g)
    marker=None; obj_cells=[]; blockers=set()
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in DIR_MARKER:
                marker=(r,c,v)
            elif v==5:
                blockers.add((r,c))
            elif v!=0:
                obj_cells.append((r,c))
    dr,dc=DIR_MARKER[marker[2]]
    out=clone(g)
    for r,c in obj_cells:
        out[r][c]=0
    occupied=blockers | {(marker[0],marker[1])}
    slid=slide_component(set(obj_cells), occupied, h,w, dr,dc)
    for r,c in slid:
        out[r][c]=7
    return out
def solve_M30(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        holes=hole_cells_of_component(comp)
        for r,c in holes:
            out[r][c]=comp["color"]
    return out
def solve_M31(g):
    h,w=dims(g)
    markers=[]
    obj_grid=blank(h,w)
    objects=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in {1,2,3,4,6,7,8,9} and (all(g[r+dr][c+dc]==0 if 0<=r+dr<h and 0<=c+dc<w else True for dr,dc in DIR4)) and v!=5:
                # singleton maybe marker
                pass
    # simpler: markers are colors 1-4, objects color 5
    markers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in {1,2,3,4}]
    comps=components(g, colors={5})
    out=clone(g)
    for comp in comps:
        best=min(markers, key=lambda m: min(manhattan((r,c),(m[0],m[1])) for r,c in comp["cells"]))
        for r,c in comp["cells"]:
            out[r][c]=best[2]
    return out
def solve_M32(g):
    comps=components(g)
    # exclude background; order by top-left bbox
    comps=sorted(comps, key=lambda comp: (comp["bbox"][0], comp["bbox"][1]))
    rendered=[]
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        cells=comp["cells"]
        rr=blank(r1-r0+1,c1-c0+1)
        for r,c in cells:
            rr[r-r0][c-c0]=comp["color"]
        rendered.append(rr)
    height=max(len(x) for x in rendered)
    width=sum(len(x[0]) for x in rendered)+(len(rendered)-1 if len(rendered)>1 else 0)
    out=blank(height,width)
    col=0
    for idx,rg in enumerate(rendered):
        for r,row in enumerate(rg):
            for c,v in enumerate(row):
                out[r][col+c]=v
        col += len(rg[0]) + 1
    return out
def solve_M33(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        clo=rowcol_closure(comp["cells"])
        for r,c in clo:
            out[r][c]=comp["color"]
    return out
def solve_M34(g):
    h,w=dims(g)
    # largest 5-component is template
    template_comp=max(components(g, colors={5}), key=lambda comp: len(comp["cells"]))
    norm=normalize_cells(template_comp["cells"])
    out=blank(h,w)
    anchors=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in {1,2,3,4,6,7,8,9}]
    for ar,ac,color in anchors:
        for dr,dc in norm:
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=color
    return out
def solve_M35(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        trans=transpose_in_bbox(comp["cells"])
        for r,c in trans:
            out[r][c]=comp["color"]
    return out
def solve_H29(g):
    h,w=dims(g)
    marker=None
    for r in range(h):
        for c in range(w):
            if g[r][c] in DIR_MARKER:
                marker=(r,c,g[r][c]); break
        if marker: break
    dr,dc=DIR_MARKER[marker[2]]
    comps=[comp for comp in components(g) if not (len(comp["cells"])==1 and comp["cells"][0]==(marker[0],marker[1])) and comp["color"] not in DIR_MARKER]
    def key(comp):
        r0,c0,r1,c1=comp["bbox"]
        if (dr,dc)==(1,0): return -r1
        if (dr,dc)==(-1,0): return r0
        if (dr,dc)==(0,1): return -c1
        if (dr,dc)==(0,-1): return c0
    comps=sorted(comps, key=key)
    out=blank(h,w)
    out[marker[0]][marker[1]]=marker[2]
    occupied={(marker[0],marker[1])}
    for comp in comps:
        slid=slide_component(set(comp["cells"]), occupied, h,w, dr,dc)
        for r,c in slid:
            out[r][c]=comp["color"]
        occupied |= slid
    return out
def solve_H30(g):
    h,w=dims(g)
    marker=(next((r,c) for r in range(h) for c in range(w) if g[r][c]==2))
    target=None
    for comp in components(g):
        if comp["color"]==2:
            continue
        S=set(comp["cells"])
        if any((marker[0]+dr,marker[1]+dc) in S for dr,dc in DIR4):
            target=comp; break
    out=blank(h,w)
    for r,c in trace_perimeter(target["cells"]):
        out[r][c]=2
    return out
def solve_H31(g):
    h,w=dims(g)
    # legend in bottom 2 rows, first 3 nonzero columns contiguous
    old=[]; new=[]
    cols=[c for c in range(w) if g[h-2][c]!=0 or g[h-1][c]!=0]
    # use sorted unique first 3
    cols=sorted(cols)[:3]
    old=[g[h-2][c] for c in cols]
    new=[g[h-1][c] for c in cols]
    mapping={o:n for o,n in zip(old,new)}
    anchors=[(r,c) for r in range(h-2) for c in range(w) if g[r][c]==9]
    # template = nonzero non-anchor cells excluding bottom 2 rows
    temp_cells=[(r,c,g[r][c]) for r in range(h-2) for c in range(w) if g[r][c] not in (0,9)]
    # Remove legend if somehow above? no.
    # assume template clustered in top-left; use bbox of all temp cells
    # But this includes anchors? excluded. Also copies none.
    # Since bottom 2 rows reserved for legend, this gets just template.
    rs=[r for r,c,v in temp_cells]; cs=[c for r,c,v in temp_cells]
    r0,c0,r1,c1=min(rs),min(cs),max(rs),max(cs)
    template=[(r-r0,c-c0,mapping[v]) for r,c,v in temp_cells]
    out=blank(h,w)
    for ar,ac in anchors:
        for dr,dc,v in template:
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
def solve_H32(g):
    h,w=dims(g)
    seeds=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    cov=raycast_coverage(g, seeds, wall_colors={8})
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if cov[r][c]==2:
                out[r][c]=2
    return out
def solve_H33(g):
    h,w=dims(g)
    seed=next((r,c) for r in range(h) for c in range(w) if g[r][c]==2)
    dist=parity_fill_chamber(g, seed, wall=8)
    out=clone(g)
    for (r,c),d in dist.items():
        if g[r][c]!=8:
            out[r][c]=3 if d%2==0 else 4
    return out
def solve_H34(g):
    h,w=dims(g)
    out=clone(g)
    colors=sorted({g[r][c] for r in range(h) for c in range(w) if g[r][c] not in (0,8)})
    for color in colors:
        pts=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(pts)!=2:
            continue
        # grid for bfs: 0 passable, goal allowed, walls/other endpoints blocked
        path=bfs_path(g, pts[0], pts[1], passable={0})
        if path is None:
            raise ValueError(f"No path for color {color}")
        for r,c in path:
            out[r][c]=color
    return out
def solve_H35(g):
    h,w=dims(g)
    out=clone(g)
    for comp in components(g, colors={8}):
        holes=hole_cells_of_component(comp)
        if not holes:
            continue
        # distance to wall inside hole region: frontier are cells adjacent to non-hole
        dist={}
        current={p for p in holes if any((p[0]+dr,p[1]+dc) not in holes for dr,dc in DIR4)}
        remaining=set(holes)
        d=1
        while current:
            for p in current:
                dist[p]=d
            remaining-=current
            nextset={p for p in remaining if any((p[0]+dr,p[1]+dc) in current for dr,dc in DIR4)}
            current=nextset
            d+=1
        for (r,c),dd in dist.items():
            out[r][c]=2 if dd%2==1 else 3
    return out

SOLVERS = {
    'E29': solve_E29,
    'E30': solve_E30,
    'E31': solve_E31,
    'E32': solve_E32,
    'E33': solve_E33,
    'E34': solve_E34,
    'E35': solve_E35,
    'M29': solve_M29,
    'M30': solve_M30,
    'M31': solve_M31,
    'M32': solve_M32,
    'M33': solve_M33,
    'M34': solve_M34,
    'M35': solve_M35,
    'H29': solve_H29,
    'H30': solve_H30,
    'H31': solve_H31,
    'H32': solve_H32,
    'H33': solve_H33,
    'H34': solve_H34,
    'H35': solve_H35,
}

def solve_by_id(task_id: str, grid: Grid) -> Grid:
    return SOLVERS[task_id](grid)
