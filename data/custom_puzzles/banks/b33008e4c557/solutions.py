"""Reference solvers for ARC-style additional puzzle bank volume 15.

This volume continues the 4-train-pairs format and emphasizes midpoint detection,
segment endpoints, divider reflections, chamber-majority filling, path unions versus
path cores, control-driven transforms, and normalized boolean shape operations.

Helper ideas emphasized here:
- component_endpoints(cells)
- path_union(grid, start, goal)
- mandatory_path_core(grid, start, goal)
- normalize_xor(shape_a, shape_b)
"""
from typing import List, Tuple, Dict, Iterable, Set
from collections import deque, Counter, defaultdict
import itertools

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w


def set_cells(g,cells,color):
    for r,c in cells:
        g[r][c]=color


def bbox(cells):
    cells=list(cells)
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def normalize(cells):
    cells=list(cells)
    if not cells:
        return frozenset()
    r0,c0,r1,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)


def rotate_shape(shape,k=1):
    s=set(normalize(shape))
    for _ in range(k%4):
        if not s:
            return frozenset()
        h=max(r for r,c in s)+1
        s={(c,h-1-r) for r,c in s}
        s=set(normalize(s))
    return frozenset(s)


def reflect_h(shape):
    s=set(normalize(shape))
    if not s:
        return frozenset()
    h=max(r for r,c in s)+1
    return frozenset(normalize([(h-1-r,c) for r,c in s]))


def reflect_v(shape):
    s=set(normalize(shape))
    if not s:
        return frozenset()
    w=max(c for r,c in s)+1
    return frozenset(normalize([(r,w-1-c) for r,c in s]))


def all_dihedral(shape):
    s=set(normalize(shape))
    outs=set()
    cur=frozenset(s)
    for k in range(4):
        rot=rotate_shape(cur,k)
        outs.add(rot)
        outs.add(reflect_h(rot))
    return outs


def translate(cells,dr,dc):
    return {(r+dr,c+dc) for r,c in cells}


def component_cells(g, colors=None, connectivity=4):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    dirs=DIR4 if connectivity==4 else DIR4+[(-1,-1),(-1,1),(1,-1),(1,1)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            v=g[r][c]
            if colors is None:
                if v==0:
                    continue
            else:
                if v not in colors:
                    continue
            seen[r][c]=True
            dq=deque([(r,c)]); cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==v and (colors is None or g[nr][nc] in colors):
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            comps.append((v,cells))
    return comps


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def render(grid):
    return "\n".join("".join(str(x) for x in row) for row in grid)


def find_cells(g,color):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]


def bfs_dist(g, starts, blocked={5}):
    h,w=dims(g)
    INF=10**9
    dist=[[INF]*w for _ in range(h)]
    dq=deque()
    for s in starts:
        r,c=s
        dist[r][c]=0
        dq.append((r,c))
    while dq:
        r,c=dq.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and g[nr][nc] not in blocked and dist[nr][nc]==INF:
                dist[nr][nc]=dist[r][c]+1
                dq.append((nr,nc))
    return dist


def chamber_cells(g, wall=5):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    ch=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==wall:
                continue
            seen[r][c]=True
            dq=deque([(r,c)]); cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]!=wall:
                        seen[nr][nc]=True; dq.append((nr,nc))
            ch.append(cells)
    return ch


def outline_rect(cells):
    r0,c0,r1,c1=bbox(cells)
    return {(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}


def fill_rect(r0,c0,r1,c1):
    return {(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)}


def detect_frames(g,color=6):
    frames=[]
    for v,cells in component_cells(g,{color}):
        r0,c0,r1,c1=bbox(cells)
        if set(cells)==outline_rect(cells):
            frames.append((r0,c0,r1,c1,cells))
    return frames


def trace_beam(grid, start, direction):
    # direction tuple dr,dc; mirrors 3='/',4='\\', wall 5
    dr,dc=direction
    r,c=start
    visited_states=set()
    trail=[]
    h,w=dims(grid)
    while True:
        nr,nc=r+dr,c+dc
        if not (0<=nr<h and 0<=nc<w):
            break
        if (nr,nc,dr,dc) in visited_states:
            break
        visited_states.add((nr,nc,dr,dc))
        cell=grid[nr][nc]
        if cell==5:
            break
        if cell==0:
            trail.append((nr,nc))
        if cell==3:  # '/'
            dr,dc = -dc,-dr
        elif cell==4:  # '\'
            dr,dc = dc,dr
        r,c=nr,nc
    return trail


def shortest_path_counts(grid, s, t, blocked={5}):
    ds=bfs_dist(grid,[s],blocked); dt=bfs_dist(grid,[t],blocked)
    D=ds[t[0]][t[1]]
    h,w=dims(grid)
    # count shortest paths from s
    cells=[(r,c) for r in range(h) for c in range(w) if ds[r][c]<10**9 and ds[r][c]+dt[r][c]==D]
    cells.sort(key=lambda rc: ds[rc[0]][rc[1]])
    cs=defaultdict(int); cs[s]=1
    for r,c in cells:
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and ds[nr][nc]==ds[r][c]+1 and ds[nr][nc]+dt[nr][nc]==D and grid[nr][nc] not in blocked:
                cs[(nr,nc)] += cs[(r,c)]
    ct=defaultdict(int); ct[t]=1
    for r,c in sorted(cells, key=lambda rc: dt[rc[0]][rc[1]]):
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and dt[nr][nc]==dt[r][c]+1 and ds[nr][nc]+dt[nr][nc]==D and grid[nr][nc] not in blocked:
                ct[(nr,nc)] += ct[(r,c)]
    return ds,dt,D,cs,ct


def transform_shape(shape, code):
    s=frozenset(normalize(shape))
    if code=='I':
        return s
    if code=='R1':
        return rotate_shape(s,1)
    if code=='R2':
        return rotate_shape(s,2)
    if code=='FH':
        return reflect_h(s)
    raise ValueError(code)


def render_shape(shape,color=8):
    if not shape:
        return [[0]]
    r1=max(r for r,c in shape); c1=max(c for r,c in shape)
    g=blank(r1+1,c1+1,0)
    for r,c in shape:
        g[r][c]=color
    return g


ROT_MAP_M99 = {1:0, 2:1, 4:2, 6:3}
CTRL_H103 = {2:'I', 3:'R1', 4:'FH', 6:'R2'}

def solve_E99(grid):
    g=clone(grid)
    cells=find_cells(g,1)
    for (r1,c1),(r2,c2) in itertools.combinations(cells,2):
        if r1==r2 and abs(c1-c2)%2==0 and abs(c1-c2)>=2:
            mid=(r1,(c1+c2)//2)
            g[mid[0]][mid[1]]=2
            return g
        if c1==c2 and abs(r1-r2)%2==0 and abs(r1-r2)>=2:
            mid=((r1+r2)//2,c1)
            g[mid[0]][mid[1]]=2
            return g
    return g


def solve_E100(grid):
    g=clone(grid)
    for v,cells in component_cells(grid,{2}):
        r0,c0,r1,c1=bbox(cells)
        if r0==r1 and len(cells)>=3:
            cs=sorted(c for r,c in cells)
            g[r0][cs[0]]=4
            g[r0][cs[-1]]=4
        elif c0==c1 and len(cells)>=3:
            rs=sorted(r for r,c in cells)
            g[rs[0]][c0]=4
            g[rs[-1]][c0]=4
    return g


def solve_E101(grid):
    g=clone(grid)
    comps=component_cells(grid,{3})
    for v,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        box=fill_rect(r0,c0,r1,c1)
        missing=[(r,c) for r,c in box if grid[r][c]==0]
        if len(missing)==1 and len(cells)==len(box)-1:
            r,c=missing[0]
            g[r][c]=8
    return g


def solve_E102(grid):
    g=clone(grid)
    h,w=dims(g)
    div_row=None; div_col=None
    for r in range(h):
        if all(g[r][c]==5 for c in range(w)):
            div_row=r; break
    if div_row is None:
        for c in range(w):
            if all(g[r][c]==5 for r in range(h)):
                div_col=c; break
    cells=find_cells(g,7)
    if div_row is not None:
        for r,c in cells:
            rr=2*div_row-r
            if inb(g,rr,c) and g[rr][c]==0:
                g[rr][c]=1
    else:
        for r,c in cells:
            cc=2*div_col-c
            if inb(g,r,cc) and g[r][cc]==0:
                g[r][cc]=1
    return g


def solve_E103(grid):
    g=clone(grid)
    cells=find_cells(g,6)
    for (r1,c1),(r2,c2) in itertools.combinations(cells,2):
        if r1==r2:
            for c in range(min(c1,c2)+1,max(c1,c2)):
                if g[r1][c]==0:
                    g[r1][c]=8
            return g
        if c1==c2:
            for r in range(min(r1,r2)+1,max(r1,r2)):
                if g[r][c1]==0:
                    g[r][c1]=8
            return g
    return g


def solve_E104(grid):
    return crop_nonzero(grid)


def solve_E105(grid):
    g=clone(grid)
    for v,cells in component_cells(grid,{1}):
        h,w=dims(grid)
        touches=set()
        for r,c in cells:
            if r==0: touches.add('T')
            if r==h-1: touches.add('B')
            if c==0: touches.add('L')
            if c==w-1: touches.add('R')
        if len(touches)==1:
            for r,c in cells:
                g[r][c]=2
    return g


def solve_M99(grid):
    g=clone(grid)
    control=None
    for col in ROT_MAP_M99:
        pos=find_cells(g,col)
        if len(pos)==1:
            control=col; break
    k=ROT_MAP_M99[control]
    template=max(component_cells(grid,{3}), key=lambda x: len(x[1]))[1]
    shape=rotate_shape(template,k)
    frames=detect_frames(grid,5)
    # choose largest frame
    r0,c0,r1,c1,_=max(frames, key=lambda x: (x[2]-x[0])*(x[3]-x[1]))
    for r,c in shape:
        rr,cc=r0+1+r, c0+1+c
        if inb(g,rr,cc) and g[rr][cc]==0:
            g[rr][cc]=8
    return g


def solve_M100(grid):
    g=clone(grid)
    h,w=dims(g)
    rows=[r for r in range(1,h) if g[r][0]==1]
    cols=[c for c in range(1,w) if g[0][c]==2]
    for r in rows:
        for c in cols:
            if g[r][c]==0:
                g[r][c]=3
    return g


def solve_M101(grid):
    g=clone(grid)
    for v,cells in component_cells(grid,{7}):
        h,w=dims(grid)
        top=any(r==0 for r,c in cells)
        left=any(c==0 for r,c in cells)
        if top and left:
            for r,c in cells:
                g[r][c]=8
    return g


def solve_M102(grid):
    g=clone(grid)
    pts=find_cells(g,3)
    if len(pts)!=2:
        return g
    (r1,c1),(r2,c2)=pts
    r0,r1b=sorted([r1,r2]); c0,c1b=sorted([c1,c2])
    for r in range(r0,r1b+1):
        for c in range(c0,c1b+1):
            if r in (r0,r1b) or c in (c0,c1b):
                if g[r][c]==0:
                    g[r][c]=8
    return g


def solve_M103(grid):
    g=clone(grid)
    template=max(component_cells(grid,{1}), key=lambda x: len(x[1]))[1]
    a=find_cells(g,2)[0]
    b=find_cells(g,3)[0]
    c=find_cells(g,4)[0]
    d=find_cells(g,6)[0]
    dr=(b[0]-a[0])+(d[0]-c[0])
    dc=(b[1]-a[1])+(d[1]-c[1])
    for r,c in template:
        rr,cc=r+dr, c+dc
        if inb(g,rr,cc) and g[rr][cc]==0:
            g[rr][cc]=8
    return g


def solve_M104(grid):
    g=clone(grid)
    best=None
    for cells in chamber_cells(grid,5):
        seed_cells=[(r,c) for r,c in cells if grid[r][c] not in (0,5)]
        if not seed_cells:
            continue
        colors=[grid[r][c] for r,c in seed_cells]
        cnt=Counter(colors)
        top=cnt.most_common()
        # assume unique max count and majority
        score=(len(seed_cells), top[0][1], -top[0][0])  # more seeds, stronger majority, smaller color as last tiebreak invert?
        if best is None or score>best[0]:
            best=(score,cells,top[0][0])
    if best:
        _,cells,color=best
        for r,c in cells:
            if g[r][c]==0:
                g[r][c]=color
    return g


def solve_M105(grid):
    g=clone(grid)
    ref=max(component_cells(grid,{1}), key=lambda x: len(x[1]))[1]
    forms=all_dihedral(ref)
    for v,cells in component_cells(grid,{2}):
        if normalize(cells) in forms:
            for r,c in cells:
                g[r][c]=8
    return g


def solve_H99(grid):
    g=clone(grid)
    s=find_cells(g,1)[0]; t=find_cells(g,2)[0]
    ds=bfs_dist(grid,[s],{5}); dt=bfs_dist(grid,[t],{5})
    D=ds[t[0]][t[1]]
    h,w=dims(g)
    INF=10**9
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and ds[r][c]<INF and dt[r][c]<INF and ds[r][c]+dt[r][c]==D:
                g[r][c]=8
    return g


def solve_H100(grid):
    g=clone(grid)
    s=find_cells(g,1)[0]
    trail=trace_beam(grid,s,(0,1))
    for r,c in trail:
        g[r][c]=8
    return g


def solve_H101(grid):
    g=clone(grid)
    control=None
    for col in (1,2,3):
        pos=find_cells(g,col)
        if len(pos)==1:
            control=col; break
    k=control-1
    frames=sorted(detect_frames(grid,6), key=lambda x: (x[2]-x[0],x[3]-x[1]), reverse=True)
    if not frames:
        return g
    r0,c0,r1,c1,_=frames[k]
    inner=frames[k+1] if k+1 < len(frames) else None
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            inside_inner = inner is not None and inner[0] < r < inner[2] and inner[1] < c < inner[3]
            if not inside_inner and g[r][c]==0:
                g[r][c]=8
    return g


def solve_H102(grid):
    g=clone(grid)
    s=find_cells(g,1)[0]; t=find_cells(g,2)[0]
    ds,dt,D,cs,ct=shortest_path_counts(grid,s,t,{5})
    total=cs[t]
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and ds[r][c]+dt[r][c]==D and cs[(r,c)]*ct[(r,c)]==total:
                g[r][c]=8
    return g


def solve_H103(grid):
    g=clone(grid)
    template=max(component_cells(grid,{1}), key=lambda x: len(x[1]))[1]
    control=None
    for col in CTRL_H103:
        pos=find_cells(g,col)
        if len(pos)==1:
            control=col; break
    code=CTRL_H103[control]
    start=find_cells(g,7)[0]; end=find_cells(g,9)[0]
    dr,dc=end[0]-start[0], end[1]-start[1]
    shape=transform_shape(template, code)
    r0,c0,_,_=bbox(template)
    # place transformed shape translated relative to normalized anchor from template bbox top-left
    for r,c in shape:
        rr,cc=r0+dr+r, c0+dc+c
        if inb(g,rr,cc) and g[rr][cc]==0:
            g[rr][cc]=8
    return g


def solve_H104(grid):
    g=clone(grid)
    comps=[cells for v,cells in component_cells(grid,{3})]
    classes=defaultdict(list)
    for cells in comps:
        canon=min(all_dihedral(cells), key=lambda s: (len(s), sorted(s)))
        classes[canon].append(cells)
    odd=None
    for canon, lst in classes.items():
        if len(lst)==1:
            odd=lst[0]
            break
    if odd:
        for r,c in odd:
            g[r][c]=8
    return g


def solve_H105(grid):
    comps1=[cells for v,cells in component_cells(grid,{1})]
    comps2=[cells for v,cells in component_cells(grid,{2})]
    s1=normalize(max(comps1,key=len))
    s2=normalize(max(comps2,key=len))
    xor=set(s1)^set(s2)
    return render_shape(normalize(xor),8)


SOLVERS = {
    'E99': solve_E99,
    'E100': solve_E100,
    'E101': solve_E101,
    'E102': solve_E102,
    'E103': solve_E103,
    'E104': solve_E104,
    'E105': solve_E105,
    'M99': solve_M99,
    'M100': solve_M100,
    'M101': solve_M101,
    'M102': solve_M102,
    'M103': solve_M103,
    'M104': solve_M104,
    'M105': solve_M105,
    'H99': solve_H99,
    'H100': solve_H100,
    'H101': solve_H101,
    'H102': solve_H102,
    'H103': solve_H103,
    'H104': solve_H104,
    'H105': solve_H105,
}

def solve(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
