"""Reference solvers for ARC-style additional puzzle bank volume 16.

This volume continues the 4-train-pairs format and emphasizes elbow detection,
gap filling, rectangle/frame structure, reflection matching, chamber counting,
maze geodesics, transform stamping, and normalized boolean shape operations.

Helper ideas emphasized here:
- shortest_union_cells
- equidistant geodesics under walls
- reflected-only shape orbits
- normalized XOR / intersection
- selected nested-frame bands
"""
from __future__ import annotations
from typing import List, Tuple, Dict, Iterable, Set
from collections import deque, defaultdict

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR8 = DIR4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def blank(h: int, w: int, v: int = 0) -> Grid:
    return [[v for _ in range(w)] for _ in range(h)]


def clone(g: Grid) -> Grid:
    return [row[:] for row in g]


def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0])


def inb(g: Grid, r: int, c: int) -> bool:
    h, w = dims(g)
    return 0 <= r < h and 0 <= c < w


def paint(g: Grid, cells: Iterable[Cell], color: int) -> None:
    for r, c in cells:
        if inb(g, r, c):
            g[r][c] = color


def fill_rect(r0: int, c0: int, r1: int, c1: int) -> Set[Cell]:
    return {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)}


def outline_rect(r0: int, c0: int, r1: int, c1: int) -> Set[Cell]:
    return {
        (r, c)
        for r in range(r0, r1 + 1)
        for c in range(c0, c1 + 1)
        if r in (r0, r1) or c in (c0, c1)
    }


def bbox(cells: Iterable[Cell]) -> Tuple[int, int, int, int]:
    cells = list(cells)
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def normalize(cells: Iterable[Cell]) -> frozenset[Cell]:
    cells = list(cells)
    if not cells:
        return frozenset()
    r0, c0, r1, c1 = bbox(cells)
    return frozenset((r - r0, c - c0) for r, c in cells)


def translate(cells: Iterable[Cell], dr: int, dc: int) -> Set[Cell]:
    return {(r + dr, c + dc) for r, c in cells}


def rotate_shape(shape: Iterable[Cell], k: int = 1) -> frozenset[Cell]:
    s = set(normalize(shape))
    for _ in range(k % 4):
        if not s:
            return frozenset()
        h = max(r for r, _ in s) + 1
        s = {(c, h - 1 - r) for r, c in s}
        s = set(normalize(s))
    return frozenset(s)


def reflect_h(shape: Iterable[Cell]) -> frozenset[Cell]:
    s = set(normalize(shape))
    if not s:
        return frozenset()
    h = max(r for r, _ in s) + 1
    return frozenset(normalize([(h - 1 - r, c) for r, c in s]))


def reflect_v(shape: Iterable[Cell]) -> frozenset[Cell]:
    s = set(normalize(shape))
    if not s:
        return frozenset()
    w = max(c for _, c in s) + 1
    return frozenset(normalize([(r, w - 1 - c) for r, c in s]))


def all_rotations(shape: Iterable[Cell]) -> Set[frozenset[Cell]]:
    return {rotate_shape(shape, k) for k in range(4)}


def all_dihedral(shape: Iterable[Cell]) -> Set[frozenset[Cell]]:
    outs: Set[frozenset[Cell]] = set()
    base = frozenset(normalize(shape))
    for k in range(4):
        r = rotate_shape(base, k)
        outs.add(r)
        outs.add(reflect_h(r))
    return outs


def component_cells(g: Grid, colors: Set[int] | None = None, connectivity: int = 4) -> List[Tuple[int, List[Cell]]]:
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    dirs = DIR4 if connectivity == 4 else DIR8
    comps: List[Tuple[int, List[Cell]]] = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            v = g[r][c]
            if colors is None:
                if v == 0:
                    continue
            else:
                if v not in colors:
                    continue
            seen[r][c] = True
            q = deque([(r, c)])
            cells: List[Cell] = []
            while q:
                rr, cc = q.popleft()
                cells.append((rr, cc))
                for dr, dc in dirs:
                    nr, nc = rr + dr, cc + dc
                    if inb(g, nr, nc) and not seen[nr][nc] and g[nr][nc] == v and (colors is None or g[nr][nc] in colors):
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append((v, cells))
    return comps


def crop_cells(cells: Iterable[Cell], color: int = 1) -> Grid:
    cells = list(cells)
    if not cells:
        return [[0]]
    r0, c0, r1, c1 = bbox(cells)
    g = blank(r1 - r0 + 1, c1 - c0 + 1)
    for r, c in cells:
        g[r - r0][c - c0] = color
    return g


def find_cells(g: Grid, color: int) -> List[Cell]:
    return [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == color]


def render(g: Grid) -> str:
    return '\n'.join(''.join(str(x) for x in row) for row in g)


def place_shape(g: Grid, shape: Iterable[Cell], top: int, left: int, color: int) -> None:
    for r, c in normalize(shape):
        rr, cc = top + r, left + c
        if not inb(g, rr, cc):
            raise ValueError(f'shape cell {(rr, cc)} out of bounds for {dims(g)}')
        g[rr][cc] = color


def add_rect(g: Grid, r0: int, c0: int, h: int, w: int, color: int, outline: bool = False) -> None:
    cells = outline_rect(r0, c0, r0 + h - 1, c0 + w - 1) if outline else fill_rect(r0, c0, r0 + h - 1, c0 + w - 1)
    paint(g, cells, color)


def bfs_dist(g: Grid, starts: List[Cell], blocked: Set[int] = {5}) -> List[List[int]]:
    h, w = dims(g)
    INF = 10**9
    dist = [[INF] * w for _ in range(h)]
    q = deque()
    for r, c in starts:
        dist[r][c] = 0
        q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if inb(g, nr, nc) and g[nr][nc] not in blocked and dist[nr][nc] == INF:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


def chambers(g: Grid, wall: int = 5) -> List[List[Cell]]:
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    out: List[List[Cell]] = []
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c] == wall:
                continue
            seen[r][c] = True
            q = deque([(r, c)])
            cells: List[Cell] = []
            while q:
                rr, cc = q.popleft()
                cells.append((rr, cc))
                for dr, dc in DIR4:
                    nr, nc = rr + dr, cc + dc
                    if inb(g, nr, nc) and not seen[nr][nc] and g[nr][nc] != wall:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            out.append(cells)
    return out


def diag_cells(r: int, c: int, length: int, slope: int = 1) -> Set[Cell]:
    if slope == 1:
        return {(r + i, c + i) for i in range(length)}
    return {(r + i, c - i) for i in range(length)}


def shortest_union_cells(grid: Grid, s: Cell, t: Cell, blocked: Set[int] = {5}) -> Set[Cell]:
    ds = bfs_dist(grid, [s], blocked)
    dt = bfs_dist(grid, [t], blocked)
    D = ds[t[0]][t[1]]
    if D >= 10**9:
        return set()
    h, w = dims(grid)
    return {
        (r, c)
        for r in range(h)
        for c in range(w)
        if ds[r][c] < 10**9 and dt[r][c] < 10**9 and ds[r][c] + dt[r][c] == D and grid[r][c] not in blocked
    }


def apply_control_transform(shape: Iterable[Cell], control: int) -> frozenset[Cell]:
    if control == 2:
        return frozenset(normalize(shape))
    if control == 3:
        return rotate_shape(shape, 1)
    if control == 4:
        return reflect_h(shape)
    if control == 6:
        return reflect_v(shape)
    raise ValueError(control)


def detect_frames(grid: Grid, color: int = 6) -> List[Tuple[int, int, int, int]]:
    frames: List[Tuple[int, int, int, int]] = []
    for _, cells in component_cells(grid, {color}, connectivity=4):
        s = set(cells)
        r0, c0, r1, c1 = bbox(s)
        if s == outline_rect(r0, c0, r1, c1):
            frames.append((r0, c0, r1, c1))
    frames.sort(key=lambda b: (b[2] - b[0] + 1) * (b[3] - b[1] + 1), reverse=True)
    return frames


def count_shortest_paths(grid: Grid, s: Cell, t: Cell, blocked: Set[int] = {5}) -> Tuple[int, Set[Cell]]:
    ds = bfs_dist(grid, [s], blocked)
    dt = bfs_dist(grid, [t], blocked)
    D = ds[t[0]][t[1]]
    if D >= 10**9:
        return 0, set()
    h, w = dims(grid)
    cells = [
        (r, c)
        for r in range(h)
        for c in range(w)
        if ds[r][c] < 10**9 and dt[r][c] < 10**9 and ds[r][c] + dt[r][c] == D and grid[r][c] not in blocked
    ]
    cells.sort(key=lambda rc: ds[rc[0]][rc[1]])
    ways: Dict[Cell, int] = defaultdict(int)
    ways[s] = 1
    for r, c in cells:
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if inb(grid, nr, nc) and grid[nr][nc] not in blocked and ds[nr][nc] == ds[r][c] + 1 and ds[nr][nc] + dt[nr][nc] == D:
                ways[(nr, nc)] += ways[(r, c)]
    return ways[t], set(cells)


def solve_E106(grid: Grid) -> Grid:
    g = clone(grid)
    for _, cells in component_cells(grid, {2}, connectivity=4):
        s = set(cells)
        if len(s) != 3:
            continue
        r0, c0, r1, c1 = bbox(s)
        if (r1 - r0, c1 - c0) != (1, 1):
            continue
        for r, c in s:
            deg = sum((r + dr, c + dc) in s for dr, dc in DIR4)
            if deg == 2:
                g[r][c] = 4
    return g


def solve_E107(grid: Grid) -> Grid:
    g = clone(grid)
    h, w = dims(g)
    for r in range(h):
        ones = [c for c in range(w) if grid[r][c] == 1]
        used: Set[int] = set()
        for i in range(len(ones)):
            for j in range(i + 1, len(ones)):
                c1, c2 = ones[i], ones[j]
                if any(grid[r][c] != 0 for c in range(c1 + 1, c2)):
                    continue
                if c1 not in used and c2 not in used:
                    for c in range(c1 + 1, c2):
                        g[r][c] = 2
                    used.add(c1)
                    used.add(c2)
    for c in range(w):
        ones = [r for r in range(h) if grid[r][c] == 1]
        used: Set[int] = set()
        for i in range(len(ones)):
            for j in range(i + 1, len(ones)):
                r1, r2 = ones[i], ones[j]
                if any(grid[r][c] != 0 for r in range(r1 + 1, r2)):
                    continue
                if r1 not in used and r2 not in used:
                    for r in range(r1 + 1, r2):
                        g[r][c] = 2
                    used.add(r1)
                    used.add(r2)
    return g


def solve_E108(grid: Grid) -> Grid:
    g = clone(grid)
    for _, cells in component_cells(grid, {3}, connectivity=4):
        s = set(cells)
        r0, c0, r1, c1 = bbox(s)
        if s == fill_rect(r0, c0, r1, c1):
            for r, c in outline_rect(r0, c0, r1, c1):
                g[r][c] = 8
    return g


def solve_E109(grid: Grid) -> Grid:
    g = clone(grid)
    h, w = dims(g)
    for r in range(h - 1):
        for c in range(w - 1):
            coords = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
            vals = [grid[rr][cc] for rr, cc in coords]
            if vals.count(1) == 3 and vals.count(0) == 1:
                idx = vals.index(0)
                rr, cc = coords[idx]
                g[rr][cc] = 2
    return g


def solve_E110(grid: Grid) -> Grid:
    g = clone(grid)
    for _, cells in component_cells(grid, {6}, connectivity=8):
        s = set(cells)
        if len(s) < 2:
            continue
        degs: Dict[Cell, int] = {}
        valid = True
        for r, c in s:
            neigh = [
                (r + dr, c + dc)
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                if (r + dr, c + dc) in s
            ]
            degs[(r, c)] = len(neigh)
            if len(neigh) not in (1, 2):
                valid = False
        if not valid:
            continue
        ends = [cell for cell, d in degs.items() if d == 1]
        if len(ends) == 2:
            for r, c in ends:
                g[r][c] = 1
    return g


def solve_E111(grid: Grid) -> Grid:
    g = clone(grid)
    h, w = dims(g)
    pattern = [4, 4, 4, 4, 0, 4, 4, 4, 4]
    for r in range(h - 2):
        for c in range(w - 2):
            vals = [grid[rr][cc] for rr in range(r, r + 3) for cc in range(c, c + 3)]
            if vals == pattern:
                g[r + 1][c + 1] = 2
    return g


def solve_E112(grid: Grid) -> Grid:
    g = clone(grid)
    h, w = dims(g)
    for _, cells in component_cells(grid, {7}, connectivity=4):
        if any(r in (0, h - 1) or c in (0, w - 1) for r, c in cells):
            for r, c in cells:
                g[r][c] = 3
    return g


def solve_M106(grid: Grid) -> Grid:
    g = clone(grid)
    for _, cells in component_cells(grid, {6}, connectivity=4):
        s = set(cells)
        r0, c0, r1, c1 = bbox(s)
        if s == outline_rect(r0, c0, r1, c1):
            for r in range(r0 + 1, r1):
                for c in range(c0 + 1, c1):
                    if g[r][c] == 0:
                        g[r][c] = 8
    return g


def solve_M107(grid: Grid) -> Grid:
    g = clone(grid)
    red = find_cells(grid, 2)[0]
    green = find_cells(grid, 3)[0]
    dr, dc = green[0] - red[0], green[1] - red[1]
    comps = [cells for _, cells in component_cells(grid, {1}, connectivity=4)]
    target = sorted(comps, key=lambda cells: (len(cells), bbox(cells)))[0]
    for r, c in target:
        g[r][c] = 0
    for r, c in target:
        nr, nc = r + dr, c + dc
        if inb(g, nr, nc):
            g[nr][nc] = 8
    return g


def solve_M108(grid: Grid) -> Grid:
    g = clone(grid)
    best = None
    best_count = -1
    for ch in chambers(grid, wall=5):
        cnt = sum(grid[r][c] == 2 for r, c in ch)
        if cnt > best_count:
            best_count = cnt
            best = ch
    assert best is not None
    for r, c in best:
        if g[r][c] == 0:
            g[r][c] = 8
    return g


def solve_M109(grid: Grid) -> Grid:
    g = clone(grid)
    source = find_cells(grid, 1)
    src_orbit = all_rotations(source)
    refl_orbit = all_dihedral(source) - src_orbit
    for _, cells in component_cells(grid, {2}, connectivity=4):
        if normalize(cells) in refl_orbit:
            for r, c in cells:
                g[r][c] = 8
    return g


def solve_M110(grid: Grid) -> Grid:
    counts = {color: len(component_cells(grid, {color}, connectivity=4)) for color in (1, 2, 3)}
    w = max(max(counts.values()), 1)
    out = blank(3, w)
    for row, color in enumerate((1, 2, 3)):
        for c in range(counts[color]):
            out[row][c] = color
    return out


def solve_M111(grid: Grid) -> Grid:
    k = sum(v == 2 for row in grid for v in row)
    for _, cells in component_cells(grid, {1}, connectivity=4):
        if len(cells) == k:
            return crop_cells(cells, color=1)
    return [[0]]


def solve_M112(grid: Grid) -> Grid:
    g = clone(grid)
    blue_adj: Set[Cell] = set()
    red_adj: Set[Cell] = set()
    for r, c in find_cells(grid, 1):
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if inb(grid, nr, nc) and grid[nr][nc] == 0:
                blue_adj.add((nr, nc))
    for r, c in find_cells(grid, 2):
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if inb(grid, nr, nc) and grid[nr][nc] == 0:
                red_adj.add((nr, nc))
    for r, c in blue_adj & red_adj:
        g[r][c] = 8
    return g


def solve_H106(grid: Grid) -> Grid:
    g = clone(grid)
    s = find_cells(grid, 2)[0]
    t = find_cells(grid, 3)[0]
    for r, c in shortest_union_cells(grid, s, t):
        if g[r][c] == 0:
            g[r][c] = 8
    return g


def solve_H107(grid: Grid) -> Grid:
    g = clone(grid)
    a = find_cells(grid, 2)[0]
    b = find_cells(grid, 3)[0]
    da = bfs_dist(grid, [a], {5})
    db = bfs_dist(grid, [b], {5})
    h, w = dims(grid)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0 and da[r][c] < 10**9 and da[r][c] == db[r][c]:
                g[r][c] = 8
    return g


def solve_H108(grid: Grid) -> Grid:
    g = clone(grid)
    source = find_cells(grid, 1)
    control = [v for row in grid for v in row if v in (2, 3, 4, 6)][0]
    anchor = find_cells(grid, 9)[0]
    transformed = apply_control_transform(source, control)
    for r, c in transformed:
        nr, nc = anchor[0] + r, anchor[1] + c
        if inb(g, nr, nc):
            g[nr][nc] = 8
    return g


def solve_H109(grid: Grid) -> Grid:
    blue = set(normalize(find_cells(grid, 1)))
    red = set(normalize(find_cells(grid, 2)))
    return crop_cells(blue ^ red, color=8)


def solve_H110(grid: Grid) -> Grid:
    g = clone(grid)
    frames = detect_frames(grid, 6)
    control = [v for row in grid for v in row if v in (2, 3, 4)][0]
    depth = {2: 0, 3: 1, 4: 2}[control]
    if depth >= len(frames):
        return g
    r0, c0, r1, c1 = frames[depth]
    inner = frames[depth + 1] if depth + 1 < len(frames) else None
    region = {(r, c) for r in range(r0 + 1, r1) for c in range(c0 + 1, c1)}
    if inner:
        ir0, ic0, ir1, ic1 = inner
        region = {cell for cell in region if not (ir0 <= cell[0] <= ir1 and ic0 <= cell[1] <= ic1)}
    for r, c in region:
        if g[r][c] == 0:
            g[r][c] = 8
    return g


def solve_H111(grid: Grid) -> Grid:
    g = clone(grid)
    a = find_cells(grid, 2)[0]
    b = find_cells(grid, 4)[0]
    c = find_cells(grid, 3)[0]
    cells = shortest_union_cells(grid, a, b) | shortest_union_cells(grid, b, c)
    for r, cc in cells:
        if g[r][cc] == 0:
            g[r][cc] = 8
    return g


def solve_H112(grid: Grid) -> Grid:
    s1 = set(normalize(find_cells(grid, 1)))
    s2 = set(normalize(find_cells(grid, 2)))
    s3 = set(normalize(find_cells(grid, 3)))
    return crop_cells(s1 & s2 & s3, color=8)


SOLVERS = {
    'E106': solve_E106,
    'E107': solve_E107,
    'E108': solve_E108,
    'E109': solve_E109,
    'E110': solve_E110,
    'E111': solve_E111,
    'E112': solve_E112,
    'M106': solve_M106,
    'M107': solve_M107,
    'M108': solve_M108,
    'M109': solve_M109,
    'M110': solve_M110,
    'M111': solve_M111,
    'M112': solve_M112,
    'H106': solve_H106,
    'H107': solve_H107,
    'H108': solve_H108,
    'H109': solve_H109,
    'H110': solve_H110,
    'H111': solve_H111,
    'H112': solve_H112,
}

def solve_by_id(puzzle_id: str, grid: Grid) -> Grid:
    return SOLVERS[puzzle_id](grid)
