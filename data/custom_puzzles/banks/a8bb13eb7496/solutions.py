"""Reference solvers for ARC-style additional puzzle bank volume 19.

This volume keeps the 4-train-pairs format and emphasizes solid-rectangle corners,
gap marking, border-touch counting, L-completion, component-size selection,
divider reflections, row/column Cartesian products, unique maze paths,
normalized intersections, three-way boolean overlap, shortest-path unions,
seed-count chamber selection, dihedral transforms, wall-constrained Voronoi
partitions, vector repeat stamping, and legend-controlled boolean operations.

Helper ideas emphasized here:
- filled_rect_corners
- border_touch_count
- normalize_shape
- shortest_path_union
- voronoi_partition
- repeat_stamp
- legend_boolean
"""
from __future__ import annotations
from typing import List, Tuple, Iterable, Dict, Set
from collections import deque, Counter

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = DIR4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h:int,w:int,v:int=0)->Grid:
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def dims(g:Grid):
    return len(g), len(g[0])

def inb(g:Grid, r:int, c:int)->bool:
    h,w=dims(g)
    return 0 <= r < h and 0 <= c < w

def paint(g:Grid, cells:Iterable[Cell], color:int):
    for r,c in cells:
        if 0 <= r < len(g) and 0 <= c < len(g[0]):
            g[r][c] = color

def find_cells(g:Grid, color:int)->List[Cell]:
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == color]

def bbox(cells:Iterable[Cell]):
    cells = list(cells)
    rs = [r for r,_ in cells]
    cs = [c for _,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells:Iterable[Cell])->List[Cell]:
    cells = list(cells)
    if not cells:
        return []
    r0,c0,_,_ = bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def crop_cells(cells:Iterable[Cell], color:int=8)->Grid:
    cells = list(cells)
    if not cells:
        return [[0]]
    norm = normalize(cells)
    rmax = max(r for r,_ in norm)
    cmax = max(c for _,c in norm)
    g = blank(rmax+1, cmax+1, 0)
    paint(g, norm, color)
    return g

def components(g:Grid, color:int, dirs=DIR4)->List[List[Cell]]:
    h,w = dims(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c] != color or (r,c) in seen:
                continue
            comp=[]
            q=[(r,c)]
            seen.add((r,c))
            while q:
                cr,cc = q.pop()
                comp.append((cr,cc))
                for dr,dc in dirs:
                    nr,nc = cr+dr, cc+dc
                    if inb(g,nr,nc) and g[nr][nc] == color and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append(sorted(comp))
    return out

def translate(cells:Iterable[Cell], dr:int, dc:int)->List[Cell]:
    return sorted((r+dr, c+dc) for r,c in cells)

def is_straight_line(cells:Iterable[Cell])->bool:
    cells = list(cells)
    if not cells:
        return False
    rs = {r for r,_ in cells}
    cs = {c for _,c in cells}
    if len(rs)==1:
        row = next(iter(rs))
        xs = sorted(c for _,c in cells)
        return xs == list(range(min(xs), max(xs)+1))
    if len(cs)==1:
        col = next(iter(cs))
        ys = sorted(r for r,_ in cells)
        return ys == list(range(min(ys), max(ys)+1))
    return False

def line_endpoints(cells:Iterable[Cell])->List[Cell]:
    cells = list(cells)
    rs={r for r,_ in cells}; cs={c for _,c in cells}
    if len(rs)==1:
        row=next(iter(rs))
        xs=sorted(c for _,c in cells)
        return [(row, xs[0]), (row, xs[-1])]
    col=next(iter(cs))
    ys=sorted(r for r,_ in cells)
    return [(ys[0], col), (ys[-1], col)]

def rectangle_fill_cells(box):
    r0,c0,r1,c1 = box
    return [(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)]

def rectangle_border_cells(box):
    r0,c0,r1,c1 = box
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return sorted(cells)

def rectangle_interior_cells(box):
    r0,c0,r1,c1 = box
    return [(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]

def is_hollow_rect(comp:Iterable[Cell])->bool:
    comp = list(comp)
    r0,c0,r1,c1 = bbox(comp)
    return sorted(comp) == rectangle_border_cells((r0,c0,r1,c1)) and r1-r0 >= 2 and c1-c0 >= 2

def is_filled_rect(comp:Iterable[Cell])->bool:
    comp = list(comp)
    r0,c0,r1,c1 = bbox(comp)
    return len(comp) == (r1-r0+1)*(c1-c0+1)

def rot90(cells:Iterable[Cell])->List[Cell]:
    n = normalize(cells)
    if not n:
        return []
    rmax = max(r for r,_ in n)
    return normalize((c, rmax-r) for r,c in n)

def rot180(cells:Iterable[Cell])->List[Cell]:
    return rot90(rot90(cells))

def rot270(cells:Iterable[Cell])->List[Cell]:
    return rot90(rot180(cells))

def flip_h(cells:Iterable[Cell])->List[Cell]:
    n = normalize(cells)
    if not n:
        return []
    rmax = max(r for r,_ in n)
    return normalize((rmax-r, c) for r,c in n)

def flip_v(cells:Iterable[Cell])->List[Cell]:
    n = normalize(cells)
    if not n:
        return []
    cmax = max(c for _,c in n)
    return normalize((r, cmax-c) for r,c in n)

def apply_rot(cells:Iterable[Cell], code:int)->List[Cell]:
    code %= 4
    if code == 0: return normalize(cells)
    if code == 1: return rot90(cells)
    if code == 2: return rot180(cells)
    return rot270(cells)

def dihedral_variant(cells:Iterable[Cell], rot:int, flip:bool)->List[Cell]:
    base = flip_h(cells) if flip else normalize(cells)
    return apply_rot(base, rot)

def passable_components(g:Grid, passable:Set[int]|None=None)->List[List[Cell]]:
    if passable is None:
        passable = {0,2,3}
    h,w=dims(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c] not in passable or (r,c) in seen:
                continue
            comp=[]
            q=[(r,c)]
            seen.add((r,c))
            while q:
                cr,cc=q.pop()
                comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr, cc+dc
                    if inb(g,nr,nc) and g[nr][nc] in passable and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append(sorted(comp))
    return out

def bfs_dist(g:Grid, start:Cell, blocked:Set[int]={5})->Dict[Cell,int]:
    q=deque([start])
    dist={start:0}
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and g[nr][nc] not in blocked and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist

def shortest_path_any(g:Grid, start:Cell, goal:Cell, blocked:Set[int]={5})->List[Cell]:
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        r,c=cur
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            nxt=(nr,nc)
            if inb(g,nr,nc) and g[nr][nc] not in blocked and nxt not in prev:
                prev[nxt]=cur
                q.append(nxt)
    if goal not in prev:
        return []
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return list(reversed(path))

def shortest_path_union_cells(g:Grid, start:Cell, goal:Cell, blocked:Set[int]={5})->List[Cell]:
    ds=bfs_dist(g,start,blocked)
    de=bfs_dist(g,goal,blocked)
    if goal not in ds:
        return []
    best=ds[goal]
    return sorted([cell for cell,d in ds.items() if cell in de and d + de[cell] == best])

def solve_E127(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1):
        if not is_filled_rect(comp):
            continue
        r0,c0,r1,c1=bbox(comp)
        if r1-r0+1 >= 2 and c1-c0+1 >= 2:
            for cell in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
                g[cell[0]][cell[1]] = 2
    return g

def solve_E128(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        for c in range(1,w-1):
            if grid[r][c]==0 and grid[r][c-1]==1 and grid[r][c+1]==1:
                g[r][c]=2
    return g

def solve_E129(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(grid)
    for comp in components(grid,6):
        touches = 0
        if any(r==0 for r,_ in comp): touches += 1
        if any(r==h-1 for r,_ in comp): touches += 1
        if any(c==0 for _,c in comp): touches += 1
        if any(c==w-1 for _,c in comp): touches += 1
        if touches == 1:
            for r,c in comp:
                g[r][c]=4
    return g

def solve_E130(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,2):
        if len(comp) != 3:
            continue
        r0,c0,r1,c1 = bbox(comp)
        if (r1-r0+1, c1-c0+1) != (2,2):
            continue
        missing = set(rectangle_fill_cells((r0,c0,r1,c1))) - set(comp)
        if len(missing)==1:
            r,c = next(iter(missing))
            g[r][c] = 3
    return g

def solve_E131(grid:Grid)->Grid:
    comps = components(grid,7)
    comp = sorted(comps, key=lambda c:(len(c), normalize(c), c))[0]
    return crop_cells(comp, 8)

def solve_E132(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,8):
        if len(comp)==4 and is_straight_line(comp):
            for r,c in line_endpoints(comp):
                g[r][c]=2
    return g

def solve_E133(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,4):
        if is_hollow_rect(comp):
            r0,c0,r1,c1 = bbox(comp)
            if (r1-r0+1, c1-c0+1)==(3,3):
                for r,c in rectangle_interior_cells((r0,c0,r1,c1)):
                    g[r][c]=1
    return g

def solve_M127(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    shape = sorted(components(grid,3), key=len, reverse=True)[0]
    a = find_cells(grid,2)[0]
    b = find_cells(grid,1)[0]
    dr,dc = b[0]-a[0], b[1]-a[1]
    paint(out, translate(shape, dr, dc), 8)
    return out

def solve_M128(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    div = None
    for c in range(w):
        if all(grid[r][c]==5 for r in range(h)):
            div = c
            break
    if div is None:
        return out
    for comp in components(grid,1):
        reflected = [(r, 2*div - c) for r,c in comp]
        paint(out, reflected, 8)
    return out

def solve_M129(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    rows = sorted({r for r,c in find_cells(grid,2)})
    cols = sorted({c for r,c in find_cells(grid,3)})
    paint(out, ((r,c) for r in rows for c in cols), 8)
    return out

def solve_M130(grid:Grid)->Grid:
    comps = components(grid,2)
    comps = sorted(comps, key=lambda c:(-len(c), normalize(c), c))
    comp = comps[1]
    return crop_cells(comp, 8)

def solve_M131(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    path = shortest_path_any(grid, a, b, blocked={5})
    paint(out, path, 8)
    return out

def solve_M132(grid:Grid)->Grid:
    a = normalize(components(grid,2)[0])
    b = normalize(components(grid,3)[0])
    inter = sorted(set(a) & set(b))
    return crop_cells(inter, 8)

def solve_M133(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,5):
        if not is_hollow_rect(comp):
            continue
        r0,c0,r1,c1 = bbox(comp)
        inside = rectangle_interior_cells((r0,c0,r1,c1))
        colors = {grid[r][c] for r,c in inside if grid[r][c] not in (0,5)}
        if len(colors)==1:
            col = next(iter(colors))
            for r,c in inside:
                if g[r][c]==0:
                    g[r][c]=col
    return g

def solve_H127(grid:Grid)->Grid:
    shapes = [set(normalize(components(grid,col)[0])) for col in (1,2,3)]
    counts = Counter(cell for s in shapes for cell in s)
    out = sorted([cell for cell,n in counts.items() if n==2])
    return crop_cells(out, 8)

def solve_H128(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    paint(out, shortest_path_union_cells(grid, a, b, blocked={5}), 8)
    return out

def solve_H129(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    comps = passable_components(grid, passable={0,2})
    scored=[]
    for comp in comps:
        seeds = sum(1 for r,c in comp if grid[r][c]==2)
        scored.append((seeds, len(comp), comp))
    scored.sort(key=lambda t:(-t[0], -t[1], t[2][0]))
    if scored:
        paint(out, scored[0][2], 8)
    return out

def solve_H130(grid:Grid)->Grid:
    h,w=dims(grid)
    shape = components(grid,2)[0]
    corners = {(0,0):0, (0,w-1):1, (h-1,w-1):2, (h-1,0):3}
    rot = 0
    for cell,code in corners.items():
        r,c=cell
        if grid[r][c]==1:
            rot=code
            break
    flip = bool(find_cells(grid,3))
    transformed = dihedral_variant(shape, rot, flip)
    return crop_cells(transformed, 8)

def solve_H131(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    da=bfs_dist(grid, a, blocked={5})
    db=bfs_dist(grid, b, blocked={5})
    allcells=set(da)|set(db)
    for cell in allcells:
        if cell not in da or cell not in db:
            continue
        if da[cell] < db[cell]:
            out[cell[0]][cell[1]] = 8
        elif db[cell] < da[cell]:
            out[cell[0]][cell[1]] = 6
        else:
            out[cell[0]][cell[1]] = 4
    return out

def solve_H132(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    shape = components(grid,2)[0]
    a=find_cells(grid,3)[0]
    b=find_cells(grid,4)[0]
    dr,dc = b[0]-a[0], b[1]-a[1]
    union=set()
    for k in range(3):
        union |= set(translate(shape, k*dr, k*dc))
    paint(out, union, 8)
    return out

def solve_H133(grid:Grid)->Grid:
    a=set(normalize(components(grid,1)[0]))
    b=set(normalize(components(grid,2)[0]))
    if find_cells(grid,3):
        cells = a & b
    elif find_cells(grid,4):
        cells = a | b
    else:
        cells = a ^ b
    return crop_cells(sorted(cells), 8)

SOLVERS = {
    'E127': solve_E127,
    'E128': solve_E128,
    'E129': solve_E129,
    'E130': solve_E130,
    'E131': solve_E131,
    'E132': solve_E132,
    'E133': solve_E133,
    'M127': solve_M127,
    'M128': solve_M128,
    'M129': solve_M129,
    'M130': solve_M130,
    'M131': solve_M131,
    'M132': solve_M132,
    'M133': solve_M133,
    'H127': solve_H127,
    'H128': solve_H128,
    'H129': solve_H129,
    'H130': solve_H130,
    'H131': solve_H131,
    'H132': solve_H132,
    'H133': solve_H133,
}
