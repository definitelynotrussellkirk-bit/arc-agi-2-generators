"""Reference solvers for ARC-style additional puzzle bank volume 14.

This volume continues the denser 4-train-pairs format and leans into
sparse rectangle completion, chamber filling, count-coded frames,
all-shortest-path unions, mirror-beam tracing, and transform-plus-vector stamping.

Helper primitives emphasized here:
- all_shortest_path_union(grid, start, goal)
- trace_mirror_beam(grid, start, direction)
- boundary_majority_color(chamber)
- transform_then_translate(shape, code, vector)
"""
from typing import List, Tuple, Dict, Iterable, Set
from collections import deque, Counter, defaultdict
import itertools

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]


def clone(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g); return 0<=r<h and 0<=c<w


def set_cells(g,cells,color):
    for r,c in cells:
        g[r][c]=color


def component_cells(g, colors=None):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            if colors is None:
                if g[r][c]==0: continue
            else:
                if g[r][c] not in colors: continue
            col=g[r][c]
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==col and (colors is None or g[nr][nc] in colors):
                        seen[nr][nc]=True; dq.append((nr,nc))
            comps.append((col,cells))
    return comps


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
        s={(c, h-1-r) for r,c in s}
        s=set(normalize(s))
    return frozenset(s)


def reflect_h(shape):
    s=set(normalize(shape))
    if not s: return frozenset()
    h=max(r for r,c in s)+1
    return frozenset(normalize([(h-1-r,c) for r,c in s]))


def reflect_v(shape):
    s=set(normalize(shape))
    if not s: return frozenset()
    w=max(c for r,c in s)+1
    return frozenset(normalize([(r,w-1-c) for r,c in s]))


def translate(cells, dr, dc):
    return {(r+dr,c+dc) for r,c in cells}


def render(g):
    return "\n".join("".join(str(x) for x in row) for row in g)


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def find_single_cells(grid, color):
    return [(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==color]


def find_component_of_color(grid, color):
    comps=[cells for col,cells in component_cells(grid,{color}) if col==color]
    return comps[0] if comps else []


def chamber_regions(grid, passable=lambda v:v!=5):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    regs=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or not passable(grid[r][c]): continue
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and passable(grid[nr][nc]):
                        seen[nr][nc]=True; dq.append((nr,nc))
            regs.append(cells)
    return regs


def bfs_dist(grid, starts, blocked={5}):
    h,w=dims(grid)
    INF=10**9
    dist=[[INF]*w for _ in range(h)]
    dq=deque()
    for r,c in starts:
        dist[r][c]=0; dq.append((r,c))
    while dq:
        r,c=dq.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and grid[nr][nc] not in blocked and dist[nr][nc]==INF:
                dist[nr][nc]=dist[r][c]+1
                dq.append((nr,nc))
    return dist


def apply_transform(shape, code):
    s=normalize(shape)
    if code==3: # identity
        return s
    if code==4: # rot90
        return rotate_shape(s,1)
    if code==7: # reflect_h
        return reflect_h(s)
    if code==8: # reflect_v
        return reflect_v(s)
    return s


def solve_E92(grid):
    g=clone(grid)
    ones=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    one_set=set(ones)
    done=set()
    for a,b,c in itertools.combinations(ones,3):
        pts=[a,b,c]
        rs=sorted(set(r for r,_ in pts))
        cs=sorted(set(cc for _,cc in pts))
        if len(rs)==2 and len(cs)==2:
            rect={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}
            if len(rect & one_set)==3:
                miss=list(rect-one_set)
                if len(miss)==1:
                    mr,mc=miss[0]
                    if g[mr][mc]==0:
                        g[mr][mc]=2
    return g


def solve_E93(grid):
    g=clone(grid)
    h,w=dims(g)
    for r in range(h):
        twos=[c for c in range(w) if g[r][c]==2]
        # fill any pair with zeros between and no nonzero between
        for i in range(len(twos)):
            for j in range(i+1,len(twos)):
                c1,c2=twos[i],twos[j]
                if c2-c1>=2 and all(g[r][c]==0 for c in range(c1+1,c2)):
                    for c in range(c1+1,c2):
                        g[r][c]=4
    return g


def solve_E94(grid):
    g=clone(grid)
    h,w=dims(g)
    add=[]
    for r in range(h-2):
        for c in range(w-2):
            ok=True
            for rr in range(r,r+3):
                for cc in range(c,c+3):
                    want = 1 if rr in (r,r+2) or cc in (c,c+2) else 0
                    if g[rr][cc]!=want:
                        ok=False
            if ok:
                add.append((r+1,c+1))
    for r,c in add:
        g[r][c]=8
    return g


def solve_E95(grid):
    return crop_nonzero(grid)


def solve_E96(grid):
    g=clone(grid)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]!=7: continue
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]; borders=set()
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                if rr==0: borders.add('t')
                if rr==h-1: borders.add('b')
                if cc==0: borders.add('l')
                if cc==w-1: borders.add('r')
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==7:
                        seen[nr][nc]=True; dq.append((nr,nc))
            if len(borders)==1:
                for rr,cc in cells:
                    g[rr][cc]=3
    return g


def solve_E97(grid):
    g=clone(grid)
    h,w=dims(g)
    # find full-height divider 5
    divider=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            divider=c; break
    if divider is None:
        return g
    for r in range(h):
        for c in range(divider):
            v=g[r][c]
            if v!=0:
                mc=divider+(divider-c)
                if 0<=mc<w:
                    g[r][mc]=v
    return g


def solve_E98(grid):
    g=clone(grid)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0: continue
            col=g[r][c]
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==col:
                        seen[nr][nc]=True; dq.append((nr,nc))
            comps.append(cells)
    if comps:
        smallest=min(comps,key=lambda cells: len(cells))
        for r,c in smallest:
            g[r][c]=9
    return g


def solve_M92(grid):
    g=clone(grid)
    shape=find_component_of_color(g,2)
    pts8=find_single_cells(g,8); pts9=find_single_cells(g,9)
    if shape and pts8 and pts9:
        (r8,c8),(r9,c9)=pts8[0],pts9[0]
        dr,dc=r9-r8,c9-c8
        for r,c in shape:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc):
                g[nr][nc]=3
    return g


def solve_M93(grid):
    g=clone(grid)
    comps=[cells for col,cells in component_cells(g,{4}) if col==4]
    for cells in comps:
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            cnt=sum(1 for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]==2)
            fill=5+cnt
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    g[r][c]=fill
    return g


def solve_M94(grid):
    g=clone(grid)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==5: continue
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]; seed_colors=set()
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                if g[rr][cc] in {1,2,3}: seed_colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]!=5:
                        seen[nr][nc]=True; dq.append((nr,nc))
            if len(seed_colors)==1:
                color=next(iter(seed_colors))
                for rr,cc in cells:
                    if g[rr][cc]==0:
                        g[rr][cc]=color
    return g


def solve_M95(grid):
    g=clone(grid)
    shape=find_component_of_color(g,6)
    anchors=find_single_cells(g,8)
    ctrls=[v for row in g for v in row if v in {1,2,3,4}]
    if not shape or not anchors or not ctrls:
        return g
    anchor=anchors[0]
    k=ctrls[0]-1
    norm=rotate_shape(shape,k)
    ar,ac=anchor
    for r,c in norm:
        nr,nc=ar+r,ac+c
        if inb(g,nr,nc):
            g[nr][nc]=3
    return g


def solve_M96(grid):
    g=clone(grid)
    pts1=find_single_cells(g,1)
    pts2=find_single_cells(g,2)
    if len(pts1)==2 and len(pts2)==2:
        r01,c01=pts1[0]; r02,c02=pts1[1]
        a_r0,a_r1=sorted([r01,r02]); a_c0,a_c1=sorted([c01,c02])
        r11,c11=pts2[0]; r12,c12=pts2[1]
        b_r0,b_r1=sorted([r11,r12]); b_c0,b_c1=sorted([c11,c12])
        r0=max(a_r0,b_r0); r1=min(a_r1,b_r1)
        c0=max(a_c0,b_c0); c1=min(a_c1,b_c1)
        if r0<=r1 and c0<=c1:
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    g[r][c]=8
    return g


def solve_M97(grid):
    comps=[]
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==0: continue
            col=grid[r][c]
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and grid[nr][nc]==col:
                        seen[nr][nc]=True; dq.append((nr,nc))
            comps.append((col,len(cells)))
    comps.sort(key=lambda x:(-x[1], x[0]))
    return [[col for col,_ in comps]]


def solve_M98(grid):
    g=clone(grid)
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v not in (0,5,6,7,8,9)})  # maybe 1,2,3
    # more general: any color with exactly two cells aligned and zeros between
    positions=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append((r,c))
    for color,pts in positions.items():
        if len(pts)!=2: 
            continue
        (r1,c1),(r2,c2)=pts
        if r1==r2:
            lo,hi=sorted([c1,c2])
            if all(g[r1][c]==0 for c in range(lo+1,hi)):
                for c in range(lo+1,hi):
                    g[r1][c]=color
        elif c1==c2:
            lo,hi=sorted([r1,r2])
            if all(g[r][c1]==0 for r in range(lo+1,hi)):
                for r in range(lo+1,hi):
                    g[r][c1]=color
    return g


def solve_H92(grid):
    g=clone(grid)
    start=find_single_cells(g,2)[0]
    goal=find_single_cells(g,3)[0]
    ds=bfs_dist(g,[start],{5})
    dg=bfs_dist(g,[goal],{5})
    d=ds[goal[0]][goal[1]]
    h,w=dims(g)
    if d>=10**9: return g
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and ds[r][c]+dg[r][c]==d:
                g[r][c]=8
    return g


def solve_H93(grid):
    g=clone(grid)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v in {1,2,3}]
    dists={color:bfs_dist(g,[(r,c)],{5}) for r,c,color in seeds}
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: continue
            vals=[(dist[r][c], color) for color,dist in dists.items()]
            best=min(d for d,_ in vals)
            if best>=10**9: 
                continue
            colors=[color for d,color in vals if d==best]
            if len(colors)==1:
                g[r][c]=colors[0]
    return g


def solve_H94(grid):
    g=clone(grid)
    # find control 1/2/3
    ctrl=None
    for row in g:
        for v in row:
            if v in {1,2,3}:
                ctrl=v
                break
        if ctrl is not None: break
    comps=[cells for col,cells in component_cells(g,{4}) if col==4]
    frames=[]
    for cells in comps:
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border:
            frames.append(( (r1-r0+1)*(c1-c0+1), (r0,c0,r1,c1) ))
    frames.sort(reverse=True)  # outer to inner by area
    if ctrl is None or not frames: return g
    idx=ctrl-1
    rects=[rc for _,rc in frames]
    h,w=dims(g)
    if idx==0 and len(rects)>=2:
        r0,c0,r1,c1=rects[0]
        ir0,ic0,ir1,ic1=rects[1]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if not (ir0<=r<=ir1 and ic0<=c<=ic1) and g[r][c]==0:
                    g[r][c]=8
    elif idx==1 and len(rects)>=3:
        r0,c0,r1,c1=rects[1]
        ir0,ic0,ir1,ic1=rects[2]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if not (ir0<=r<=ir1 and ic0<=c<=ic1) and g[r][c]==0:
                    g[r][c]=8
    elif idx==2 and len(rects)>=3:
        r0,c0,r1,c1=rects[2]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]==0:
                    g[r][c]=8
    return g


def solve_H95(grid):
    g=clone(grid)
    source=find_single_cells(g,2)
    if not source: return g
    r,c=source[0]
    dr,dc=0,1
    h,w=dims(g)
    rr,cc=r+dr,c+dc
    seen=set()
    while 0<=rr<h and 0<=cc<w and (rr,cc,dr,dc) not in seen:
        seen.add((rr,cc,dr,dc))
        v=g[rr][cc]
        if v==5:
            break
        if v==0:
            g[rr][cc]=8
        elif v==3:  # /
            dr,dc = -dc, -dr  # right->up, down->left, etc
        elif v==4:  # \
            dr,dc = dc, dr  # right->down, up->left, etc
        # source or other colored cells just pass through? we'll preserve and continue
        rr,cc=rr+dr,cc+dc
    return g


def solve_H96(grid):
    g=clone(grid)
    shape=find_component_of_color(g,6)
    pts1=find_single_cells(g,1); pts2=find_single_cells(g,2)
    ctrl=None
    for row in g:
        for v in row:
            if v in {3,4,7,8}:
                ctrl=v; break
        if ctrl is not None: break
    if shape and pts1 and pts2 and ctrl is not None:
        (mr1,mc1),(mr2,mc2)=pts1[0],pts2[0]
        dr,dc=mr2-mr1,mc2-mc1
        r0,c0,r1,c1=bbox(shape)
        tr=apply_transform(shape,ctrl)
        for r,c in tr:
            nr,nc=r0+dr+r, c0+dc+c
            if inb(g,nr,nc):
                g[nr][nc]=9
    return g


def solve_H97(grid):
    g=clone(grid)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]!=0: continue
            dq=deque([(r,c)]); seen[r][c]=True; cells=[]; cnt=Counter()
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if not inb(g,nr,nc): 
                        continue
                    if g[nr][nc]==0 and not seen[nr][nc]:
                        seen[nr][nc]=True; dq.append((nr,nc))
                    elif g[nr][nc] in {1,2,3,4}:
                        cnt[g[nr][nc]] += 1
            if cnt:
                top=cnt.most_common()
                if len(top)==1 or top[0][1] > top[1][1]:
                    color=top[0][0]
                    for rr,cc in cells:
                        g[rr][cc]=color
    return g


def solve_H98(grid):
    g=clone(grid)
    a=find_single_cells(g,1)[0]
    b=find_single_cells(g,2)[0]
    da=bfs_dist(g,[a],{5})
    db=bfs_dist(g,[b],{5})
    h,w=dims(g)
    INF=10**9
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and da[r][c]<INF and da[r][c]==db[r][c]:
                g[r][c]=8
    return g


SOLVERS = {
    "E92": solve_E92,
    "E93": solve_E93,
    "E94": solve_E94,
    "E95": solve_E95,
    "E96": solve_E96,
    "E97": solve_E97,
    "E98": solve_E98,
    "M92": solve_M92,
    "M93": solve_M93,
    "M94": solve_M94,
    "M95": solve_M95,
    "M96": solve_M96,
    "M97": solve_M97,
    "M98": solve_M98,
    "H92": solve_H92,
    "H93": solve_H93,
    "H94": solve_H94,
    "H95": solve_H95,
    "H96": solve_H96,
    "H97": solve_H97,
    "H98": solve_H98,
}

def solve(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
