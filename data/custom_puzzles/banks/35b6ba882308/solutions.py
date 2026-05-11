"""Reference solvers for ARC-style additional puzzle bank volume 17.

This volume keeps the 4-train-pairs format and emphasizes marker spans,
rectangle completion, divider reflections, chamber fills, mirror-beam tracing,
nested-frame band selection, and transform-plus-translation tasks.

Helper ideas emphasized here:
- span_between_markers
- mirror_across_divider
- beam_trace
- band_from_nested_frames
- normalized_exactly_two
- maze_voronoi_partition
"""
from __future__ import annotations
from typing import List, Tuple, Dict, Iterable, Set
from collections import deque

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR8 = DIR4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def blank(h:int,w:int,v:int=0)->Grid:
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def dims(g:Grid):
    return len(g), len(g[0])

def inb(g:Grid,r:int,c:int)->bool:
    h,w=dims(g); return 0<=r<h and 0<=c<w

def paint(g:Grid,cells:Iterable[Cell],color:int):
    for r,c in cells:
        assert inb(g,r,c), (r,c,dims(g))
        g[r][c]=color

def find_cells(g:Grid,color:int)->List[Cell]:
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]

def bbox(cells:Iterable[Cell]):
    cells=list(cells)
    rs=[r for r,_ in cells]; cs=[c for _,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g:Grid, box)->Grid:
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def normalize(cells:Iterable[Cell])->List[Cell]:
    cells=list(cells)
    if not cells: return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def crop_cells(cells:Iterable[Cell], color:int=8)->Grid:
    cells=list(cells)
    if not cells:
        return [[0]]
    norm=normalize(cells)
    rmax=max(r for r,_ in norm); cmax=max(c for _,c in norm)
    g=blank(rmax+1,cmax+1,0)
    paint(g,norm,color)
    return g

def components(g:Grid, color:int, dirs=DIR4)->List[Set[Cell]]:
    h,w=dims(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=color or (r,c) in seen: 
                continue
            comp=set()
            dq=deque([(r,c)]); seen.add((r,c))
            while dq:
                x,y=dq.popleft(); comp.add((x,y))
                for dr,dc in dirs:
                    nx,ny=x+dr,y+dc
                    if 0<=nx<h and 0<=ny<w and g[nx][ny]==color and (nx,ny) not in seen:
                        seen.add((nx,ny)); dq.append((nx,ny))
            out.append(comp)
    return out

def rect_border_cells(r0,c0,r1,c1):
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return cells

def rect_interior_cells(r0,c0,r1,c1):
    return {(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)}

def major_diag(start:Cell, length:int):
    r,c=start
    return [(r+i,c+i) for i in range(length)]

def minor_diag(start:Cell, length:int):
    r,c=start
    return [(r+i,c-i) for i in range(length)]

def line_cells(start:Cell, dr:int, dc:int, length:int):
    r,c=start
    return [(r+dr*i,c+dc*i) for i in range(length)]

def translate(cells:Iterable[Cell], dr:int, dc:int)->List[Cell]:
    return [(r+dr,c+dc) for r,c in cells]

def bfs_dist_open(grid:Grid, start:Cell, blocked:Set[int]={5}) -> Dict[Cell,int]:
    dq=deque([start]); dist={start:0}
    while dq:
        r,c=dq.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and (nr,nc) not in dist and grid[nr][nc] not in blocked:
                dist[(nr,nc)] = dist[(r,c)] + 1
                dq.append((nr,nc))
    return dist

def transform_cells(cells:Iterable[Cell], code:int)->List[Cell]:
    # normalize first
    norm=normalize(cells)
    if not norm:
        return []
    pts=norm
    if code==1:   # identity
        out=pts
    elif code==2: # rot90 cw
        maxr=max(r for r,_ in pts); maxc=max(c for _,c in pts)
        out=[(c, maxr-r) for r,c in pts]
    elif code==3: # rot180
        maxr=max(r for r,_ in pts); maxc=max(c for _,c in pts)
        out=[(maxr-r, maxc-c) for r,c in pts]
    elif code==4: # mirror left-right
        maxc=max(c for _,c in pts)
        out=[(r, maxc-c) for r,c in pts]
    elif code==7: # rot180 for H119 maybe
        maxr=max(r for r,_ in pts); maxc=max(c for _,c in pts)
        out=[(maxr-r, maxc-c) for r,c in pts]
    elif code==9: # mirror top-bottom for H119 maybe
        maxr=max(r for r,_ in pts)
        out=[(maxr-r, c) for r,c in pts]
    else:
        raise ValueError(code)
    return normalize(out)

def nested_frames(grid:Grid, color:int=1):
    comps=components(grid,color,DIR4)
    frames=[]
    for comp in comps:
        r0,c0,r1,c1=bbox(comp)
        if comp==rect_border_cells(r0,c0,r1,c1):
            frames.append((r0,c0,r1,c1))
    frames.sort()  # outermost first due smaller r0/c0
    # Actually sort by area descending? outer first
    frames.sort(key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)
    return frames

def solve_E113(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,2,DIR4):
        rs={r for r,_ in comp}; cs={c for _,c in comp}
        if len(rs)==1 and len(comp)>=2:
            r=next(iter(rs))
            minc=min(c for _,c in comp); maxc=max(c for _,c in comp)
            g[r][minc]=8; g[r][maxc]=8
        elif len(cs)==1 and len(comp)>=2:
            c=next(iter(cs))
            minr=min(r for r,_ in comp); maxr=max(r for r,_ in comp)
            g[minr][c]=8; g[maxr][c]=8
    return g

def solve_E114(grid:Grid)->Grid:
    g=clone(grid)
    pts=find_cells(grid,3)
    rows=sorted(set(r for r,_ in pts)); cols=sorted(set(c for _,c in pts))
    assert len(pts)==3 and len(rows)==2 and len(cols)==2
    allcorners={(rows[0],cols[0]),(rows[0],cols[1]),(rows[1],cols[0]),(rows[1],cols[1])}
    missing=(allcorners-set(pts)).pop()
    g[missing[0]][missing[1]]=4
    return g

def solve_E115(grid:Grid)->Grid:
    g=clone(grid)
    pts=find_cells(grid,2)
    used=set()
    # check all pairs of 2's aligned with zeros between
    for i,a in enumerate(pts):
        for j,b in enumerate(pts):
            if j<=i: continue
            if a[0]==b[0]:
                r=a[0]; c0,c1=sorted([a[1],b[1]])
                cells=[(r,c) for c in range(c0,c1+1)]
                if all(grid[r][c] in (0,2) for c in range(c0,c1+1)) and sum(grid[r][c]==2 for c in range(c0,c1+1))==2:
                    for c in range(c0+1,c1):
                        g[r][c]=8
                    used.add((i,j))
            elif a[1]==b[1]:
                c=a[1]; r0,r1=sorted([a[0],b[0]])
                cells=[(r,c) for r in range(r0,r1+1)]
                if all(grid[r][c] in (0,2) for r in range(r0,r1+1)) and sum(grid[r][c]==2 for r in range(r0,r1+1))==2:
                    for r in range(r0+1,r1):
                        g[r][c]=8
                    used.add((i,j))
    return g

def solve_E116(grid:Grid)->Grid:
    pts=find_cells(grid,6)
    return crop_bbox(grid, bbox(pts))

def solve_E117(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,7,DIR4):
        r0,c0,r1,c1=bbox(comp)
        if comp==rect_border_cells(r0,c0,r1,c1):
            for r,c in rect_interior_cells(r0,c0,r1,c1):
                if g[r][c]==0:
                    g[r][c]=8
    return g

def solve_E118(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1,DIR4):
        rs={r for r,_ in comp}; cs={c for _,c in comp}
        if len(rs)==1:
            color=4
        elif len(cs)==1:
            color=7
        else:
            continue
        for r,c in comp:
            g[r][c]=color
    return g

def solve_E119(grid:Grid)->Grid:
    g=clone(grid)
    seen_mid=set()
    for comp in components(grid,5,DIR8):
        if len(comp)!=3: 
            continue
        rows=sorted(r for r,_ in comp); cols=sorted(c for _,c in comp)
        pts=sorted(comp)
        # major or minor diagonal if three distinct rows and cols and each consecutive diff abs==1
        norm=normalize(comp)
        if norm==[(0,0),(1,1),(2,2)] or norm==[(0,2),(1,1),(2,0)]:
            # middle by median row
            mid=sorted(comp)[1]
            # but sorted by row,col works for these
            if norm==[(0,2),(1,1),(2,0)]:
                mid=sorted(comp)[1]
            g[mid[0]][mid[1]]=4
    return g

def solve_M113(grid:Grid)->Grid:
    g=clone(grid)
    shape=find_cells(grid,2)
    a=find_cells(grid,3)[0]
    b=find_cells(grid,4)[0]
    dr,dc=b[0]-a[0], b[1]-a[1]
    for r,c in translate(shape,dr,dc):
        if inb(g,r,c) and g[r][c]==0:
            g[r][c]=8
        elif inb(g,r,c) and g[r][c] in (3,4):  # if overlaps marker, still color? better avoid in examples
            g[r][c]=8
    return g

def solve_M114(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(grid)
    # divider is full row or full col of 9
    div_row = next((r for r in range(h) if all(grid[r][c]==9 for c in range(w))), None)
    div_col = next((c for c in range(w) if all(grid[r][c]==9 for r in range(h))), None)
    for r,c in find_cells(grid,2):
        if div_col is not None:
            nc = 2*div_col - c
            nr = r
        else:
            nr = 2*div_row - r
            nc = c
        if inb(g,nr,nc) and g[nr][nc]==0:
            g[nr][nc]=8
    return g

def solve_M115(grid:Grid)->Grid:
    g=clone(grid)
    comps=components(grid,2,DIR4)
    comps_sorted=sorted(comps, key=lambda s:(-len(s), min(s)))
    target=comps_sorted[1]
    for r,c in target:
        g[r][c]=8
    return g

def solve_M116(grid:Grid)->Grid:
    g=clone(grid)
    seed=find_cells(grid,2)[0]
    dq=deque([seed]); seen={seed}
    while dq:
        r,c=dq.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and (nr,nc) not in seen and grid[nr][nc]==0:
                seen.add((nr,nc)); dq.append((nr,nc))
    for r,c in seen:
        if g[r][c]==0:
            g[r][c]=8
    return g

def solve_M117(grid:Grid)->Grid:
    s1=set(normalize(find_cells(grid,1)))
    s2=set(normalize(find_cells(grid,2)))
    inter=s1 & s2
    return crop_cells(inter, color=8)

def solve_M118(grid:Grid)->Grid:
    g=clone(grid)
    pts=find_cells(grid,2)
    assert len(pts)==2
    (r0,c0),(r1,c1)=pts
    r0,r1=sorted([r0,r1]); c0,c1=sorted([c0,c1])
    for r,c in rect_border_cells(r0,c0,r1,c1):
        if g[r][c]==0:
            g[r][c]=8
    return g

def solve_M119(grid:Grid)->Grid:
    n=len(components(grid,2,DIR4))
    return [[8 if i%2==0 else 4 for i in range(n)]]

def solve_H113(grid:Grid)->Grid:
    # beam tracing with mirrors
    g=clone(grid)
    src=find_cells(grid,2)[0]
    dr,dc=0,1  # starts right
    r,c=src
    # move from source into next cell
    while True:
        r += dr; c += dc
        if not inb(grid,r,c) or grid[r][c]==5:
            break
        cell=grid[r][c]
        if cell==0:
            g[r][c]=8
        elif cell==3:  # slash /
            # mark mirror? keep 3 unchanged
            dr,dc = {(-1,0):(0,1),(1,0):(0,-1),(0,-1):(1,0),(0,1):(-1,0)}[(dr,dc)]
        elif cell==4:  # backslash \
            dr,dc = {(-1,0):(0,-1),(1,0):(0,1),(0,-1):(-1,0),(0,1):(1,0)}[(dr,dc)]
        else:
            # other colored cells behave as passable? mark only zero cells; continue straight
            pass
    return g

def solve_H114(grid:Grid)->Grid:
    g=clone(grid)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    da=bfs_dist_open(grid,a,blocked={5})
    db=bfs_dist_open(grid,b,blocked={5})
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==0 and (r,c) in da and (r,c) in db and da[(r,c)]==db[(r,c)]:
                g[r][c]=8
    return g

def solve_H115(grid:Grid)->Grid:
    g=clone(grid)
    ctrl_candidates=[cell for color in (1,2,3,4) for cell in find_cells(grid,color)]
    assert len(ctrl_candidates)==1
    ctrl=ctrl_candidates[0]
    code=grid[ctrl[0]][ctrl[1]]
    shape=find_cells(grid,6)
    anchor=find_cells(grid,7)[0]
    trans=transform_cells(shape, code)
    for r,c in trans:
        nr,nc=anchor[0]+r, anchor[1]+c
        if inb(g,nr,nc) and g[nr][nc] not in (6,1,2,3,4):
            g[nr][nc]=8
    return g

def solve_H116(grid:Grid)->Grid:
    g=clone(grid)
    k=len(find_cells(grid,2))
    frames=nested_frames(grid,1)
    frames=sorted(frames, key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)  # outer to inner
    target=frames[k-1]
    inner=frames[k] if k < len(frames) else None
    region=rect_interior_cells(*target)
    if inner:
        ir0,ic0,ir1,ic1=inner
        region={cell for cell in region if not (ir0 <= cell[0] <= ir1 and ic0 <= cell[1] <= ic1)}
    for r,c in region:
        if g[r][c]==0:
            g[r][c]=8
    return g

def solve_H117(grid:Grid)->Grid:
    s1=set(normalize(find_cells(grid,1)))
    s2=set(normalize(find_cells(grid,2)))
    s3=set(normalize(find_cells(grid,3)))
    exact2={cell for cell in s1|s2|s3 if (cell in s1)+(cell in s2)+(cell in s3)==2}
    return crop_cells(exact2, color=8)

def solve_H118(grid:Grid)->Grid:
    # Voronoi labeling under walls: closer to 2 => 8, closer to 3 => 4, ties left 0
    g=clone(grid)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    da=bfs_dist_open(grid,a,blocked={5})
    db=bfs_dist_open(grid,b,blocked={5})
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==0 and (r,c) in da and (r,c) in db:
                if da[(r,c)] < db[(r,c)]:
                    g[r][c]=8
                elif db[(r,c)] < da[(r,c)]:
                    g[r][c]=4
    return g

def solve_H119(grid:Grid)->Grid:
    g=clone(grid)
    shape=find_cells(grid,6)
    p2=find_cells(grid,2)[0]
    p3=find_cells(grid,3)[0]
    vec=(p3[0]-p2[0], p3[1]-p2[1])
    # control code among {1,4,7,9}
    ctrl=None
    for color in (1,4,7,9):
        cells=find_cells(grid,color)
        # exclude markers? 4/7/9 could appear elsewhere? examples controlled
        if cells:
            if color in (2,3,6):
                continue
            # need unique control not part of shape markers
            # if multiple due other objects? examples avoid.
            ctrl=cells[0]; code=color; break
    trans=transform_cells(shape, code if code in (1,4,7,9) else 1)
    # place relative to original shape bbox top-left plus vector
    r0,c0,_,_=bbox(shape)
    for r,c in trans:
        nr,nc=r0+vec[0]+r, c0+vec[1]+c
        if inb(g,nr,nc) and g[nr][nc]==0:
            g[nr][nc]=8
    return g

SOLVERS = {
    'E113': solve_E113,
    'E114': solve_E114,
    'E115': solve_E115,
    'E116': solve_E116,
    'E117': solve_E117,
    'E118': solve_E118,
    'E119': solve_E119,
    'M113': solve_M113,
    'M114': solve_M114,
    'M115': solve_M115,
    'M116': solve_M116,
    'M117': solve_M117,
    'M118': solve_M118,
    'M119': solve_M119,
    'H113': solve_H113,
    'H114': solve_H114,
    'H115': solve_H115,
    'H116': solve_H116,
    'H117': solve_H117,
    'H118': solve_H118,
    'H119': solve_H119,
}

def solve_by_id(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
