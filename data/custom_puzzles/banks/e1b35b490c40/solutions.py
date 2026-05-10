"""Reference solvers for ARC-style additional puzzle bank volume 9.

This volume leans into anti-diagonal symmetry, aspect-ratio classification,
marker-implied rectangle overlap, checkpoint routing, chamber selection by seed count,
scaling, transposition, and shape-frequency grouping.

New helper primitives emphasized here:
- anti_diagonal_reflect_cell(r, c, n)   # used conceptually in E60
- l_path(a, b)                          # explicit in M60
- transpose_shape(shape)                # explicit in H62
- scale_shape(shape, k)                 # explicit in H58
"""

from typing import List
from collections import Counter, defaultdict, deque

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
    if not cells:
        return set()
    r0,c0,r1,c1 = bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}


def render_shape(shape, color=1):
    s=normalize(shape)
    if not s:
        return [[0]]
    h=max(r for r,c in s)+1
    w=max(c for r,c in s)+1
    g=blank(h,w)
    for r,c in s:
        g[r][c]=color
    return g


def rotate_shape(shape, k=1):
    s=set(shape)
    for _ in range(k%4):
        if not s: return set()
        h=max(r for r,c in s)+1
        s={(c, h-1-r) for r,c in s}
        s=normalize(s)
    return s


def transpose_shape(shape):
    return normalize({(c,r) for r,c in shape})


def scale_shape(shape, k):
    out=set()
    for r,c in shape:
        for dr in range(k):
            for dc in range(k):
                out.add((r*k+dr,c*k+dc))
    return normalize(out)


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


def is_solid_rectangle(cells):
    S=set(cells)
    r0,c0,r1,c1=bbox(S)
    return len(S)==(r1-r0+1)*(c1-c0+1)


def shortest_path(g, start, goal, blocked={5}):
    h,w=dims(g)
    q=deque([start])
    prev={start: None}
    while q:
        r,c=q.popleft()
        if (r,c)==goal:
            break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and g[nr][nc] not in blocked:
                prev[(nr,nc)] = (r,c)
                q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return path[::-1]


def l_path(a,b):
    (r1,c1),(r2,c2)=a,b
    out=[]
    step = 1 if c2>=c1 else -1
    for c in range(c1,c2+step,step):
        out.append((r1,c))
    step = 1 if r2>=r1 else -1
    for r in range(r1+step,r2+step,step):
        out.append((r,c2))
    return out


def solve_E57(grid):
    out=clone(grid)
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        if len(cells)==9 and is_solid_rectangle(cells):
            r0,c0,r1,c1=bbox(cells)
            if (r1-r0+1, c1-c0+1)==(3,3):
                for r,c in cells:
                    out[r][c]=3
    return out


def solve_E58(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            cells=[grid[r+dr][c+dc] for dr in range(2) for dc in range(2)]
            ones=[i for i,v in enumerate(cells) if v==1]
            zeros=[i for i,v in enumerate(cells) if v==0]
            if len(ones)==3 and len(zeros)==1:
                i=zeros[0]
                out[r+i//2][c+i%2]=3
    return out


def solve_E59(grid):
    out=clone(grid)
    for comp in components(grid, colors={7}):
        cells=comp["cells"]
        if len(cells)==5:
            rs={r for r,c in cells}; cs={c for r,c in cells}
            if len(rs)==1:
                row=next(iter(rs))
                cols=sorted(cs)
                if cols==list(range(cols[0], cols[0]+5)):
                    out[row][cols[2]]=8
            elif len(cs)==1:
                col=next(iter(cs))
                rows=sorted(rs)
                if rows==list(range(rows[0], rows[0]+5)):
                    out[rows[2]][col]=8
    return out


def solve_E60(grid):
    n=len(grid)
    out=clone(grid)
    for r in range(n):
        for c in range(n):
            v=grid[r][c]
            if v!=0:
                rr,cc=n-1-c, n-1-r
                out[rr][cc]=v
    return out


def solve_E61(grid):
    out=clone(grid)
    h,w=dims(grid)
    pos_by_color=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                pos_by_color[grid[r][c]].append((r,c))
    for color,cells in pos_by_color.items():
        if len(cells)==3:
            rs=sorted(set(r for r,c in cells))
            cs=sorted(set(c for r,c in cells))
            if len(rs)==2 and len(cs)==2:
                corners={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}
                missing=list(corners-set(cells))
                if len(missing)==1:
                    r,c=missing[0]
                    out[r][c]=color
    return out


def solve_E62(grid):
    out=clone(grid)
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        if len(cells)==6 and is_solid_rectangle(cells):
            r0,c0,r1,c1=bbox(cells)
            if sorted((r1-r0+1,c1-c0+1))==[2,3]:
                for r,c in cells:
                    out[r][c]=2
    return out


def solve_E63(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c]==0 and grid[r-1][c]==grid[r+1][c]==grid[r][c-1]==grid[r][c+1]==2:
                out[r][c]=4
    return out


def solve_M57(grid):
    out=clone(grid)
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        if is_solid_rectangle(cells):
            r0,c0,r1,c1=bbox(cells)
            h=r1-r0+1; w=c1-c0+1
            newc=8 if h==w else (2 if w>h else 3)
            for r,c in cells:
                out[r][c]=newc
    return out


def solve_M58(grid):
    h,w=dims(grid)
    out=blank(h,w)
    pos_by_color=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if grid[r][c] in (1,2):
                pos_by_color[grid[r][c]].append((r,c))
    if len(pos_by_color[1])!=2 or len(pos_by_color[2])!=2:
        return out
    def rect_from_markers(cells):
        rs=sorted(r for r,c in cells); cs=sorted(c for r,c in cells)
        return rs[0], cs[0], rs[1], cs[1]
    r0b,c0b,r1b,c1b=rect_from_markers(pos_by_color[1])
    r0r,c0r,r1r,c1r=rect_from_markers(pos_by_color[2])
    rr0=max(r0b,r0r); cc0=max(c0b,c0r); rr1=min(r1b,r1r); cc1=min(c1b,c1r)
    if rr0<=rr1 and cc0<=cc1:
        for r in range(rr0,rr1+1):
            for c in range(cc0,cc1+1):
                out[r][c]=3
    return out


def solve_M59(grid):
    comps=components(grid, colors={6})
    freq=Counter(tuple(sorted(normalize(comp["cells"]))) for comp in comps)
    target=None
    for comp in comps:
        key=tuple(sorted(normalize(comp["cells"])))
        if freq[key]==1:
            target=comp["cells"]
            break
    if target is None:
        return [[0]]
    return render_shape(normalize(target), 6)


def solve_M60(grid):
    h,w=dims(grid)
    out=blank(h,w)
    pos_by_color=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                pos_by_color[v].append((r,c))
    for color,cells in pos_by_color.items():
        if len(cells)==2:
            a,b=sorted(cells)
            for r,c in l_path(a,b):
                out[r][c]=color
    return out


def solve_M61(grid):
    counts={1:0,2:0,3:0}
    for color in counts:
        counts[color]=len(components(grid, colors={color}))
    out=blank(3,6)
    for i,color in enumerate((1,2,3)):
        for c in range(counts[color]):
            out[i][c]=color
    return out


def solve_M62(grid):
    control=grid[0][0]
    want = {2:"h",3:"v",4:"s"}[control]
    target=None
    for comp in components(grid, colors={1}):
        cells=comp["cells"]
        if is_solid_rectangle(cells):
            r0,c0,r1,c1=bbox(cells); h=r1-r0+1; w=c1-c0+1
            kind="s" if h==w else ("h" if w>h else "v")
            if kind==want:
                target=cells; break
    return render_shape(normalize(target), 1) if target else [[0]]


def solve_M63(grid):
    out=clone(grid)
    rects=[comp for comp in components(grid, colors={1}) if is_solid_rectangle(comp["cells"])]
    rects.sort(key=lambda comp: len(comp["cells"]))
    target=rects[len(rects)//2]
    for r,c in target["cells"]:
        out[r][c]=8
    return out


def solve_H57(grid):
    h,w=dims(grid)
    start=check=goal=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==2: start=(r,c)
            elif grid[r][c]==3: check=(r,c)
            elif grid[r][c]==4: goal=(r,c)
    p1=shortest_path(grid,start,check,blocked={5})
    p2=shortest_path(grid,check,goal,blocked={5})
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                out[r][c]=5
    for path in (p1,p2):
        for r,c in path:
            out[r][c]=8
    return out


def solve_H58(grid):
    h,w=dims(grid)
    scale = 1 if grid[0][0]==1 else 2
    rot = {3:0,4:1,5:2,6:3}[grid[0][1]]
    anchor=None
    comps=[]
    for r in range(h):
        for c in range(w):
            if grid[r][c]==8:
                anchor=(r,c)
    for comp in components(grid, colors={7}):
        comps.append(comp)
    if not comps or anchor is None:
        return blank(h,w)
    shape=normalize(comps[0]["cells"])
    shape=scale_shape(shape, scale)
    shape=rotate_shape(shape, rot)
    out=blank(h,w)
    ar,ac=anchor
    for r,c in shape:
        if 0<=ar+r<h and 0<=ac+c<w:
            out[ar+r][ac+c]=7
    return out


def solve_H59(grid):
    h,w=dims(grid)
    target_count=grid[0][0]
    out=blank(h,w)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                out[r][c]=5
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==5 or (r,c)==(0,0):
                seen[r][c]=True
                continue
            if grid[r][c] in (0,2):
                q=[(r,c)]
                seen[r][c]=True
                cells=[]
                seeds=0
                while q:
                    rr,cc=q.pop()
                    cells.append((rr,cc))
                    if grid[rr][cc]==2:
                        seeds+=1
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]!=5 and (nr,nc)!=(0,0):
                            seen[nr][nc]=True
                            q.append((nr,nc))
                if seeds==target_count:
                    for rr,cc in cells:
                        out[rr][cc]=8
    return out


def solve_H60(grid):
    h,w=dims(grid)
    rot={3:0,4:1,5:2,6:3}[grid[0][0]]
    comps1=components(grid, colors={1})
    comps2=components(grid, colors={2})
    if not comps1 or not comps2:
        return [[0]]
    a=rotate_shape(normalize(comps1[0]["cells"]), rot)
    b=normalize(comps2[0]["cells"])
    inter=a & b
    return render_shape(inter, 8)


def solve_H61(grid):
    totals={1:0,2:0,3:0}
    for row in grid:
        for v in row:
            if v in totals:
                totals[v]+=1
    H=6; W=3
    out=blank(H,W)
    for c,color in enumerate((1,2,3)):
        hgt=totals[color]
        for r in range(H-hgt,H):
            if 0<=r<H:
                out[r][c]=color
    return out


def solve_H62(grid):
    comps=components(grid, colors={6})
    comps.sort(key=lambda comp: len(comp["cells"]))
    target=normalize(comps[len(comps)//2]["cells"])
    trans=transpose_shape(target)
    return render_shape(trans, 6)


def solve_H63(grid):
    out=clone(grid)
    comps=components(grid, colors={1})
    freq=Counter(tuple(sorted(normalize(comp["cells"]))) for comp in comps)
    for comp in comps:
        key=tuple(sorted(normalize(comp["cells"])))
        newc=8 if freq[key]==1 else 2
        for r,c in comp["cells"]:
            out[r][c]=newc
    return out


SOLVERS = {
    "E57": solve_E57,
    "E58": solve_E58,
    "E59": solve_E59,
    "E60": solve_E60,
    "E61": solve_E61,
    "E62": solve_E62,
    "E63": solve_E63,
    "M57": solve_M57,
    "M58": solve_M58,
    "M59": solve_M59,
    "M60": solve_M60,
    "M61": solve_M61,
    "M62": solve_M62,
    "M63": solve_M63,
    "H57": solve_H57,
    "H58": solve_H58,
    "H59": solve_H59,
    "H60": solve_H60,
    "H61": solve_H61,
    "H62": solve_H62,
    "H63": solve_H63,
}

