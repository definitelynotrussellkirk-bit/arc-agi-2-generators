"""Reference solvers for ARC-style additional puzzle bank volume 13.

This volume leans into diagonal-box completion, endpoint logic,
symbolic resize outputs, obstacle-aware distances, transform intersections,
vector composition, and chamber-boundary aggregation.

Helper primitives emphasized here:
- mandatory_shortest_path_cells(grid, start, goal)
- equidistant_cells(grid, a, b, blocked)
- compose_vectors(v1, v2)
- transform_intersection(shape, code_a, code_b)
"""
from typing import List, Tuple, Dict, Iterable, Set
from collections import deque, Counter, defaultdict

Grid = List[List[int]]
Cell = Tuple[int,int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def dims(g: Grid) -> Tuple[int,int]:
    return len(g), len(g[0])

def in_bounds(g: Grid, r: int, c: int) -> bool:
    h, w = dims(g)
    return 0 <= r < h and 0 <= c < w

def bbox(cells: Iterable[Cell]) -> Tuple[int,int,int,int]:
    cells = list(cells)
    rs = [r for r,_ in cells]
    cs = [c for _,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells: Iterable[Cell]) -> frozenset[Cell]:
    cells = list(cells)
    if not cells:
        return frozenset()
    r0,c0,r1,c1 = bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def translate(cells: Iterable[Cell], dr: int, dc: int) -> Set[Cell]:
    return {(r+dr, c+dc) for r,c in cells}

def reflect_v(shape: Iterable[Cell]) -> frozenset[Cell]:
    s = normalize(shape)
    if not s:
        return frozenset()
    w = max(c for _,c in s) + 1
    return normalize((r, w-1-c) for r,c in s)

def reflect_h(shape: Iterable[Cell]) -> frozenset[Cell]:
    s = normalize(shape)
    if not s:
        return frozenset()
    h = max(r for r,_ in s) + 1
    return normalize((h-1-r, c) for r,c in s)

def rotate_shape(shape: Iterable[Cell], k: int = 1) -> frozenset[Cell]:
    s = set(normalize(shape))
    for _ in range(k % 4):
        if not s:
            return frozenset()
        h = max(r for r,_ in s) + 1
        s = {(c, h-1-r) for r,c in s}
        s = set(normalize(s))
    return frozenset(s)

def dihedral(shape: Iterable[Cell], code: int) -> frozenset[Cell]:
    s = normalize(shape)
    if code == 1:
        return s
    if code == 2:
        return rotate_shape(s, 1)
    if code == 3:
        return reflect_v(s)
    if code == 4:
        return reflect_h(s)
    raise ValueError(code)

def rect_border(r0: int, c0: int, r1: int, c1: int) -> Set[Cell]:
    out = set()
    for r in range(r0, r1+1):
        out.add((r,c0)); out.add((r,c1))
    for c in range(c0, c1+1):
        out.add((r0,c)); out.add((r1,c))
    return out

def rect_interior(r0: int, c0: int, r1: int, c1: int) -> Set[Cell]:
    return {(r,c) for r in range(r0+1, r1) for c in range(c0+1, c1)}

def place(g: Grid, cells: Iterable[Cell], color: int):
    h,w = dims(g)
    for r,c in cells:
        if not (0 <= r < h and 0 <= c < w):
            raise ValueError((r,c,'out of bounds'))
        g[r][c] = color

def can_place(g: Grid, cells: Iterable[Cell], margin: int = 0, allow_on: Set[int] | None = None) -> bool:
    allow_on = allow_on or set()
    h,w = dims(g)
    cells = list(cells)
    for r,c in cells:
        if not (0 <= r < h and 0 <= c < w):
            return False
    for r,c in cells:
        for rr in range(r-margin, r+margin+1):
            for cc in range(c-margin, c+margin+1):
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] not in allow_on:
                    if g[rr][cc] != 0 and (rr,cc) not in cells:
                        return False
        if g[r][c] not in allow_on and g[r][c] != 0:
            return False
    return True

def components(g: Grid, colors: Set[int] | None = None, bg: int = 0) -> List[Dict]:
    h,w = dims(g)
    seen = [[False]*w for _ in range(h)]
    out = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c] = True
            v = g[r][c]
            if v == bg or (colors is not None and v not in colors):
                continue
            q = [(r,c)]
            cells = [(r,c)]
            while q:
                rr,cc = q.pop()
                for dr,dc in DIR4:
                    nr,nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == v:
                        seen[nr][nc] = True
                        q.append((nr,nc))
                        cells.append((nr,nc))
            out.append({'color': v, 'cells': cells})
    return out

def crop_to_bbox(g: Grid, cells: Iterable[Cell]) -> Grid:
    r0,c0,r1,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def shortest_path_dist(grid: Grid, start: Cell, blocked: Set[int]) -> Dict[Cell,int]:
    h,w = dims(grid)
    q = deque([start])
    dist = {start: 0}
    while q:
        r,c = q.popleft()
        for dr,dc in DIR4:
            nr,nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] not in blocked and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist

def shortest_path_counts(grid: Grid, start: Cell, blocked: Set[int]) -> Tuple[Dict[Cell,int], Dict[Cell,int]]:
    dist = shortest_path_dist(grid, start, blocked)
    counts = defaultdict(int)
    counts[start] = 1
    for d in range(1, max(dist.values(), default=0)+1):
        cells = [p for p,v in dist.items() if v == d]
        for r,c in cells:
            total = 0
            for dr,dc in DIR4:
                p = (r+dr, c+dc)
                if dist.get(p) == d-1:
                    total += counts[p]
            counts[(r,c)] = total
    return dist, counts

def all_nonzero_colors(g: Grid) -> Set[int]:
    return {v for row in g for v in row if v != 0}

def solve_E85(grid: Grid) -> Grid:
    """Find pairs of blue(1) cells that are diagonally adjacent (Chebyshev
    distance 1, but NOT 4-connected). Each such pair fills a 2×2 box; the
    full 2×2 region becomes red(2). Cells in 4-connected blue components
    of size > 1 are left unchanged.

    Previous implementation used components() with 4-connectivity, which
    split each diagonal pair into two singleton components — so the
    `len(cells) == 2` check never fired. Rewritten to iterate over
    blue singletons and check if any other blue singleton is diagonally
    adjacent."""
    g = clone(grid)
    h, w = dims(g)
    # Singleton blue cells (4-connected components of size 1)
    singleton_cells = [comp["cells"][0]
                       for comp in components(grid, colors={1})
                       if len(comp["cells"]) == 1]
    seen_pair = set()
    for (r, c) in singleton_cells:
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) not in singleton_cells:
                # singleton_cells is a list — convert to set once outside
                pass
        # Above loop is a no-op; rewrite cleanly:
    singletons = set(singleton_cells)
    for (r, c) in singletons:
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in singletons:
                pair = frozenset([(r, c), (nr, nc)])
                if pair in seen_pair:
                    continue
                seen_pair.add(pair)
                r0, c0, r1, c1 = bbox(pair)
                for rr in range(r0, r1 + 1):
                    for cc in range(c0, c1 + 1):
                        g[rr][cc] = 2
    return g

def solve_E86(grid: Grid) -> Grid:
    g = clone(grid)
    for comp in components(grid, colors={3}):
        cells = comp['cells']
        rs = {r for r,_ in cells}; cs = {c for _,c in cells}
        if len(cells) >= 3 and (len(rs) == 1 or len(cs) == 1):
            if len(rs) == 1:
                r = next(iter(rs))
                cmin = min(c for _,c in cells); cmax = max(c for _,c in cells)
                g[r][cmin] = g[r][cmax] = 2
            else:
                c = next(iter(cs))
                rmin = min(r for r,_ in cells); rmax = max(r for r,_ in cells)
                g[rmin][c] = g[rmax][c] = 2
    return g

def solve_E87(grid: Grid) -> Grid:
    g = clone(grid)
    h,w = dims(g)
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                continue
            if c-1 >= 0 and c+1 < w and grid[r][c-1] == 6 and grid[r][c+1] == 6:
                g[r][c] = 7
            if r-1 >= 0 and r+1 < h and grid[r-1][c] == 6 and grid[r+1][c] == 6:
                g[r][c] = 7
    return g

def solve_E88(grid: Grid) -> Grid:
    g = clone(grid)
    h,w = dims(g)
    for comp in components(grid, colors={7}):
        cells = comp['cells']
        borders = set()
        if any(r == 0 for r,_ in cells): borders.add('top')
        if any(r == h-1 for r,_ in cells): borders.add('bottom')
        if any(c == 0 for _,c in cells): borders.add('left')
        if any(c == w-1 for _,c in cells): borders.add('right')
        if len(borders) == 1:
            for r,c in cells:
                g[r][c] = 1
    return g

def solve_E89(grid: Grid) -> Grid:
    comps = [comp for comp in components(grid, colors=all_nonzero_colors(grid))]
    smallest = min(comps, key=lambda comp: len(comp['cells']))
    return crop_to_bbox(grid, smallest['cells'])

def solve_E90(grid: Grid) -> Grid:
    g = clone(grid)
    for comp in components(grid, colors={4}):
        cells = set(comp['cells'])
        r0,c0,r1,c1 = bbox(cells)
        if cells == rect_border(r0,c0,r1,c1) and r1-r0 >= 2 and c1-c0 >= 2:
            inside = rect_interior(r0,c0,r1,c1)
            markers = {(r,c): grid[r][c] for r,c in inside if grid[r][c] not in {0,4}}
            if len(markers) == 1:
                color = next(iter(markers.values()))
                for r,c in inside:
                    if g[r][c] == 0:
                        g[r][c] = color
    return g

def solve_E91(grid: Grid) -> Grid:
    g = clone(grid)
    pos_by_color = defaultdict(list)
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            if v != 0:
                pos_by_color[v].append((r,c))
    for color, cells in pos_by_color.items():
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 == r2:
            step = 1 if c2 >= c1 else -1
            if all(grid[r1][c] == 0 or c in {c1,c2} for c in range(c1, c2+step, step)):
                for c in range(min(c1,c2), max(c1,c2)+1):
                    g[r1][c] = color
        elif c1 == c2:
            step = 1 if r2 >= r1 else -1
            if all(grid[r][c1] == 0 or r in {r1,r2} for r in range(r1, r2+step, step)):
                for r in range(min(r1,r2), max(r1,r2)+1):
                    g[r][c1] = color
    return g

def solve_M85(grid: Grid) -> Grid:
    g = clone(grid)
    source = [comp for comp in components(grid, colors={1})]
    if not source:
        return g
    shape = source[0]['cells']
    src_anchor = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2), None)
    tgt_anchor = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 3), None)
    if src_anchor is None or tgt_anchor is None:
        return g
    dr = tgt_anchor[0] - src_anchor[0]
    dc = tgt_anchor[1] - src_anchor[1]
    for r,c in shape:
        nr,nc = r+dr, c+dc
        if in_bounds(g, nr, nc):
            g[nr][nc] = 8
    return g

def solve_M86(grid: Grid) -> Grid:
    g = clone(grid)
    shape_comps = components(grid, colors={8})
    if not shape_comps:
        return g
    shape = shape_comps[0]['cells']
    pivot = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 9), None)
    code = next(( v for row in grid for v in row if v in {1,2,3,4}), None)
    if pivot is None or code is None:
        return g
    for r,c in shape:
        dr,dc = r - pivot[0], c - pivot[1]
        if code == 1:
            nr,nc = pivot[0] + dr, pivot[1] + dc
        elif code == 2:
            nr,nc = pivot[0] + dc, pivot[1] - dr
        elif code == 3:
            nr,nc = pivot[0] - dr, pivot[1] - dc
        else:
            nr,nc = pivot[0] - dc, pivot[1] + dr
        if in_bounds(g, nr, nc):
            g[nr][nc] = 2
    return g

def solve_M87(grid: Grid) -> Grid:
    sizes = sorted(len(comp['cells']) for comp in components(grid, colors={2}))
    return [sizes]

def solve_M88(grid: Grid) -> Grid:
    g = clone(grid)
    h,w = dims(grid)
    seen = [[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c] == 5:
                continue
            q = deque([(r,c)])
            seen[r][c] = True
            chamber = []
            while q:
                rr,cc = q.popleft(); chamber.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and grid[nr][nc] != 5:
                        seen[nr][nc] = True
                        q.append((nr,nc))
            seeds = [(rr,cc,grid[rr][cc]) for rr,cc in chamber if grid[rr][cc] in {1,2,3,4}]
            if len(seeds) == 1:
                color = seeds[0][2]
                for rr,cc in chamber:
                    if g[rr][cc] == 0:
                        g[rr][cc] = color
    return g

def solve_M89(grid: Grid) -> Grid:
    g = clone(grid)
    pos_by_color = defaultdict(list)
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            if v != 0:
                pos_by_color[v].append((r,c))
    for color, cells in pos_by_color.items():
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 != r2 and c1 != c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                g[r][c1] = color
                g[r][c2] = color
            for c in range(min(c1,c2), max(c1,c2)+1):
                g[r1][c] = color
                g[r2][c] = color
    return g

def solve_M90(grid: Grid) -> Grid:
    g = clone(grid)
    comps = components(grid, colors={1})
    if not comps:
        return g
    flags = []
    for comp in comps:
        shp = normalize(comp['cells'])
        flags.append(shp == reflect_v(shp))
    cnt = Counter(flags)
    if len(cnt) == 2:
        odd_flag = min(cnt, key=cnt.get)
        if cnt[odd_flag] == 1:
            target = comps[flags.index(odd_flag)]['cells']
            for r,c in target:
                g[r][c] = 2
    return g

def solve_M91(grid: Grid) -> Grid:
    g = clone(grid)
    seed2 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2), None)
    seed3 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 3), None)
    if seed2 is None or seed3 is None:
        return g
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                continue
            d2 = abs(r-seed2[0]) + abs(c-seed2[1])
            d3 = abs(r-seed3[0]) + abs(c-seed3[1])
            if d2 < d3:
                g[r][c] = 2
            elif d3 < d2:
                g[r][c] = 3
    return g

def solve_H85(grid: Grid) -> Grid:
    g = clone(grid)
    start = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2), None)
    goal = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 3), None)
    if start is None or goal is None:
        return g
    ds, cs = shortest_path_counts(grid, start, {5})
    dg, cg = shortest_path_counts(grid, goal, {5})
    if goal not in ds:
        return g
    D = ds[goal]
    total = cs[goal]
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                continue
            if (r,c) in ds and (r,c) in dg and ds[(r,c)] + dg[(r,c)] == D:
                if cs[(r,c)] * cg[(r,c)] == total:
                    g[r][c] = 8
    return g

def solve_H86(grid: Grid) -> Grid:
    g = clone(grid)
    frame_cells = [comp['cells'] for comp in components(grid, colors={4})]
    frames = []
    for cells in frame_cells:
        s = set(cells)
        r0,c0,r1,c1 = bbox(cells)
        if s == rect_border(r0,c0,r1,c1):
            frames.append((r0,c0,r1,c1))
    frames.sort(key=lambda t: (t[2]-t[0])*(t[3]-t[1]), reverse=True)
    k = next((v for row in grid for v in row if v in {1,2,3}), None)
    if k is None or k >= len(frames):
        return g
    outer = frames[k-1]
    inner = frames[k]
    for r in range(outer[0]+1, outer[2]):
        for c in range(outer[1]+1, outer[3]):
            if inner[0] < r < inner[2] and inner[1] < c < inner[3]:
                continue
            if g[r][c] == 0:
                g[r][c] = 8
    return g

def solve_H87(grid: Grid) -> Grid:
    g = clone(grid)
    comps = components(grid, colors={8})
    if not comps:
        return g
    shape = normalize(comps[0]['cells'])
    codes = [v for row in grid for v in row if v in {1,2,3,4}]
    if len(codes) < 2:
        return g
    code1, code2 = codes[:2]
    anchor = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 9), None)
    if anchor is None:
        return g
    s1 = dihedral(shape, code1)
    s2 = dihedral(shape, code2)
    inter = s1 & s2
    for r,c in inter:
        nr,nc = anchor[0] + r, anchor[1] + c
        if in_bounds(g, nr, nc):
            g[nr][nc] = 2
    return g

def solve_H88(grid: Grid) -> Grid:
    g = clone(grid)
    a = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2), None)
    b = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 3), None)
    if a is None or b is None:
        return g
    da = shortest_path_dist(grid, a, {5})
    db = shortest_path_dist(grid, b, {5})
    h,w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 0 and (r,c) in da and (r,c) in db and da[(r,c)] == db[(r,c)]:
                g[r][c] = 8
    return g

def solve_H89(grid: Grid) -> Grid:
    g = clone(grid)
    shape_comps = components(grid, colors={1})
    if not shape_comps:
        return g
    shape = shape_comps[0]['cells']
    p2 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2), None)
    p3 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 3), None)
    p4 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 4), None)
    p6 = next(( (r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 6), None)
    if None in {p2,p3,p4,p6}:
        return g
    dr = (p3[0]-p2[0]) + (p6[0]-p4[0])
    dc = (p3[1]-p2[1]) + (p6[1]-p4[1])
    for r,c in shape:
        nr,nc = r+dr, c+dc
        if in_bounds(g, nr, nc):
            g[nr][nc] = 8
    return g

def solve_H90(grid: Grid) -> Grid:
    g = clone(grid)
    comps = components(grid, colors={1})
    freq = Counter(normalize(comp['cells']) for comp in comps)
    odd_shapes = {shape for shape,count in freq.items() if count % 2 == 1}
    for comp in comps:
        if normalize(comp['cells']) in odd_shapes:
            for r,c in comp['cells']:
                g[r][c] = 2
    return g

def solve_H91(grid: Grid) -> Grid:
    g = clone(grid)
    h,w = dims(grid)
    seen = [[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c] != 0:
                continue
            q = deque([(r,c)])
            seen[r][c] = True
            chamber = []
            boundary = []
            while q:
                rr,cc = q.popleft(); chamber.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc = rr+dr, cc+dc
                    if not (0 <= nr < h and 0 <= nc < w):
                        continue
                    if grid[nr][nc] == 0 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        q.append((nr,nc))
                    elif grid[nr][nc] in {1,2,3,4}:
                        boundary.append(grid[nr][nc])
            cnt = Counter(boundary)
            if cnt:
                top = cnt.most_common()
                if len(top) == 1 or top[0][1] > top[1][1]:
                    color = top[0][0]
                    for rr,cc in chamber:
                        g[rr][cc] = color
    return g

SOLVERS = {
    "E85": solve_E85,
    "E86": solve_E86,
    "E87": solve_E87,
    "E88": solve_E88,
    "E89": solve_E89,
    "E90": solve_E90,
    "E91": solve_E91,
    "M85": solve_M85,
    "M86": solve_M86,
    "M87": solve_M87,
    "M88": solve_M88,
    "M89": solve_M89,
    "M90": solve_M90,
    "M91": solve_M91,
    "H85": solve_H85,
    "H86": solve_H86,
    "H87": solve_H87,
    "H88": solve_H88,
    "H89": solve_H89,
    "H90": solve_H90,
    "H91": solve_H91,
}

def solve(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
