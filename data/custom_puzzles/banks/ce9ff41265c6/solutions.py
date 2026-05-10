"""Reference solvers for ARC-style additional puzzle bank volume 12.

This volume leans into shape completion, border signatures, vector copying,
frame selection, rotation-controlled stamping, shortest-path cores,
wall-constrained distance ties, odd-frequency shape grouping,
and chamber parity-majority fills.

Helper primitives emphasized here:
- band_between_frames(frames, k)              # conceptual, used in H78
- mandatory_shortest_path_cells(grid, s, t)   # conceptual, used in H79
- equidistant_cells(grid, a, b, blocked)      # conceptual, used in H82
- dihedral_stamp(shape, anchor, code)         # conceptual, used in H80
"""
from typing import List
from collections import deque, Counter, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
ARROW_DIR = {1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    if not cells:
        return frozenset()
    r0,c0,r1,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def rotate_shape(shape,k=1):
    s=set(shape)
    s=normalize(s)
    for _ in range(k%4):
        if not s:
            return frozenset()
        h=max(r for r,c in s)+1
        s={(c,h-1-r) for r,c in s}
        s=normalize(s)
    return frozenset(s)

def flip_h(shape):
    s=normalize(shape)
    if not s: return frozenset()
    w=max(c for r,c in s)+1
    return normalize({(r,w-1-c) for r,c in s})

def dihedral(shape, code):
    s=normalize(shape)
    if code==1: return s
    if code==2: return rotate_shape(s,1)
    if code==3: return flip_h(s)
    if code==4: return rotate_shape(flip_h(s),1)
    raise ValueError(code)

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
            q=[(r,c)]
            cells=[(r,c)]
            while q:
                rr,cc=q.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v,"cells":cells})
    return out

def border_touch_count(cells,h,w):
    ct=0
    if any(r==0 for r,c in cells): ct+=1
    if any(r==h-1 for r,c in cells): ct+=1
    if any(c==0 for r,c in cells): ct+=1
    if any(c==w-1 for r,c in cells): ct+=1
    return ct

def interior_of_rect(r0,c0,r1,c1):
    return {(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)}

def find_rect_frames(grid, color):
    out=[]
    comps=components(grid, colors={color})
    for comp in comps:
        cells=set(comp["cells"])
        r0,c0,r1,c1=bbox(cells)
        border={(r0,c) for c in range(c0,c1+1)}|{(r1,c) for c in range(c0,c1+1)}|{(r,c0) for r in range(r0,r1+1)}|{(r,c1) for r in range(r0,r1+1)}
        if cells==border and r1-r0>=2 and c1-c0>=2:
            out.append((r0,c0,r1,c1))
    return out

def shortest_paths_info(grid, start, blocked={5}):
    h,w=dims(grid)
    dist=[[None]*w for _ in range(h)]
    count=[[0]*w for _ in range(h)]
    q=deque([start])
    sr,sc=start
    dist[sr][sc]=0
    count[sr][sc]=1
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc] not in blocked:
                nd=dist[r][c]+1
                if dist[nr][nc] is None:
                    dist[nr][nc]=nd
                    count[nr][nc]=count[r][c]
                    q.append((nr,nc))
                elif dist[nr][nc]==nd:
                    count[nr][nc]+=count[r][c]
    return dist,count

def canonical_rot(shape):
    rots=[normalize(rotate_shape(shape,k)) for k in range(4)]
    return min(tuple(sorted(s)) for s in rots)

def solve_E78(grid):
    g=clone(grid)
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        if len(cells)==3:
            r0,c0,r1,c1=bbox(cells)
            if r1-r0==1 and c1-c0==1:
                for r in range(r0,r1+1):
                    for c in range(c0,c1+1):
                        g[r][c]=2
    return g

def solve_E79(grid):
    g=clone(grid)
    for comp in components(grid, colors={4}):
        cells=comp["cells"]
        if len(cells)==8:
            r0,c0,r1,c1=bbox(cells)
            if r1-r0==2 and c1-c0==2:
                border={(r0,c) for c in range(c0,c1+1)}|{(r1,c) for c in range(c0,c1+1)}|{(r,c0) for r in range(r0,r1+1)}|{(r,c1) for r in range(r0,r1+1)}
                if set(cells)==border:
                    g[r0+1][c0+1]=8
    return g

def solve_E80(grid):
    g=clone(grid)
    h,w=dims(grid)
    # rows
    for r in range(h):
        cols=[c for c in range(w) if grid[r][c]==2]
        if len(cols)==2 and all(grid[r][c]==0 for c in range(cols[0]+1, cols[1])):
            for c in range(cols[0]+1, cols[1]):
                g[r][c]=3
    # cols
    for c in range(w):
        rows=[r for r in range(h) if grid[r][c]==2]
        if len(rows)==2 and all(grid[r][c]==0 for r in range(rows[0]+1, rows[1])):
            for r in range(rows[0]+1, rows[1]):
                g[r][c]=3
    return g

def solve_E81(grid):
    g=clone(grid)
    h,w=dims(grid)
    for comp in components(grid, colors={7}):
        if border_touch_count(comp["cells"], h, w)==2:
            for r,c in comp["cells"]:
                g[r][c]=6
    return g

def solve_E82(grid):
    g=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals={(dr,dc):grid[r+dr][c+dc] for dr in [0,1] for dc in [0,1]}
            red=[pos for pos,v in vals.items() if v==2]
            zero=[pos for pos,v in vals.items() if v==0]
            if len(red)==2 and len(zero)==2:
                if set(red)=={(0,0),(1,1)} or set(red)=={(0,1),(1,0)}:
                    for dr,dc in zero:
                        g[r+dr][c+dc]=3
    return g

def solve_E83(grid):
    g=clone(grid)
    h,w=dims(grid)
    divider=None
    for c in range(w):
        if all(grid[r][c]==5 for r in range(h)):
            divider=c
            break
    if divider is None:
        return g
    for r in range(h):
        for c in range(divider):
            v=grid[r][c]
            if v!=0 and v!=5:
                mc=divider+(divider-c)
                if 0<=mc<w:
                    g[r][mc]=v
    return g

def solve_E84(grid):
    comps=components(grid, colors=set(range(1,10)))
    if not comps:
        return clone(grid)
    sizes=[len(c["cells"]) for c in comps]
    m=min(sizes)
    target=[c for c in comps if len(c["cells"])==m]
    g=clone(grid)
    if len(target)==1:
        for r,c in target[0]["cells"]:
            g[r][c]=4
    return g

def solve_M78(grid):
    g=clone(grid)
    src=None; dst=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2: src=(r,c)
            elif v==1: dst=(r,c)
    objs=components(grid, colors={3})
    if not src or not dst or len(objs)!=1:
        return g
    comp=objs[0]["cells"]
    dr=dst[0]-src[0]; dc=dst[1]-src[1]
    for r,c in comp:
        nr,nc=r+dr,c+dc
        if 0<=nr<len(g) and 0<=nc<len(g[0]):
            g[nr][nc]=8
    return g

def solve_M79(grid):
    g=clone(grid)
    frames=find_rect_frames(grid, 5)
    for r0,c0,r1,c1 in frames:
        interior=[(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]
        markers=[grid[r][c] for r,c in interior if grid[r][c] not in (0,5)]
        if len(markers)==1:
            color=markers[0]
            for r,c in interior:
                if g[r][c]==0:
                    g[r][c]=color
            return g
    return g

def solve_M80(grid):
    g=clone(grid)
    comps=components(grid, colors={2})
    if len(comps)!=1:
        return g
    shape=normalize(comps[0]["cells"])
    control=None; anchor=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {6,7,8,9}: control=(r,c,v)
            elif v==1: anchor=(r,c)
    if not control or not anchor:
        return g
    rot={6:0,7:1,8:2,9:3}[control[2]]
    shp=rotate_shape(shape, rot)
    ar,ac=anchor
    for r,c in shp:
        if 0<=ar+r<len(g) and 0<=ac+c<len(g[0]):
            g[ar+r][ac+c]=4
    return g

def solve_M81(grid):
    h,w=dims(grid)
    g=clone(grid)
    seed=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                seed=(r,c)
                break
        if seed: break
    if not seed: return g
    q=deque([seed]); seen={seed}
    while q:
        r,c=q.popleft()
        if g[r][c]!=5:
            g[r][c]=8
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and grid[nr][nc]!=5:
                seen.add((nr,nc)); q.append((nr,nc))
    return g

def solve_M82(grid):
    g=clone(grid)
    pos=defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {2,3,4,6,7,8,9}:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==2:
            a,b=sorted(cells)
            r1,c1=a; r2,c2=b
            step=1 if c2>=c1 else -1
            for c in range(c1,c2+step,step):
                g[r1][c]=color
            step=1 if r2>=r1 else -1
            for r in range(r1,r2+step,step):
                g[r][c2]=color
    return g

def solve_M83(grid):
    g=clone(grid)
    comps_all=components(grid, colors={1,2})
    legend=None
    candidates=[]
    for comp in comps_all:
        if comp["color"]==1:
            legend=comp["cells"]
        elif comp["color"]==2:
            candidates.append(comp["cells"])
    if legend is None:
        return g
    sig=canonical_rot(legend)
    matches=[]
    for cells in candidates:
        if canonical_rot(cells)==sig:
            matches.append(cells)
    if len(matches)==1:
        for r,c in matches[0]:
            g[r][c]=8
    return g

def solve_M84(grid):
    g=clone(grid)
    h,w=dims(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in ARROW_DIR:
                dr,dc=ARROW_DIR[v]
                nr,nc=r+dr,c+dc
                while 0<=nr<h and 0<=nc<w and grid[nr][nc]!=5:
                    if g[nr][nc]==0:
                        g[nr][nc]=7
                    nr+=dr; nc+=dc
    return g

def solve_H78(grid):
    g=clone(grid)
    frames=sorted(find_rect_frames(grid,5), key=lambda x: (x[2]-x[0]+1)*(x[3]-x[1]+1), reverse=True)
    if len(frames)<3:
        return g
    control=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {1,2,3}:
                control=v
                break
        if control: break
    if not control:
        return g
    outer,mid,inner=frames[:3]
    reg1=interior_of_rect(*outer) - (interior_of_rect(*mid) | set())
    reg2=interior_of_rect(*mid) - (interior_of_rect(*inner) | set())
    reg3=interior_of_rect(*inner)
    reg={1:reg1,2:reg2,3:reg3}[control]
    for r,c in reg:
        if g[r][c]==0:
            g[r][c]=8
    return g

def solve_H79(grid):
    g=clone(grid)
    start=goal=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
    if not start or not goal: return g
    distS,countS=shortest_paths_info(grid,start,blocked={5})
    distG,countG=shortest_paths_info(grid,goal,blocked={5})
    total=distS[goal[0]][goal[1]]
    if total is None: return g
    total_paths=countS[goal[0]][goal[1]]
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=5 and distS[r][c] is not None and distG[r][c] is not None and distS[r][c]+distG[r][c]==total:
                if countS[r][c]*countG[r][c]==total_paths and (r,c) not in {start,goal}:
                    g[r][c]=8
    return g

def solve_H80(grid):
    g=clone(grid)
    comps=[comp for comp in components(grid, colors={9}) if len(comp["cells"])>1]
    if len(comps)!=1:
        return g
    shape=normalize(comps[0]["cells"])
    h,w=dims(grid)
    anchors=[]
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==6 and grid[r-1][c] in {1,2,3,4}:
                anchors.append((r,c,grid[r-1][c]))
    for ar,ac,code in anchors:
        shp=dihedral(shape, code)
        for r,c in shp:
            nr,nc=ar+r, ac+c
            if 0<=nr<h and 0<=nc<w:
                g[nr][nc]=8
    return g

def solve_H81(grid):
    g=clone(grid)
    comps=components(grid, colors={2,3})
    red=[c["cells"] for c in comps if c["color"]==2]
    blue=[c["cells"] for c in comps if c["color"]==3]
    frames=find_rect_frames(grid,5)
    if len(red)!=1 or len(blue)!=1 or not frames:
        return g
    s1=set(normalize(red[0]))
    s2=set(normalize(blue[0]))
    sxor=normalize(s1 ^ s2)
    # choose largest empty 5 frame
    frame=max(frames, key=lambda x:(x[2]-x[0]+1)*(x[3]-x[1]+1))
    r0,c0,r1,c1=frame
    ir0,ic0=r0+1,c0+1
    for r,c in sxor:
        nr,nc=ir0+r, ic0+c
        if nr<r1 and nc<c1:
            g[nr][nc]=8
    return g

def solve_H82(grid):
    g=clone(grid)
    seeds={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in {2,3}:
                seeds[v]=(r,c)
    if 2 not in seeds or 3 not in seeds: return g
    dist2,_=shortest_paths_info(grid,seeds[2],blocked={5})
    dist3,_=shortest_paths_info(grid,seeds[3],blocked={5})
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0 and dist2[r][c] is not None and dist3[r][c] is not None and dist2[r][c]==dist3[r][c]:
                g[r][c]=8
    return g

def solve_H83(grid):
    g=clone(grid)
    comps=components(grid, colors={2})
    groups=defaultdict(list)
    for comp in comps:
        sig=canonical_rot(comp["cells"])
        groups[sig].append(comp["cells"])
    odd=[cells_list for sig,cells_list in groups.items() if len(cells_list)%2==1]
    if len(odd)!=1:
        return g
    for cells in odd[0]:
        r0,c0,r1,c1=bbox(cells)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                g[r][c]=7
    return g

def solve_H84(grid):
    g=clone(grid)
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==5:
                continue
            # chamber over non-wall cells
            q=[(r,c)]
            seen[r][c]=True
            chamber=[]
            while q:
                rr,cc=q.pop()
                chamber.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]!=5:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            markers=[grid[rr][cc] for rr,cc in chamber if grid[rr][cc] in {1,2,3,4}]
            if markers and len(markers)%2==0:
                cnt=Counter(markers)
                top=cnt.most_common()
                if len(top)>=1 and (len(top)==1 or top[0][1]>top[1][1]):
                    color=top[0][0]
                    for rr,cc in chamber:
                        if g[rr][cc]==0:
                            g[rr][cc]=color
    return g

SOLVERS = {
    "E78": solve_E78,
    "E79": solve_E79,
    "E80": solve_E80,
    "E81": solve_E81,
    "E82": solve_E82,
    "E83": solve_E83,
    "E84": solve_E84,
    "M78": solve_M78,
    "M79": solve_M79,
    "M80": solve_M80,
    "M81": solve_M81,
    "M82": solve_M82,
    "M83": solve_M83,
    "M84": solve_M84,
    "H78": solve_H78,
    "H79": solve_H79,
    "H80": solve_H80,
    "H81": solve_H81,
    "H82": solve_H82,
    "H83": solve_H83,
    "H84": solve_H84,
}

def solve(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
