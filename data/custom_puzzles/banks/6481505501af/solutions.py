"""Reference solvers for ARC-style additional puzzle bank volume 21.

This volume keeps the 4-train-pairs format and emphasizes endpoint marking,
local square completion, border-touch logic, mirror copying, vector
translation, orientation classification, bounding-box overlap,
control-selected rotation, frame filling, packing, two-axis reflection,
shortest-path unions, three-seed Voronoi partitions, nested-frame indexing,
controlled boolean shape algebra, mirror-beam tracing, repeat stamping, and
chamber plurality fills.

Helper ideas emphasized here:
- endpoint_cells
- bbox_intersection
- frame_marker_fill
- quadrant_reflect
- shortest_path_union
- voronoi3
- beam_trace
- repeat_stamp
"""
from __future__ import annotations
from typing import List, Tuple
from collections import deque, Counter

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = DIR4 + [(-1,-1),(-1,1),(1,-1),(1,1)]
ORIENT_MAP_M141 = {((0, 0), (0, 1), (1, 0)): 2, ((0, 0), (0, 1), (1, 1)): 3, ((0, 0), (1, 0), (1, 1)): 4, ((0, 1), (1, 0), (1, 1)): 8}
ROT_MAP_M144 = {2: 0, 3: 1, 4: 2, 6: 3}
OP_CTRL_H144 = {3: 'union', 4: 'inter', 6: 'xor'}
TR_CTRL_H144 = {7: 0, 8: 1, 9: 5}
ROT_CTRL_H146 = {2: 0, 3: 1, 4: 2}

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    return 0 <= r < len(g) and 0 <= c < len(g[0])

def paint(g, cells, color):
    for r,c in cells:
        if inb(g,r,c):
            g[r][c] = color

def bbox(cells):
    cells = list(cells)
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    cells = list(cells)
    if not cells:
        return []
    r0,c0,_,_ = bbox(cells)
    return sorted((r-r0, c-c0) for r,c in cells)

def crop_cells(cells, color=8):
    cells = list(cells)
    if not cells:
        return [[0]]
    n = normalize(cells)
    rmax = max(r for r,c in n)
    cmax = max(c for r,c in n)
    g = blank(rmax+1, cmax+1, 0)
    paint(g, n, color)
    return g

def find_cells(g,color):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == color]

def components(g, color, dirs=DIR4):
    h,w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] != color or (r,c) in seen:
                continue
            q = [(r,c)]
            seen.add((r,c))
            comp = []
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

def is_line(comp):
    rs = {r for r,c in comp}
    cs = {c for r,c in comp}
    if len(rs) == 1:
        xs = sorted(c for r,c in comp)
        return xs == list(range(min(xs), max(xs)+1)), 'h'
    if len(cs) == 1:
        ys = sorted(r for r,c in comp)
        return ys == list(range(min(ys), max(ys)+1)), 'v'
    return False, None

def translate(cells, dr, dc):
    return sorted((r+dr, c+dc) for r,c in cells)

def rectangle_border(box):
    r0,c0,r1,c1 = box
    cells = set()
    for c in range(c0, c1+1):
        cells.add((r0,c))
        cells.add((r1,c))
    for r in range(r0, r1+1):
        cells.add((r,c0))
        cells.add((r,c1))
    return sorted(cells)

def rectangle_interior(box):
    r0,c0,r1,c1 = box
    return [(r,c) for r in range(r0+1, r1) for c in range(c0+1, c1)]

def is_hollow_rect(comp):
    comp = sorted(comp)
    if not comp:
        return False
    r0,c0,r1,c1 = bbox(comp)
    return r1-r0 >= 2 and c1-c0 >= 2 and comp == rectangle_border((r0,c0,r1,c1))

def rot90(cells):
    n = normalize(cells)
    if not n:
        return []
    rmax = max(r for r,c in n)
    return normalize((c, rmax-r) for r,c in n)

def rot180(cells):
    return rot90(rot90(cells))

def rot270(cells):
    return rot90(rot180(cells))

def flip_h(cells):
    n = normalize(cells)
    if not n:
        return []
    rmax = max(r for r,c in n)
    return normalize((rmax-r, c) for r,c in n)

def flip_v(cells):
    n = normalize(cells)
    if not n:
        return []
    cmax = max(c for r,c in n)
    return normalize((r, cmax-c) for r,c in n)

def apply_dihedral(cells, code:int):
    n = normalize(cells)
    if code == 0:
        return n
    if code == 1:
        return rot90(n)
    if code == 2:
        return rot180(n)
    if code == 3:
        return rot270(n)
    if code == 4:
        return flip_h(n)
    if code == 5:
        return flip_v(n)
    if code == 6:
        return normalize((c,r) for r,c in n)
    raise ValueError(code)

def bfs_dist(g, starts, blocked={5}):
    if isinstance(starts, tuple):
        starts = [starts]
    q = deque()
    dist = {}
    for s in starts:
        q.append(s)
        dist[s] = 0
    while q:
        r,c = q.popleft()
        for dr,dc in DIR4:
            nr,nc = r+dr, c+dc
            if inb(g,nr,nc) and g[nr][nc] not in blocked and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist

def chamber_components(g, passable_colors={0,1,2,3,4,6,7,8,9}):
    h,w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] not in passable_colors or (r,c) in seen:
                continue
            q = [(r,c)]
            seen.add((r,c))
            comp = []
            while q:
                cr,cc = q.pop()
                comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc = cr+dr, cc+dc
                    if inb(g,nr,nc) and g[nr][nc] in passable_colors and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append(sorted(comp))
    return out

def beam_trace(grid):
    h,w = dims(grid)
    start = find_cells(grid, 2)[0]
    arrow = find_cells(grid, 1)[0]
    dr,dc = arrow[0]-start[0], arrow[1]-start[1]
    r,c = start
    visited = set()
    path = []
    while True:
        state = (r,c,dr,dc)
        if state in visited:
            break
        visited.add(state)
        nr,nc = r+dr, c+dc
        if not (0 <= nr < h and 0 <= nc < w):
            break
        if grid[nr][nc] == 5:
            break
        cell = grid[nr][nc]
        if cell == 0:
            path.append((nr,nc))
        if cell == 4:  # /
            dr,dc = -dc, -dr
        elif cell == 6:  # \
            dr,dc = dc, dr
        r,c = nr,nc
    return path

def solve_E141(grid):
    g = clone(grid)
    for comp in components(grid, 2):
        ok, ori = is_line(comp)
        if ok and ori == 'v' and len(comp) >= 2:
            col = comp[0][1]
            rows = sorted(r for r,c in comp)
            g[rows[0]][col] = 1
            g[rows[-1]][col] = 1
    return g

def solve_E142(grid):
    g = clone(grid)
    h,w = dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            coords = [(r,c),(r,c+1),(r+1,c),(r+1,c+1)]
            vals = [grid[rr][cc] for rr,cc in coords]
            if vals.count(4) == 3 and vals.count(0) == 1:
                rr,cc = coords[vals.index(0)]
                g[rr][cc] = 2
    return g

def solve_E143(grid):
    g = clone(grid)
    h,w = dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c] == 0 and all(grid[r+dr][c+dc] == 3 for dr,dc in DIR4):
                g[r][c] = 8
    return g

def solve_E144(grid):
    g = clone(grid)
    h,w = dims(grid)
    for comp in components(grid, 7):
        borders = set()
        for r,c in comp:
            if r == 0: borders.add('top')
            if r == h-1: borders.add('bottom')
            if c == 0: borders.add('left')
            if c == w-1: borders.add('right')
        if len(borders) == 1:
            for r,c in comp:
                g[r][c] = 5
    return g

def solve_E145(grid):
    g = clone(grid)
    h,w = dims(grid)
    divider_cols = [c for c in range(w) if all(grid[r][c] == 9 for r in range(h))]
    if not divider_cols:
        return g
    d = divider_cols[0]
    for r,c in find_cells(grid, 1):
        mc = 2*d - c
        if 0 <= mc < w and mc != d:
            g[r][mc] = 8
    return g

def solve_E146(grid):
    g = clone(grid)
    a = find_cells(grid, 2)[0]
    b = find_cells(grid, 3)[0]
    dr,dc = b[0]-a[0], b[1]-a[1]
    for r,c in find_cells(grid, 8):
        nr,nc = r+dr, c+dc
        if inb(g, nr, nc):
            g[nr][nc] = 1
    return g

def solve_E147(grid):
    comps = components(grid, 6)
    best = max(comps, key=lambda comp: (len(comp), normalize(comp)))
    return crop_cells(best, 8)

def solve_M141(grid):
    g = clone(grid)
    for comp in components(grid, 1):
        n = tuple(normalize(comp))
        if n in ORIENT_MAP_M141:
            color = ORIENT_MAP_M141[n]
            for r,c in comp:
                g[r][c] = color
    return g

def solve_M142(grid):
    g = clone(grid)
    for color in [2,3,4]:
        pts = find_cells(grid, color)
        if len(pts) == 2:
            (r1,c1),(r2,c2) = pts
            if r1 == r2:
                for c in range(min(c1,c2), max(c1,c2)+1):
                    g[r1][c] = color
            elif c1 == c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    g[r][c1] = color
    return g

def solve_M143(grid):
    reds = find_cells(grid, 2)
    greens = find_cells(grid, 3)
    if not reds or not greens:
        return [[0]]
    r0a,c0a,r1a,c1a = bbox(reds)
    r0b,c0b,r1b,c1b = bbox(greens)
    rr0,cc0 = max(r0a,r0b), max(c0a,c0b)
    rr1,cc1 = min(r1a,r1b), min(c1a,c1b)
    h,w = dims(grid)
    out = blank(h,w,0)
    if rr0 <= rr1 and cc0 <= cc1:
        for r in range(rr0, rr1+1):
            for c in range(cc0, cc1+1):
                out[r][c] = 8
    return out

def solve_M144(grid):
    h,w = dims(grid)
    template = find_cells(grid, 1)
    ctrl = next((c for c in [2,3,4,6] if find_cells(grid,c)), 2)
    anchor = find_cells(grid, 7)[0]
    shape = normalize(template)
    for _ in range(ROT_MAP_M144[ctrl]):
        shape = rot90(shape)
    out = blank(h,w,0)
    for r,c in shape:
        nr,nc = anchor[0]+r, anchor[1]+c
        if inb(out, nr, nc):
            out[nr][nc] = 8
    return out

def solve_M145(grid):
    g = clone(grid)
    for comp in components(grid, 4):
        if not is_hollow_rect(comp):
            continue
        r0,c0,r1,c1 = bbox(comp)
        interior = rectangle_interior((r0,c0,r1,c1))
        colors = {grid[r][c] for r,c in interior if grid[r][c] not in (0,4)}
        if len(colors) == 1:
            fill = next(iter(colors))
            for r,c in interior:
                if g[r][c] == 0:
                    g[r][c] = fill
    return g

def solve_M146(grid):
    comps = components(grid, 1)
    shapes = [normalize(comp) for comp in comps]
    shapes.sort(key=lambda sh: (len(sh), sh))
    height = max(max(r for r,c in sh)+1 for sh in shapes)
    width = sum(max(c for r,c in sh)+1 for sh in shapes) + (len(shapes)-1)
    out = blank(height, width, 0)
    x = 0
    for sh in shapes:
        sh_h = max(r for r,c in sh)+1
        sh_w = max(c for r,c in sh)+1
        for r,c in sh:
            out[r][x+c] = 8
        x += sh_w + 1
    return out

def solve_M147(grid):
    g = clone(grid)
    h,w = dims(grid)
    row = next(r for r in range(h) if all(grid[r][c] == 9 for c in range(w)))
    col = next(c for c in range(w) if all(grid[r][c] == 9 for r in range(h)))
    ones = find_cells(grid, 1)
    for r,c in ones:
        mr = 2*row - r
        mc = 2*col - c
        for nr,nc in {(r,mc),(mr,c),(mr,mc)}:
            if 0 <= nr < h and 0 <= nc < w and not (nr == row or nc == col):
                g[nr][nc] = 8
    return g

def solve_H141(grid):
    g = clone(grid)
    s = find_cells(grid, 2)[0]
    t = find_cells(grid, 3)[0]
    ds = bfs_dist(grid, s, {5})
    dt = bfs_dist(grid, t, {5})
    if t not in ds:
        return g
    L = ds[t]
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v == 0 and (r,c) in ds and (r,c) in dt and ds[(r,c)] + dt[(r,c)] == L:
                g[r][c] = 8
    return g

def solve_H142(grid):
    g = clone(grid)
    seeds = {}
    for color in [2,3,4]:
        pts = find_cells(grid, color)
        if pts:
            seeds[color] = pts[0]
    dists = {color: bfs_dist(grid, pos, {5}) for color,pos in seeds.items()}
    for r,row in enumerate(grid):
        for c,v in enumerate(grid):
            pass
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                continue
            vals = []
            for color,dist in dists.items():
                if (r,c) in dist:
                    vals.append((dist[(r,c)], color))
            if not vals:
                continue
            vals.sort()
            if len(vals) >= 2 and vals[0][0] == vals[1][0]:
                g[r][c] = 8
            else:
                g[r][c] = vals[0][1]
    return g

def solve_H143(grid):
    g = clone(grid)
    frames = [comp for comp in components(grid, 4) if is_hollow_rect(comp)]
    frames.sort(key=lambda comp: (bbox(comp)[2]-bbox(comp)[0])*(bbox(comp)[3]-bbox(comp)[1]), reverse=True)
    k = len(find_cells(grid, 2))
    if 1 <= k <= len(frames):
        for r,c in frames[k-1]:
            g[r][c] = 8
    return g

def solve_H144(grid):
    a = set(normalize(find_cells(grid, 1)))
    b = set(normalize(find_cells(grid, 2)))
    op = 'union'
    for c, name in OP_CTRL_H144.items():
        if find_cells(grid, c):
            op = name
            break
    tcode = 0
    for c, code in TR_CTRL_H144.items():
        if find_cells(grid, c):
            tcode = code
            break
    b2 = set(apply_dihedral(list(b), tcode))
    if op == 'union':
        res = a | b2
    elif op == 'inter':
        res = a & b2
    else:
        res = a ^ b2
    return crop_cells(sorted(res), 8)

def solve_H145(grid):
    g = clone(grid)
    for r,c in beam_trace(grid):
        g[r][c] = 8
    return g

def solve_H146(grid):
    h,w = dims(grid)
    template = normalize(find_cells(grid, 1))
    rot_ctrl = next((c for c in [2,3,4] if find_cells(grid,c)), 2)
    shape = template
    for _ in range(ROT_CTRL_H146[rot_ctrl]):
        shape = rot90(shape)
    if find_cells(grid, 6):
        shape = flip_v(shape)
    start = find_cells(grid, 7)[0]
    nxt = find_cells(grid, 8)[0]
    step = (nxt[0]-start[0], nxt[1]-start[1])
    out = blank(h,w,0)
    ar,ac = start
    while True:
        placed = [(ar+r, ac+c) for r,c in shape]
        if all(0 <= r < h and 0 <= c < w for r,c in placed):
            paint(out, placed, 9)
            ar += step[0]
            ac += step[1]
        else:
            break
    return out

def solve_H147(grid):
    g = clone(grid)
    # passable chamber cells are all non-wall cells
    comps = chamber_components(grid, {0,1,2,3,4,6,7,8,9})
    for comp in comps:
        cnt = Counter(grid[r][c] for r,c in comp if grid[r][c] in {1,2,3})
        if not cnt:
            continue
        top = cnt.most_common()
        if len(top) >= 2 and top[0][1] == top[1][1]:
            fill = 8
        else:
            fill = top[0][0]
        for r,c in comp:
            if grid[r][c] == 0:
                g[r][c] = fill
    return g

SOLVERS = {
    'E141': solve_E141,
    'E142': solve_E142,
    'E143': solve_E143,
    'E144': solve_E144,
    'E145': solve_E145,
    'E146': solve_E146,
    'E147': solve_E147,
    'M141': solve_M141,
    'M142': solve_M142,
    'M143': solve_M143,
    'M144': solve_M144,
    'M145': solve_M145,
    'M146': solve_M146,
    'M147': solve_M147,
    'H141': solve_H141,
    'H142': solve_H142,
    'H143': solve_H143,
    'H144': solve_H144,
    'H145': solve_H145,
    'H146': solve_H146,
    'H147': solve_H147
}
