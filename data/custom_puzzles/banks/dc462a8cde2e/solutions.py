"""Reference solvers for ARC-style additional puzzle bank volume 8.

This volume introduces two especially handy helper primitives:
`run_between(a, b)` for straight closed row/column segments between aligned markers,
and `shortest_path(grid, start, goal, blocked)` for corridor-style path extraction.

The bank also leans into component ranking, chamber flood fills, nested-frame depth,
boolean shape composition, Voronoi regions under walls, and legend-based rotation matching.
"""

from typing import List

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def normalize(cells):
    if not cells: return set()
    r0,c0,r1,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}


def rotate_shape(shape, k=1):
    s=set(shape)
    for _ in range(k%4):
        if not s: return set()
        h=max(r for r,c in s)+1
        s={(c, h-1-r) for r,c in s}
        s=normalize(s)
    return s


def reflect_h(shape):
    s=set(shape)
    if not s: return set()
    w=max(c for r,c in s)+1
    return normalize({(r, w-1-c) for r,c in s})


def components(g, colors=None, bg=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
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
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v,"cells":cells,"bbox":bbox(cells)})
    return out


def hole_count(cells):
    S=set(cells)
    r0,c0,r1,c1=bbox(S)
    outside=set()
    stack=[]
    for r in range(r0, r1+1):
        for c in range(c0, c1+1):
            if r in (r0,r1) or c in (c0,c1):
                if (r,c) not in S and (r,c) not in outside:
                    outside.add((r,c)); stack.append((r,c))
    while stack:
        r,c=stack.pop()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if r0<=nr<=r1 and c0<=nc<=c1 and (nr,nc) not in S and (nr,nc) not in outside:
                outside.add((nr,nc)); stack.append((nr,nc))
    holes={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if (r,c) not in S and (r,c) not in outside}
    count=0
    seen=set()
    for cell in holes:
        if cell in seen: continue
        count+=1
        stack=[cell]; seen.add(cell)
        while stack:
            r,c=stack.pop()
            for dr,dc in DIR4:
                nb=(r+dr,c+dc)
                if nb in holes and nb not in seen:
                    seen.add(nb); stack.append(nb)
    return count


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def line_cells(a,b):
    (r1,c1),(r2,c2)=a,b
    if r1==r2:
        step=1 if c2>=c1 else -1
        return [(r1,c) for c in range(c1,c2+step,step)]
    if c1==c2:
        step=1 if r2>=r1 else -1
        return [(r,c1) for r in range(r1,r2+step,step)]
    raise ValueError("not aligned")


def rectangle_border(a,b):
    (r1,c1),(r2,c2)=a,b
    r0,r1=sorted([r1,r2]); c0,c1=sorted([c1,c2])
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return sorted(cells)


def all_rotations(shape):
    s=normalize(shape)
    outs=[]
    seen=set()
    cur=s
    for k in range(4):
        if tuple(sorted(cur)) not in seen:
            seen.add(tuple(sorted(cur)))
            outs.append(cur)
        cur=rotate_shape(cur,1)
    return outs


def shape_equal_under_rotation(a,b):
    na=normalize(a); nb=normalize(b)
    for r in all_rotations(nb):
        if na==r:
            return True
    return False


def flood_from_seed(g, seed, walls={5}):
    h,w=dims(g)
    stack=[seed]
    seen={seed}
    while stack:
        r,c=stack.pop()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc] not in walls:
                # allow traversal through 0 and the seed color itself (2 maybe)
                if g[nr][nc]==0 or g[nr][nc]==g[seed[0]][seed[1]]:
                    seen.add((nr,nc)); stack.append((nr,nc))
    return seen


def shortest_path_grid(g, start, goal, blocked={5}):
    h,w=dims(g)
    from collections import deque
    q=deque([start])
    prev={start:None}
    while q:
        x=q.popleft()
        if x==goal: break
        r,c=x
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and g[nr][nc] not in blocked:
                prev[(nr,nc)] = x
                q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    path.reverse()
    return path


def transform_by_k(shape, k):
    s=normalize(shape)
    if k==1: return s
    if k==2: return rotate_shape(s,1)
    if k==3: return rotate_shape(s,2)
    if k==4: return reflect_h(s)
    raise ValueError(k)


def is_diag_symmetric(shape):
    s=normalize(shape)
    t=normalize({(c,r) for r,c in s})
    return s==t


def bfs_dist(g, starts, blocked={5}):
    h,w=dims(g)
    from collections import deque
    dist={}
    q=deque()
    for s in starts:
        dist[s]=0; q.append(s)
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in dist and g[nr][nc] not in blocked:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist


run_between = line_cells
shortest_path = shortest_path_grid


def solve_E50(g):
    out=clone(g)
    for comp in components(g, colors={2}):
        if len(comp["cells"])==1:
            r,c=comp["cells"][0]
            out[r][c]=3
    return out


def solve_E51(g):
    out=clone(g)
    h,w=dims(g)
    # rows
    for r in range(h):
        cols=[c for c in range(w) if g[r][c]==1]
        if len(cols)==2:
            c0,c1=sorted(cols)
            if all(g[r][c]==0 for c in range(c0+1,c1)):
                for c in range(c0+1,c1):
                    out[r][c]=3
    # cols
    for c in range(w):
        rows=[r for r in range(h) if g[r][c]==1]
        if len(rows)==2:
            r0,r1=sorted(rows)
            if all(g[r][c]==0 for r in range(r0+1,r1)):
                for r in range(r0+1,r1):
                    out[r][c]=3
    return out


def solve_E52(g):
    out=clone(g)
    for comp in components(g, colors={7}):
        cells=comp["cells"]
        if len(cells)==3:
            r0,c0,r1,c1=comp["bbox"]
            if (r1-r0+1, c1-c0+1)==(2,2):
                for r,c in cells:
                    out[r][c]=8
    return out


def solve_E53(g):
    out=clone(g)
    for comp in components(g, colors={4}):
        cells=comp["cells"]
        if len(cells)!=3: 
            continue
        rs={r for r,c in cells}; cs={c for r,c in cells}
        if len(rs)==1:
            r=next(iter(rs)); cols=sorted(cs)
            if cols[2]-cols[0]==2 and cols==list(range(cols[0],cols[0]+3)):
                for c in [cols[0]-1, cols[-1]+1]:
                    if 0<=c<dims(g)[1] and g[r][c]==0:
                        out[r][c]=8
        elif len(cs)==1:
            c=next(iter(cs)); rows=sorted(rs)
            if rows[2]-rows[0]==2 and rows==list(range(rows[0],rows[0]+3)):
                for r in [rows[0]-1, rows[-1]+1]:
                    if 0<=r<dims(g)[0] and g[r][c]==0:
                        out[r][c]=8
    return out


def solve_E54(g):
    return crop_nonzero(g)


def solve_E55(g):
    out=clone(g)
    h,w=dims(g)
    corners={(0,0),(0,w-1),(h-1,0),(h-1,w-1)}
    for comp in components(g, colors={2}):
        if any(cell in corners for cell in comp["cells"]):
            for r,c in comp["cells"]:
                out[r][c]=3
    return out


def solve_E56(g):
    out=clone(g)
    h,w=dims(g)
    div_rows=[r for r in range(h) if all(v==5 for v in g[r])]
    if not div_rows: return out
    d=div_rows[0]
    for r in range(d):
        for c in range(w):
            if g[r][c]!=0 and g[r][c]!=5:
                rr=2*d-r
                if 0<=rr<h and g[rr][c]==0:
                    out[rr][c]=8
    return out


def solve_M50(g):
    out=clone(g)
    h,w=dims(g)
    r2=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2][0]
    r1=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1][0]
    dr,dc=r1[0]-r2[0], r1[1]-r2[1]
    comps=components(g, colors={4})
    # choose largest 4-comp
    comp=max(comps, key=lambda x: len(x["cells"]))
    for r,c in comp["cells"]:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=8
    return out


def solve_M51(g):
    comps=sorted(components(g, colors={6}), key=lambda x: (-len(x["cells"]), x["bbox"]))
    comp=comps[1]
    r0,c0,r1,c1=comp["bbox"]
    h,w=r1-r0+1,c1-c0+1
    out=blank(h,w,0)
    for r,c in comp["cells"]:
        out[r-r0][c-c0]=2
    return out


def solve_M52(g):
    out=clone(g)
    pos2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    pos1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    if len(pos2)==2:
        for r,c in rectangle_border(pos2[0], pos2[1]):
            out[r][c]=3
    if len(pos1)==2:
        for r,c in rectangle_border(pos1[0], pos1[1]):
            out[r][c]=8
    return out


def solve_M53(g):
    out=clone(g)
    seed=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2][0]
    region=flood_from_seed(g, seed, walls={5})
    for r,c in region:
        if g[r][c]==0:
            out[r][c]=8
    return out


def solve_M54(g):
    out=clone(g)
    h,w=dims(g)
    top_red=[c for c in range(w) if g[0][c]==2]
    left_red=[r for r in range(h) if g[r][0]==2]
    top_blue=[c for c in range(w) if g[0][c]==1]
    left_blue=[r for r in range(h) if g[r][0]==1]
    for r in left_red:
        for c in top_red:
            if r>0 and c>0 and g[r][c]==0:
                out[r][c]=3
    for r in left_blue:
        for c in top_blue:
            if r>0 and c>0 and g[r][c]==0:
                out[r][c]=8
    return out


def solve_M55(g):
    out=clone(g)
    mp={0:2,1:3,2:8}
    for comp in components(g, colors={4}):
        hc=hole_count(comp["cells"])
        if hc in mp:
            for r,c in comp["cells"]:
                out[r][c]=mp[hc]
    return out


def solve_M56(g):
    out=clone(g)
    h,w=dims(g)
    comps=components(g, colors={3})
    template=max(comps, key=lambda x: len(x["cells"]))
    shape=normalize(template["cells"])
    k=sum(1 for r,row in enumerate(g) for c,v in enumerate(row) if v==1)
    anchor=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==7][0]
    tr=transform_by_k(shape,k)
    ar,ac=anchor
    for r,c in tr:
        nr,nc=ar+r, ac+c
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=8
    return out


def solve_H50(g):
    out=clone(g)
    h,w=dims(g)
    start=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2][0]
    goal=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3][0]
    path=shortest_path_grid(g,start,goal,blocked={5})
    if path:
        for r,c in path[1:-1]:
            if g[r][c]==0:
                out[r][c]=8
    return out


def solve_H51(g):
    out=clone(g)
    k=sum(1 for r,row in enumerate(g) for c,v in enumerate(row) if v==1)
    comps=sorted(components(g, colors={4}), key=lambda x: ((x["bbox"][2]-x["bbox"][0]+1)*(x["bbox"][3]-x["bbox"][1]+1)), reverse=True)
    if 1<=k<=len(comps):
        for r,c in comps[k-1]["cells"]:
            out[r][c]=3
    return out


def solve_H52(g):
    comps2=components(g, colors={2})
    comps1=components(g, colors={1})
    shape2=normalize(max(comps2, key=lambda x: len(x["cells"]))["cells"])
    shape1=normalize(max(comps1, key=lambda x: len(x["cells"]))["cells"])
    x=set(shape2)^set(shape1)
    if not x:
        return [[0]]
    r0,c0,r1,c1=bbox(x)
    out=blank(r1-r0+1, c1-c0+1, 0)
    for r,c in x:
        out[r-r0][c-c0]=8
    return out


def solve_H53(g):
    out=clone(g)
    h,w=dims(g)
    target=None
    for comp in components(g, colors={7}):
        if is_diag_symmetric(comp["cells"]):
            target=comp["cells"]; break
    if target:
        S=set(target)
        for r in range(h):
            for c in range(w):
                if (r,c) in S: continue
                d=min(abs(r-r0)+abs(c-c0) for r0,c0 in S)
                if d==1 and g[r][c]==0:
                    out[r][c]=8
    return out


def solve_H54(g):
    out=clone(g)
    h,w=dims(g)
    template=max(components(g, colors={6}), key=lambda x: len(x["cells"]))
    shape=normalize(template["cells"])
    rot=sum(1 for r,row in enumerate(g) for c,v in enumerate(row) if v==1)-1
    ref=sum(1 for r,row in enumerate(g) for c,v in enumerate(row) if v==2)
    s=shape
    if rot:
        s=rotate_shape(s, rot)
    if ref==2:
        s=reflect_h(s)
    anchor=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==7][0]
    ar,ac=anchor
    for r,c in s:
        nr,nc=ar+r, ac+c
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=8
    return out


def solve_H55(g):
    out=clone(g)
    seeds2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    seeds3=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    d2=bfs_dist(g,seeds2,blocked={5})
    d3=bfs_dist(g,seeds3,blocked={5})
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: continue
            a=d2.get((r,c),10**9); b=d3.get((r,c),10**9)
            if a<b:
                out[r][c]=2
            elif b<a:
                out[r][c]=3
    return out


def solve_H56(g):
    out=clone(g)
    h,w=dims(g)
    div=[r for r in range(h) if all(v==5 for v in g[r])][0]
    legend={}
    # extract one component per color above divider
    sub_top=[row[:] for row in g[:div]]
    for color in (2,3,4):
        comps=[comp for comp in components(sub_top, colors={color})]
        legend[color]=normalize(comps[0]["cells"])
    # scene components below divider of color7
    sub=[row[:] for row in g[div+1:]]
    scene=components(sub, colors={7})
    for comp in scene:
        sh=normalize(comp["cells"])
        for color,leg in legend.items():
            if shape_equal_under_rotation(sh, leg):
                for r,c in comp["cells"]:
                    out[div+1+r][c]=color
                break
    return out


SOLVERS = {
    'E50': solve_E50,
    'E51': solve_E51,
    'E52': solve_E52,
    'E53': solve_E53,
    'E54': solve_E54,
    'E55': solve_E55,
    'E56': solve_E56,
    'M50': solve_M50,
    'M51': solve_M51,
    'M52': solve_M52,
    'M53': solve_M53,
    'M54': solve_M54,
    'M55': solve_M55,
    'M56': solve_M56,
    'H50': solve_H50,
    'H51': solve_H51,
    'H52': solve_H52,
    'H53': solve_H53,
    'H54': solve_H54,
    'H55': solve_H55,
    'H56': solve_H56,
}


def solve_by_id(task_id: str, grid: Grid) -> Grid:
    return SOLVERS[task_id](grid)
