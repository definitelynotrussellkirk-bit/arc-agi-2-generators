"""Reference solvers for ARC-style additional puzzle bank volume 20.

This volume keeps the 4-train-pairs format and emphasizes segment midpoints,
single-gap completion, border-touch selection, triomino classification,
divider reflections, vector copying, symmetry completion, multi-class geometry
recoloring, row/column Cartesian products, marker-driven frame fills,
size-sorted packing, nearest-object cropping, wall-distance ties,
shortest-path unions, nested-frame band selection, normalized boolean shape
operations, wall-constrained Voronoi filling, transform-controlled repeat
stamping, and chamber voting.

Helper ideas emphasized here:
- segment_midpoint
- single_gap_span
- mirror_completion
- normalize_shape
- frame_band
- voronoi_fill
- repeat_stamp
- chamber_vote
"""
from __future__ import annotations
from typing import List, Tuple, Iterable, Dict, Set
from collections import deque

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = DIR4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def inb(g,r,c):
    return 0<=r<len(g) and 0<=c<len(g[0])

def paint(g,cells,color):
    for r,c in cells:
        if inb(g,r,c): g[r][c]=color

def find_cells(g,color):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]

def bbox(cells):
    cells=list(cells)
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    cells=list(cells)
    if not cells: return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def crop_cells(cells, color=8):
    cells=list(cells)
    if not cells: return [[0]]
    n=normalize(cells)
    rmax=max(r for r,c in n); cmax=max(c for r,c in n)
    g=blank(rmax+1,cmax+1,0)
    paint(g,n,color)
    return g

def components(g,color,dirs=DIR4):
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=color or (r,c) in seen: continue
            q=[(r,c)]; seen.add((r,c)); comp=[]
            while q:
                cr,cc=q.pop(); comp.append((cr,cc))
                for dr,dc in dirs:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and g[nr][nc]==color and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            out.append(sorted(comp))
    return out

def translate(cells,dr,dc): return sorted((r+dr,c+dc) for r,c in cells)

def is_line(comp):
    rs={r for r,c in comp}; cs={c for r,c in comp}
    if len(rs)==1:
        xs=sorted(c for r,c in comp)
        return xs==list(range(min(xs),max(xs)+1)), 'h'
    if len(cs)==1:
        ys=sorted(r for r,c in comp)
        return ys==list(range(min(ys),max(ys)+1)), 'v'
    return False, None

def rectangle_border(box):
    r0,c0,r1,c1=box
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return sorted(cells)

def rectangle_interior(box):
    r0,c0,r1,c1=box
    return [(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]

def is_hollow_rect(comp):
    comp=sorted(comp)
    if not comp: return False
    r0,c0,r1,c1=bbox(comp)
    return r1-r0>=2 and c1-c0>=2 and comp==rectangle_border((r0,c0,r1,c1))

def is_filled_rect(comp):
    comp=list(comp)
    r0,c0,r1,c1=bbox(comp)
    return len(comp)==(r1-r0+1)*(c1-c0+1)

def rot90(cells):
    n=normalize(cells)
    if not n: return []
    rmax=max(r for r,c in n)
    return normalize((c, rmax-r) for r,c in n)

def rot180(cells): return rot90(rot90(cells))

def rot270(cells): return rot90(rot180(cells))

def flip_h(cells):
    n=normalize(cells)
    if not n: return []
    rmax=max(r for r,c in n)
    return normalize((rmax-r,c) for r,c in n)

def flip_v(cells):
    n=normalize(cells)
    if not n: return []
    cmax=max(c for r,c in n)
    return normalize((r,cmax-c) for r,c in n)

def apply_dihedral(cells, code:int):
    # 0 id,1 r90,2 r180,3 r270,4 fh,5 fv,6 diag(main),7 anti
    n=normalize(cells)
    if code==0: return n
    if code==1: return rot90(n)
    if code==2: return rot180(n)
    if code==3: return rot270(n)
    if code==4: return flip_h(n)
    if code==5: return flip_v(n)
    if code==6:
        # transpose
        n=normalize(n)
        return normalize((c,r) for r,c in n)
    if code==7:
        n=normalize(n)
        rmax=max(r for r,c in n); cmax=max(c for r,c in n)
        # reflect across anti diagonal within bbox? For square maybe.
        s=max(rmax,cmax)
        return normalize((s-c,s-r) for r,c in n)
    raise ValueError

def bfs_dist(g, start, blocked={5}):
    q=deque([start]); dist={start:0}
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and g[nr][nc] not in blocked and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)]+1
                q.append((nr,nc))
    return dist

def shortest_path_cells(g, a, b, blocked={5}):
    da=bfs_dist(g,a,blocked); db=bfs_dist(g,b,blocked)
    if b not in da: return set()
    L=da[b]
    return {p for p in da if p in db and da[p]+db[p]==L}

def chamber_components(g, passable=None):
    if passable is None: passable={0,2,3}
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c] not in passable or (r,c) in seen: continue
            q=[(r,c)]; seen.add((r,c)); comp=[]
            while q:
                cr,cc=q.pop(); comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and g[nr][nc] in passable and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            out.append(sorted(comp))
    return out

def solve_E134(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1):
        ok,orient=is_line(comp)
        if ok and orient=='h' and len(comp)%2==1:
            r=comp[0][0]
            cs=sorted(c for _,c in comp)
            mid=(cs[0]+cs[-1])//2
            g[r][mid]=2
    return g

def solve_E135(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(grid)
    # rows
    for r in range(h):
        pos=[c for c in range(w) if grid[r][c]==2]
        if len(pos)>=2:
            a,b=min(pos),max(pos)
            span=[grid[r][c] for c in range(a,b+1)]
            if all(v in (0,2) for v in span) and span.count(0)==1 and span.count(2)>=2:
                for c in range(a,b+1):
                    if g[r][c]==0: g[r][c]=2
    # cols
    for c in range(w):
        pos=[r for r in range(h) if grid[r][c]==2]
        if len(pos)>=2:
            a,b=min(pos),max(pos)
            span=[grid[r][c] for r in range(a,b+1)]
            if all(v in (0,2) for v in span) and span.count(0)==1 and span.count(2)>=2:
                for r in range(a,b+1):
                    if g[r][c]==0: g[r][c]=2
    return g

def solve_E136(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(grid)
    for comp in components(grid,1):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp):
            paint(g,comp,2)
    return g

def solve_E137(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,3):
        if len(comp)==3:
            r0,c0,r1,c1=bbox(comp)
            if r1-r0==1 and c1-c0==1:
                paint(g,comp,4)
    return g

def solve_E138(grid:Grid)->Grid:
    h,w=dims(grid)
    g=clone(grid)
    # find divider line color 8
    axis=None; kind=None
    for c in range(w):
        if all(grid[r][c]==8 for r in range(h)):
            axis=c; kind='v'; break
    if axis is None:
        for r in range(h):
            if all(grid[r][c]==8 for c in range(w)):
                axis=r; kind='h'; break
    if axis is None: return g
    cells=find_cells(grid,6)
    if kind=='v':
        refl=[(r,2*axis-c) for r,c in cells if c!=axis]
    else:
        refl=[(2*axis-r,c) for r,c in cells if r!=axis]
    paint(g,refl,6)
    return g

def solve_E139(grid:Grid)->Grid:
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    if not cells: return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in grid[r0:r1+1]]

def solve_E140(grid:Grid)->Grid:
    comps=components(grid,2)
    if not comps: return clone(grid)
    # unique largest by size, tie break top-left maybe
    comps=sorted(comps,key=lambda comp:(-len(comp), min(comp)))
    largest=comps[0]
    g=clone(grid); paint(g,largest,8); return g

def solve_M134(grid:Grid)->Grid:
    g=clone(grid)
    reds=find_cells(grid,2); greens=find_cells(grid,3)
    if not reds or not greens: return g
    (r2,c2)=reds[0]; (r3,c3)=greens[0]
    dr,dc=r3-r2,c3-c2
    shape=find_cells(grid,1)
    paint(g,[(r+dr,c+dc) for r,c in shape],4)
    return g

def solve_M135(grid:Grid)->Grid:
    h,w=dims(grid)
    g=clone(grid)
    axis=None; kind=None
    for c in range(w):
        if all(grid[r][c]==8 for r in range(h)):
            axis=c; kind='v'; break
    if axis is None:
        for r in range(h):
            if all(grid[r][c]==8 for c in range(w)):
                axis=r; kind='h'; break
    if axis is None: return g
    cells=find_cells(grid,7)
    if kind=='v':
        refl=[(r,2*axis-c) for r,c in cells if c!=axis]
    else:
        refl=[(2*axis-r,c) for r,c in cells if r!=axis]
    paint(g,refl,7)
    return g

def solve_M136(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1):
        r0,c0,r1,c1=bbox(comp)
        ok,orient=is_line(comp)
        if ok and orient=='h':
            paint(g,comp,2)
        elif ok and orient=='v':
            paint(g,comp,3)
        elif is_filled_rect(comp) and (r1-r0)==(c1-c0):
            paint(g,comp,4)
    return g

def solve_M137(grid:Grid)->Grid:
    h,w=dims(grid)
    g=clone(grid)
    rows=[r for r in range(1,h) if grid[r][0]==2]
    cols=[c for c in range(1,w) if grid[0][c]==1]
    for r in rows:
        for c in cols:
            g[r][c]=3
    return g

def solve_M138(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1):
        if is_hollow_rect(comp):
            r0,c0,r1,c1=bbox(comp)
            interior=rectangle_interior((r0,c0,r1,c1))
            markers=[grid[r][c] for r,c in interior if grid[r][c] not in (0,1)]
            if markers:
                color=markers[0]
                for r,c in interior:
                    g[r][c]=color
    return g

def solve_M139(grid:Grid)->Grid:
    h,w=dims(grid)
    # components across all non-zero colors, separate by color
    comps=[]
    seen=set()
    for color in sorted({v for row in grid for v in row if v!=0}):
        for comp in components(grid,color):
            n=normalize(comp)
            rmax=max(r for r,c in n); cmax=max(c for r,c in n)
            comps.append({'color':color,'cells':n,'h':rmax+1,'w':cmax+1,'area':len(comp),'topleft':min(comp)})
    comps=sorted(comps,key=lambda d:(d['area'], d['color'], d['topleft']))
    H=max([d['h'] for d in comps], default=1)
    W=sum(d['w'] for d in comps)+max(0,len(comps)-1)
    out=blank(H,W,0)
    cur=0
    for d in comps:
        paint(out,[(r,c+cur) for r,c in d['cells']], d['color'])
        cur += d['w']+1
    return out

def solve_M140(grid:Grid)->Grid:
    markers=find_cells(grid,2)
    if not markers: return [[0]]
    m=markers[0]
    best=None
    for color in sorted({v for row in grid for v in row if v not in (0,2)}):
        for comp in components(grid,color):
            d=min(abs(r-m[0])+abs(c-m[1]) for r,c in comp)
            key=(d, min(comp), color)
            if best is None or key < best[0]:
                best=(key,color,comp)
    if best is None: return [[0]]
    _, color, comp = best
    return crop_cells(comp, color)

def solve_H134(grid:Grid)->Grid:
    g=clone(grid)
    a=find_cells(grid,2)[0]; b=find_cells(grid,3)[0]
    da=bfs_dist(grid,a,{5}); db=bfs_dist(grid,b,{5})
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==0 and (r,c) in da and (r,c) in db and da[(r,c)]==db[(r,c)]:
                g[r][c]=8
    return g

def solve_H135(grid:Grid)->Grid:
    g=clone(grid)
    s=find_cells(grid,2)[0]; m=find_cells(grid,3)[0]; t=find_cells(grid,4)[0]
    cells=shortest_path_cells(grid,s,m,{5}) | shortest_path_cells(grid,m,t,{5})
    for r,c in cells:
        if g[r][c]==0: g[r][c]=8
    return g

def solve_H136(grid:Grid)->Grid:
    g=clone(grid)
    frames=[]
    for comp in components(grid,1):
        if is_hollow_rect(comp):
            box=bbox(comp)
            frames.append(box)
    if not frames: return g
    frames=sorted(frames, key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)
    k=len(find_cells(grid,2))
    idx=k-1
    if idx<0 or idx>=len(frames)-1: 
        return g
    outer=frames[idx]; inner=frames[idx+1]
    r0,c0,r1,c1=outer
    ir0,ic0,ir1,ic1=inner
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if not (ir0 <= r <= ir1 and ic0 <= c <= ic1) and g[r][c]==0:
                g[r][c]=4
    return g

def solve_H137(grid:Grid)->Grid:
    c3=find_cells(grid,3)
    c4=find_cells(grid,4)
    c6=find_cells(grid,6)
    if c3: op='union'
    elif c4: op='inter'
    elif c6: op='xor'
    else: op='union'
    a=set(normalize(find_cells(grid,1)))
    b=set(normalize(find_cells(grid,2)))
    if op=='union':
        res=a|b
    elif op=='inter':
        res=a&b
    else:
        res=a^b
    return crop_cells(sorted(res), 8)

def solve_H138(grid:Grid)->Grid:
    g=clone(grid)
    a=find_cells(grid,2)[0]; b=find_cells(grid,3)[0]
    da=bfs_dist(grid,a,{5}); db=bfs_dist(grid,b,{5})
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==0 and (r,c) in da and (r,c) in db:
                if da[(r,c)]<db[(r,c)]:
                    g[r][c]=2
                elif db[(r,c)]<da[(r,c)]:
                    g[r][c]=3
                else:
                    g[r][c]=8
    return g

def solve_H139(grid:Grid)->Grid:
    h,w=dims(grid)
    shape=find_cells(grid,1)
    start=find_cells(grid,2)[0]
    nxt=find_cells(grid,3)[0]
    ctrl=None
    for color in [4,6,7]:
        pts=find_cells(grid,color)
        if pts:
            ctrl=color; break
    code_map={4:0,6:1,7:4}  # id, rot90, flip_h
    cells=apply_dihedral(shape, code_map.get(ctrl,0))
    dr,dc=nxt[0]-start[0], nxt[1]-start[1]
    out=blank(h,w,0)
    cur_r,cur_c=start
    while True:
        placed=[(cur_r+r, cur_c+c) for r,c in cells]
        if all(0<=r<h and 0<=c<w for r,c in placed):
            paint(out,placed,8)
            cur_r += dr; cur_c += dc
        else:
            break
    return out

def solve_H140(grid:Grid)->Grid:
    g=clone(grid)
    for comp in chamber_components(grid,{0,2,3}):
        cnt2=sum(1 for r,c in comp if grid[r][c]==2)
        cnt3=sum(1 for r,c in comp if grid[r][c]==3)
        if cnt2>cnt3: fill=2
        elif cnt3>cnt2: fill=3
        else: fill=8
        for r,c in comp:
            if grid[r][c]==0:
                g[r][c]=fill
    return g

SOLVERS = {
    'E134': solve_E134,
    'E135': solve_E135,
    'E136': solve_E136,
    'E137': solve_E137,
    'E138': solve_E138,
    'E139': solve_E139,
    'E140': solve_E140,
    'M134': solve_M134,
    'M135': solve_M135,
    'M136': solve_M136,
    'M137': solve_M137,
    'M138': solve_M138,
    'M139': solve_M139,
    'M140': solve_M140,
    'H134': solve_H134,
    'H135': solve_H135,
    'H136': solve_H136,
    'H137': solve_H137,
    'H138': solve_H138,
    'H139': solve_H139,
    'H140': solve_H140,
}
