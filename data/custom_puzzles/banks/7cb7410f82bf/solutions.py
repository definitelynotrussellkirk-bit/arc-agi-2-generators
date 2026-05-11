"""Reference solvers for ARC-style additional puzzle bank volume 23.

This volume keeps the 4-train-pairs format and adds another 21 puzzles
spanning object filters, vector motion, chamber reasoning, maze-distance
problems, boolean shape algebra, and dihedral odd-one-out selection.

Helper ideas emphasized here:
- mandatory_shortest_path_cells
- chamber plurality voting
- exact graph-distance shells
- dihedral-equivalence classes
- transform-and-repeat stamping
- hole-count classification
"""

from __future__ import annotations
from typing import List, Tuple
from collections import deque, Counter

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
ORIENT_FILL_E157 = {(1, 1): 1, (1, 0): 2, (0, 1): 3, (0, 0): 8}
ROT_CTRL_M159 = {2: 'id', 3: 'rot90', 4: 'rot180', 6: 'rot270'}
BOOL_CTRL_H155 = {4: 'union', 6: 'inter', 8: 'xor'}
ROT_CTRL_H158 = {2: 'id', 3: 'rot90', 4: 'rot180', 6: 'rot270'}
PLURALITY_MAP_H159 = {2: 6, 3: 7, 4: 8}
def blank(h:int,w:int,v:int=0) -> Grid:
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g:Grid) -> Grid:
    return [row[:] for row in g]

def dims(g:Grid):
    return len(g), len(g[0])

def inb(g:Grid,r:int,c:int) -> bool:
    return 0 <= r < len(g) and 0 <= c < len(g[0])

def paint(g:Grid, cells, color:int, overwrite:bool=True):
    for r,c in cells:
        if inb(g,r,c) and (overwrite or g[r][c] == 0):
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
    return sorted((r-r0,c-c0) for r,c in cells)

def crop_bbox_grid(g:Grid, cells=None) -> Grid:
    if cells is None:
        cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v != 0]
    cells = list(cells)
    if not cells:
        return [[0]]
    r0,c0,r1,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def cells_to_grid(cells, color:int=8) -> Grid:
    n = normalize(cells)
    if not n:
        return [[0]]
    h = max(r for r,c in n) + 1
    w = max(c for r,c in n) + 1
    g = blank(h,w,0)
    paint(g, n, color)
    return g

def find_cells(g:Grid, color:int):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == color]

def components_by_color(g:Grid, color:int, dirs=DIR4):
    h,w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] != color or (r,c) in seen:
                continue
            stack = [(r,c)]
            seen.add((r,c))
            comp = []
            while stack:
                cr,cc = stack.pop()
                comp.append((cr,cc))
                for dr,dc in dirs:
                    nr,nc = cr+dr, cc+dc
                    if inb(g,nr,nc) and g[nr][nc] == color and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        stack.append((nr,nc))
            out.append(sorted(comp))
    return out

def components_nonwall(g:Grid, wall:int=5, dirs=DIR4):
    h,w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] == wall or (r,c) in seen:
                continue
            stack = [(r,c)]
            seen.add((r,c))
            comp = []
            while stack:
                cr,cc = stack.pop()
                comp.append((cr,cc))
                for dr,dc in dirs:
                    nr,nc = cr+dr, cc+dc
                    if inb(g,nr,nc) and g[nr][nc] != wall and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        stack.append((nr,nc))
            out.append(sorted(comp))
    return out

def is_hline(comp):
    rs = {r for r,c in comp}
    if len(rs) != 1:
        return False
    cs = sorted(c for r,c in comp)
    return cs == list(range(min(cs), max(cs)+1))

def is_vline(comp):
    cs = {c for r,c in comp}
    if len(cs) != 1:
        return False
    rs = sorted(r for r,c in comp)
    return rs == list(range(min(rs), max(rs)+1))

def rectangle_border(box):
    r0,c0,r1,c1 = box
    cells = set()
    for c in range(c0, c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0, r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return sorted(cells)

def rectangle_interior(box):
    r0,c0,r1,c1 = box
    if r1-r0 <= 1 or c1-c0 <= 1:
        return []
    return [(r,c) for r in range(r0+1, r1) for c in range(c0+1, c1)]

def is_hollow_rect(comp):
    if not comp:
        return False
    r0,c0,r1,c1 = bbox(comp)
    return sorted(comp) == rectangle_border((r0,c0,r1,c1)) and r1-r0 >= 2 and c1-c0 >= 2

def touch_borders(g:Grid, comp):
    h,w = dims(g)
    touched = set()
    for r,c in comp:
        if r == 0: touched.add('top')
        if r == h-1: touched.add('bottom')
        if c == 0: touched.add('left')
        if c == w-1: touched.add('right')
    return touched

def flood_fill_holes(comp):
    # count 4-connected zero holes within component bbox
    r0,c0,r1,c1 = bbox(comp)
    H = r1-r0+3
    W = c1-c0+3
    occ = set((r-r0+1, c-c0+1) for r,c in comp)
    seen = set()
    holes = 0
    for sr in range(H):
        for sc in range(W):
            if (sr,sc) in occ or (sr,sc) in seen:
                continue
            stack=[(sr,sc)]; seen.add((sr,sc)); region=[]; border=False
            while stack:
                r,c = stack.pop(); region.append((r,c))
                if r in (0,H-1) or c in (0,W-1):
                    border = True
                for dr,dc in DIR4:
                    nr,nc = r+dr, c+dc
                    if 0 <= nr < H and 0 <= nc < W and (nr,nc) not in occ and (nr,nc) not in seen:
                        seen.add((nr,nc)); stack.append((nr,nc))
            if not border:
                holes += 1
    return holes

def bfs_dist(g:Grid, starts, blocked={5}):
    if isinstance(starts, tuple):
        starts = [starts]
    q = deque()
    dist = {}
    for s in starts:
        q.append(s); dist[s] = 0
    while q:
        r,c = q.popleft()
        for dr,dc in DIR4:
            nr,nc = r+dr, c+dc
            if inb(g,nr,nc) and g[nr][nc] not in blocked and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist

def count_shortest_paths(g:Grid, start:Cell, goal:Cell, blocked={5}):
    dist = bfs_dist(g, start, blocked)
    if goal not in dist:
        return dist, {}
    ways = {start: 1}
    for (r,c),d in sorted(dist.items(), key=lambda kv: kv[1]):
        for dr,dc in DIR4:
            nr,nc = r+dr, c+dc
            if (nr,nc) in dist and dist[(nr,nc)] == d+1:
                ways[(nr,nc)] = ways.get((nr,nc), 0) + ways[(r,c)]
    return dist, ways

def mandatory_shortest_path_cells(g:Grid, start:Cell, goal:Cell, blocked={5}):
    ds, ws = count_shortest_paths(g, start, goal, blocked)
    if goal not in ds:
        return set()
    dg, wg = count_shortest_paths(g, goal, start, blocked)
    total = ws[goal]
    best = ds[goal]
    out = set()
    for cell,d in ds.items():
        if cell in dg and d + dg[cell] == best and ws.get(cell,0) * wg.get(cell,0) == total:
            out.add(cell)
    return out

def all_shortest_path_cells(g:Grid, start:Cell, goal:Cell, blocked={5}):
    ds, ws = count_shortest_paths(g, start, goal, blocked)
    if goal not in ds:
        return set()
    dg, wg = count_shortest_paths(g, goal, start, blocked)
    best = ds[goal]
    out = set()
    for cell,d in ds.items():
        if cell in dg and d + dg[cell] == best:
            out.add(cell)
    return out

def dihedral_norms(cells):
    n = normalize(cells)
    vars = []
    transforms = [
        lambda r,c: (r,c),
        lambda r,c: (c,-r),
        lambda r,c: (-r,-c),
        lambda r,c: (-c,r),
        lambda r,c: (r,-c),
        lambda r,c: (-r,c),
        lambda r,c: (c,r),
        lambda r,c: (-c,-r),
    ]
    for f in transforms:
        vars.append(tuple(sorted(normalize(f(r,c) for r,c in n))))
    return vars

def canonical_dihedral(cells):
    return min(dihedral_norms(cells))

def rotate_norm(cells, k:int):
    n = normalize(cells)
    out = []
    if k % 4 == 0:
        out = n
    elif k % 4 == 1:
        out = [(c,-r) for r,c in n]
    elif k % 4 == 2:
        out = [(-r,-c) for r,c in n]
    else:
        out = [(-c,r) for r,c in n]
    return normalize(out)

def transform_norm(cells, mode:str):
    n = normalize(cells)
    if mode == 'id':
        return n
    if mode == 'rot90':
        return rotate_norm(n,1)
    if mode == 'rot180':
        return rotate_norm(n,2)
    if mode == 'rot270':
        return rotate_norm(n,3)
    if mode == 'flipv':
        return normalize((r,-c) for r,c in n)
    if mode == 'fliph':
        return normalize((-r,c) for r,c in n)
    raise ValueError(mode)

def solve_E155(grid:Grid) -> Grid:
    g = clone(grid)
    for comp in components_by_color(grid, 1):
        if len(comp) == 5 and is_vline(comp):
            rs = sorted(r for r,c in comp)
            c = comp[0][1]
            g[rs[2]][c] = 2
    return g

def solve_E156(grid:Grid) -> Grid:
    g = clone(grid)
    h,w = dims(grid)
    for r in range(h):
        for c in range(1,w-1):
            if grid[r][c] == 0 and grid[r][c-1] == 7 and grid[r][c+1] == 7:
                g[r][c] = 3
    return g

def solve_E157(grid:Grid) -> Grid:
    g = clone(grid)
    for comp in components_by_color(grid, 4):
        if len(comp) == 3:
            r0,c0,r1,c1 = bbox(comp)
            if (r1-r0, c1-c0) == (1,1):
                local = {(r-r0,c-c0) for r,c in comp}
                missing = [xy for xy in [(0,0),(0,1),(1,0),(1,1)] if xy not in local]
                if len(missing) == 1:
                    mr,mc = missing[0]
                    g[r0+mr][c0+mc] = ORIENT_FILL_E157[(mr,mc)]
    return g

def solve_E158(grid:Grid) -> Grid:
    g = clone(grid)
    h,w = dims(grid)
    div = None
    for c in range(w):
        if all(grid[r][c] == 5 for r in range(h)):
            div = c; break
    if div is None:
        return g
    for r,c in find_cells(grid, 6):
        mc = div + (div - c)
        if 0 <= mc < w and g[r][mc] == 0:
            g[r][mc] = 8
    return g

def solve_E159(grid:Grid) -> Grid:
    comps = []
    for color in range(1,10):
        for comp in components_by_color(grid, color):
            comps.append((len(comp), comp))
    if not comps:
        return [[0]]
    _, comp = min(comps, key=lambda x: x[0])
    return crop_bbox_grid(grid, comp)

def solve_E160(grid:Grid) -> Grid:
    g = clone(grid)
    for comp in components_by_color(grid, 3):
        if len(touch_borders(grid, comp)) == 1:
            paint(g, comp, 8)
    return g

def solve_E161(grid:Grid) -> Grid:
    g = clone(grid)
    for comp in components_by_color(grid, 1):
        if is_hollow_rect(comp):
            r0,c0,r1,c1 = bbox(comp)
            if r1-r0+1 == 4 and c1-c0+1 == 4:
                paint(g, rectangle_interior((r0,c0,r1,c1)), 2)
    return g

def solve_M155(grid:Grid) -> Grid:
    g = clone(grid)
    obj = sorted(find_cells(grid, 1))
    p2 = find_cells(grid, 2)[0]
    p3 = find_cells(grid, 3)[0]
    dr,dc = p3[0]-p2[0], p3[1]-p2[1]
    for r,c in obj:
        nr,nc = r+dr, c+dc
        if inb(g,nr,nc):
            g[nr][nc] = 8
    return g

def solve_M156(grid:Grid) -> Grid:
    g = clone(grid)
    for color in [2,3,4]:
        pts = find_cells(grid, color)
        if len(pts) == 2:
            (r0,c0),(r1,c1) = pts
            if r0 != r1 and c0 != c1:
                paint(g, rectangle_border((min(r0,r1), min(c0,c1), max(r0,r1), max(c0,c1))), color)
    return g

def solve_M157(grid:Grid) -> Grid:
    counts = []
    for color in [2,3,4]:
        counts.append(len(components_by_color(grid, color)))
    row = [2]*counts[0] + [0] + [3]*counts[1] + [0] + [4]*counts[2]
    return [row]

def solve_M158(grid:Grid) -> Grid:
    g = clone(grid)
    best = None
    for comp in components_nonwall(grid, wall=5):
        seed_count = sum(grid[r][c] == 2 for r,c in comp)
        if best is None or seed_count > best[0]:
            best = (seed_count, comp)
    if best:
        for r,c in best[1]:
            if g[r][c] == 0:
                g[r][c] = 8
    return g

def solve_M159(grid:Grid) -> Grid:
    shape = normalize(find_cells(grid, 1))
    ctrl = [grid[r][c] for r,row in enumerate(grid) for c,v in enumerate(row) if v in ROT_CTRL_M159][0]
    anchor = find_cells(grid, 7)[0]
    out = blank(*dims(grid), 0)
    tshape = transform_norm(shape, ROT_CTRL_M159[ctrl])
    for r,c in tshape:
        rr,cc = anchor[0]+r, anchor[1]+c
        if inb(out, rr, cc):
            out[rr][cc] = 8
    return out

def solve_M160(grid:Grid) -> Grid:
    g = clone(grid)
    s = find_cells(grid, 2)[0]
    t = find_cells(grid, 3)[0]
    core = mandatory_shortest_path_cells(grid, s, t, blocked={5})
    for r,c in core:
        if g[r][c] == 0:
            g[r][c] = 8
    return g

def solve_M161(grid:Grid) -> Grid:
    out = blank(*dims(grid), 0)
    # preserve non-4 distractors
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v != 4:
                out[r][c] = v
    for comp in components_by_color(grid, 4):
        holes = flood_fill_holes(comp)
        paint(out, comp, 8 if holes == 1 else 2)
    return out

def solve_H155(grid:Grid) -> Grid:
    a = normalize(find_cells(grid, 2))
    b = normalize(find_cells(grid, 3))
    ctrl = [v for row in grid for v in row if v in BOOL_CTRL_H155][0]
    sa, sb = set(a), set(b)
    op = BOOL_CTRL_H155[ctrl]
    if op == 'union':
        res = sa | sb
    elif op == 'inter':
        res = sa & sb
    else:
        res = sa ^ sb
    return cells_to_grid(sorted(res), 9)

def solve_H156(grid:Grid) -> Grid:
    g = clone(grid)
    seeds = {2: find_cells(grid,2)[0], 3: find_cells(grid,3)[0], 4: find_cells(grid,4)[0]}
    dists = {k: bfs_dist(grid, pos, blocked={5}) for k,pos in seeds.items()}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v != 0:
                continue
            vals = [(k, dists[k].get((r,c), 10**9)) for k in seeds]
            mind = min(d for _,d in vals)
            winners = [k for k,d in vals if d == mind]
            if mind >= 10**9:
                continue
            if len(winners) > 1:
                g[r][c] = 9
            else:
                g[r][c] = {2:6, 3:7, 4:8}[winners[0]]
    return g

def solve_H157(grid:Grid) -> Grid:
    frames = []
    for comp in components_by_color(grid, 1):
        if is_hollow_rect(comp):
            frames.append(bbox(comp))
    frames = sorted(frames, key=lambda b: (b[2]-b[0]+1)*(b[3]-b[1]+1), reverse=True)
    ctrl = [v for row in grid for v in row if v in {2,3,4}][0]
    out = blank(*dims(grid), 0)
    if len(frames) < 3:
        return out
    outer, middle, inner = frames[:3]
    def band_cells(boxA, boxB):
        cells = set(rectangle_interior(boxA))
        cells2 = set(rectangle_interior(boxB))
        return sorted(cells - cells2)
    if ctrl == 2:
        cells = band_cells(outer, middle)
    elif ctrl == 3:
        cells = band_cells(middle, inner)
    else:
        cells = rectangle_interior(inner)
    paint(out, cells, 8)
    return out

def solve_H158(grid:Grid) -> Grid:
    shape = normalize(find_cells(grid, 1))
    ctrl = [v for row in grid for v in row if v in ROT_CTRL_H158][0]
    p7 = find_cells(grid, 7)[0]
    p8 = find_cells(grid, 8)[0]
    dr,dc = p8[0]-p7[0], p8[1]-p7[1]
    out = blank(*dims(grid), 0)
    tshape = transform_norm(shape, ROT_CTRL_H158[ctrl])
    top,left = p8
    while True:
        cells = [(top+r, left+c) for r,c in tshape]
        ok = True
        for rr,cc in cells:
            if not inb(grid, rr, cc) or grid[rr][cc] == 5:
                ok = False
                break
        if not ok:
            break
        paint(out, cells, 9)
        top += dr; left += dc
    return out

def solve_H159(grid:Grid) -> Grid:
    out = clone(grid)
    for comp in components_nonwall(grid, wall=5):
        seed_colors = [grid[r][c] for r,c in comp if grid[r][c] in (2,3,4)]
        if not seed_colors:
            continue
        cnt = Counter(seed_colors)
        if len(cnt) >= 2 and cnt.most_common(2)[0][1] == cnt.most_common(2)[1][1]:
            fill = 9
        else:
            fill = PLURALITY_MAP_H159[cnt.most_common(1)[0][0]]
        for r,c in comp:
            if out[r][c] == 0:
                out[r][c] = fill
    return out

def solve_H160(grid:Grid) -> Grid:
    comps = components_by_color(grid, 1)
    if not comps:
        return [[0]]
    classes = [canonical_dihedral(comp) for comp in comps]
    cnt = Counter(classes)
    odd_idx = None
    for i,cls in enumerate(classes):
        if cnt[cls] == 1:
            odd_idx = i
            break
    comp = comps[odd_idx if odd_idx is not None else 0]
    out = crop_bbox_grid(grid, comp)
    for r,row in enumerate(out):
        for c,v in enumerate(row):
            if v != 0:
                out[r][c] = 8
    return out

def solve_H161(grid:Grid) -> Grid:
    out = clone(grid)
    seed = find_cells(grid, 2)[0]
    k = len(find_cells(grid, 7))
    dist = bfs_dist(grid, seed, blocked={5})
    for (r,c),d in dist.items():
        if out[r][c] == 0 and d == k:
            out[r][c] = 8
    return out

SOLVERS = {
    'E155': solve_E155,
    'E156': solve_E156,
    'E157': solve_E157,
    'E158': solve_E158,
    'E159': solve_E159,
    'E160': solve_E160,
    'E161': solve_E161,
    'M155': solve_M155,
    'M156': solve_M156,
    'M157': solve_M157,
    'M158': solve_M158,
    'M159': solve_M159,
    'M160': solve_M160,
    'M161': solve_M161,
    'H155': solve_H155,
    'H156': solve_H156,
    'H157': solve_H157,
    'H158': solve_H158,
    'H159': solve_H159,
    'H160': solve_H160,
    'H161': solve_H161,
}
