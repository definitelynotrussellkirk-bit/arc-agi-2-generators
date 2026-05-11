"""Reference solvers for the twelfth 21-task ARC-style puzzle bank.

This batch leans into:
- morphology of runs, rectangles, frames, pluses, and X-shapes
- room filling, hole counting, color sorting, area arithmetic, and keyed borders
- ordered routing, geodesic propagation, frame tiling, overlap logic, visibility graphs,
  fit-by-dimensions matching, and parity wavefronts
"""
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "vertical_run_endcaps": "Reduce each vertical run to its first and last cells.",
    "checkerize_bbox": "Turn a filled rectangle into a parity checkerboard inside its bbox.",
    "bbox_center_cross": "Replace an odd rectangle by its center row and center column.",
    "frame_center_fill": "Place one colored cell at the exact center of an odd hollow frame.",
    "room_fill": "Flood only the enclosed room that contains a seed.",
    "median_select": "Keep the component whose scalar score is the median of the set.",
    "area_primality": "Classify a component by whether its area is prime or composite.",
    "corner_pair_rect_border": "Two opposite-corner markers define only a rectangle border.",
    "marker_transform_stamp": "Marker colors choose rigid transforms of a template before stamping.",
    "ordered_waypoint_path": "Route one path that must visit labeled waypoints in order.",
    "geodesic_voronoi": "Fill open cells by nearest-seed distance measured through walls.",
    "frame_tiling": "Repeat a template periodically inside a frame interior.",
    "two_of_three_overlay": "After normalization, keep cells occupied by exactly two of three shapes.",
    "visibility_graph": "Two objects are adjacent if they can see each other along a clear row or column.",
    "fit_by_interior_dims": "Match inserts to frames by the dimensions of the empty interior.",
    "room_bfs_parity_fill": "Color only even-distance cells from a seed within its room."
}

def blank(h: int, w: int, v: int = 0) -> Grid:
    return [[v for _ in range(w)] for __ in range(h)]

def dims(g: Grid) -> Tuple[int, int]:
    return (len(g), len(g[0]) if g else 0)

def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]

def bbox(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize_cells(cells):
    if not cells:
        return []
    r0, c0, r1, c1 = bbox(cells)
    return sorted((r - r0, c - c0) for r, c in cells)

def crop_to_cells(g: Grid, cells):
    if not cells:
        return [[0]]
    r0, c0, r1, c1 = bbox(cells)
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]

def paste(out: Grid, sub: Grid, r0: int, c0: int) -> None:
    for r, row in enumerate(sub):
        for c, v in enumerate(row):
            if v != 0:
                out[r0 + r][c0 + c] = v

def find_components(g: Grid):
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            col = g[r][c]
            if col == 0 or seen[r][c]:
                continue
            q = deque([(r, c)])
            seen[r][c] = True
            cells = []
            while q:
                rr, cc = q.popleft()
                cells.append((rr, cc))
                for dr, dc in DIR4:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == col:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append({"color": col, "cells": cells})
    return comps

def run_vertical_segments(g: Grid):
    h, w = dims(g)
    segs = []
    for c in range(w):
        r = 0
        while r < h:
            if g[r][c] == 0:
                r += 1
                continue
            col = g[r][c]
            r2 = r
            while r2 + 1 < h and g[r2 + 1][c] == col:
                r2 += 1
            segs.append((r, r2, c, col))
            r = r2 + 1
    return segs

def count_colors(g: Grid):
    d = defaultdict(int)
    for row in g:
        for v in row:
            if v != 0:
                d[v] += 1
    return dict(d)

def solid_rectangles(g: Grid):
    out = []
    for comp in find_components(g):
        cells = set(comp["cells"])
        r0, c0, r1, c1 = bbox(comp["cells"])
        expected = {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)}
        if cells == expected:
            out.append(comp)
    return out

def frame_rectangles(g: Grid):
    out = []
    for comp in find_components(g):
        cells = set(comp["cells"])
        r0, c0, r1, c1 = bbox(comp["cells"])
        expected = {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)
                    if r in (r0, r1) or c in (c0, c1)}
        if cells == expected and r1 - r0 >= 2 and c1 - c0 >= 2:
            out.append(comp)
    return out

def component_holes(g: Grid, comp):
    r0, c0, r1, c1 = bbox(comp["cells"])
    H, W = r1 - r0 + 1, c1 - c0 + 1
    sub = blank(H, W)
    for r, c in comp["cells"]:
        sub[r - r0][c - c0] = 1
    seen = [[False] * W for _ in range(H)]
    holes = 0
    for r in range(H):
        for c in range(W):
            if sub[r][c] != 0 or seen[r][c]:
                continue
            q = deque([(r, c)])
            seen[r][c] = True
            touches = (r in (0, H - 1) or c in (0, W - 1))
            while q:
                rr, cc = q.popleft()
                for dr, dc in DIR4:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < H and 0 <= nc < W and not seen[nr][nc] and sub[nr][nc] == 0:
                        seen[nr][nc] = True
                        q.append((nr, nc))
                        if nr in (0, H - 1) or nc in (0, W - 1):
                            touches = True
            if not touches:
                holes += 1
    return holes

def crop_component(g: Grid, comp):
    return crop_to_cells(g, comp["cells"])

def pack_components_from_grid(g: Grid, comps, key_fn=lambda c: c["color"], gap: int = 1, reverse: bool = False):
    ordered = sorted(comps, key=key_fn, reverse=reverse)
    crops = [crop_component(g, comp) for comp in ordered]
    if not crops:
        return [[0]]
    h = max(len(cr) for cr in crops)
    w = sum(len(cr[0]) for cr in crops) + gap * (len(crops) - 1)
    out = blank(h, w)
    x = 0
    for cr in crops:
        paste(out, cr, 0, x)
        x += len(cr[0]) + gap
    return out

def rotate90(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]

def rotate180(g: Grid) -> Grid:
    return [row[::-1] for row in g[::-1]]

def rotate270(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[r][w - 1 - c] for r in range(h)] for c in range(w - 1, -1, -1)]

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def shortest_path_with_waypoints(g: Grid, order_colors, start_color: int = 1, end_color: int = 6, wall_colors = {5}):
    h, w = dims(g)
    positions = {}
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v in [start_color, end_color] + list(order_colors):
                positions[v] = (r, c)
    targets = [positions[start_color]] + [positions[c] for c in order_colors] + [positions[end_color]]
    full = []
    for i in range(len(targets) - 1):
        s = targets[i]
        t = targets[i + 1]
        q = deque([s])
        prev = {s: None}
        while q and t not in prev:
            r, c = q.popleft()
            for dr, dc in DIR4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in prev and g[nr][nc] not in wall_colors:
                    prev[(nr, nc)] = (r, c)
                    q.append((nr, nc))
        if t not in prev:
            return None
        path = []
        cur = t
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path = path[::-1]
        if full:
            full.extend(path[1:])
        else:
            full.extend(path)
    return full

def geodesic_voronoi(g: Grid, wall_colors = {5}) -> Grid:
    h, w = dims(g)
    seeds = []
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and v not in wall_colors:
                seeds.append((r, c, v))
    dist = [[None] * w for _ in range(h)]
    owners = [[set() for _ in range(w)] for __ in range(h)]
    q = deque()
    for r, c, v in seeds:
        dist[r][c] = 0
        owners[r][c] = {v}
        q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                continue
            if g[nr][nc] in wall_colors:
                continue
            nd = dist[r][c] + 1
            if dist[nr][nc] is None:
                dist[nr][nc] = nd
                owners[nr][nc] = set(owners[r][c])
                q.append((nr, nc))
            elif nd == dist[nr][nc]:
                owners[nr][nc] |= owners[r][c]
    out = copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] in wall_colors or g[r][c] != 0:
                continue
            if dist[r][c] is None:
                continue
            out[r][c] = next(iter(owners[r][c])) if len(owners[r][c]) == 1 else 0
    return out

def extract_template_and_markers(g: Grid):
    h, w = dims(g)
    sep = None
    for r in range(h):
        if all(v == 5 for v in g[r]):
            sep = r
            break
    assert sep is not None
    template = [row[:] for row in g[:sep]]
    cells = [(r, c) for r, row in enumerate(template) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    template = [row[c0:c1 + 1] for row in template[r0:r1 + 1]]
    markers = []
    for r in range(sep + 1, h):
        for c, v in enumerate(g[r]):
            if v in (1, 2, 3, 4):
                markers.append((r - (sep + 1), c, v))
    return template, markers, h - (sep + 1), w

def transform_by_marker(template: Grid, marker_color: int) -> Grid:
    if marker_color == 1:
        return template
    if marker_color == 2:
        return rotate90(template)
    if marker_color == 3:
        return rotate180(template)
    if marker_color == 4:
        return rotate270(template)
    return template

def extract_template_and_frames(g: Grid):
    h, w = dims(g)
    sep = None
    for r in range(h):
        if all(v == 5 for v in g[r]):
            sep = r
            break
    assert sep is not None
    template = [row[:] for row in g[:sep]]
    cells = [(r, c) for r, row in enumerate(template) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    template = [row[c0:c1 + 1] for row in template[r0:r1 + 1]]
    lower = [row[:] for row in g[sep + 1:]]
    frames = frame_rectangles(lower)
    return template, lower, frames

def tile_inside_frame(frame_grid: Grid, comp, template: Grid) -> Grid:
    r0, c0, r1, c1 = bbox(comp["cells"])
    interior_h = max(0, r1 - r0 - 1)
    interior_w = max(0, c1 - c0 - 1)
    out = copy_grid(frame_grid)
    th, tw = dims(template)
    for r in range(interior_h):
        for c in range(interior_w):
            val = template[r % th][c % tw]
            if val != 0:
                out[r0 + 1 + r][c0 + 1 + c] = val
    return out

def visibility_edges(g: Grid):
    comps = find_components(g)
    n = len(comps)
    comp_sets = [set(c["cells"]) for c in comps]
    edges = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            linked = False
            for r1, c1 in comps[i]["cells"]:
                for r2, c2 in comps[j]["cells"]:
                    if r1 == r2:
                        lo, hi = sorted((c1, c2))
                        ok = True
                        for cc in range(lo, hi + 1):
                            if (r1, cc) in comp_sets[i] or (r1, cc) in comp_sets[j] or g[r1][cc] == 0:
                                continue
                            ok = False
                            break
                        if ok:
                            linked = True
                            break
                    if c1 == c2:
                        lo, hi = sorted((r1, r2))
                        ok = True
                        for rr in range(lo, hi + 1):
                            if (rr, c1) in comp_sets[i] or (rr, c1) in comp_sets[j] or g[rr][c1] == 0:
                                continue
                            ok = False
                            break
                        if ok:
                            linked = True
                            break
                if linked:
                    break
            if linked:
                edges[i][j] = edges[j][i] = 1
    return comps, edges

# ---- Easy ----

def solve_easy_l01(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r0, r1, c, col in run_vertical_segments(g):
        out[r0][c] = col
        out[r1][c] = col
    return out

def solve_easy_l02(g: Grid) -> Grid:
    cnt = count_colors(g)
    return [[v if v != 0 and cnt[v] > 1 else 0 for v in row] for row in g]

def solve_easy_l03(g: Grid) -> Grid:
    out = blank(*dims(g))
    for comp in solid_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        col = comp["color"]
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if ((r - r0) + (c - c0)) % 2 == 0:
                    out[r][c] = col
    return out

def solve_easy_l04(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for comp in solid_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        if (r1 - r0) % 2 == 0 and (c1 - c0) % 2 == 0:
            rm = (r0 + r1) // 2
            cm = (c0 + c1) // 2
            for c in range(c0, c1 + 1):
                out[rm][c] = comp["color"]
            for r in range(r0, r1 + 1):
                out[r][cm] = comp["color"]
    return out

def solve_easy_l05(g: Grid) -> Grid:
    out = copy_grid(g)
    for comp in frame_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        if (r1 - r0) % 2 == 0 and (c1 - c0) % 2 == 0:
            out[(r0 + r1) // 2][(c0 + c1) // 2] = comp["color"]
    return out

def solve_easy_l06(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            col = g[r][c]
            if col != 0 and g[r - 1][c] == col and g[r + 1][c] == col and g[r][c - 1] == col and g[r][c + 1] == col:
                for dr, dc in [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    out[r + dr][c + dc] = col
    return out

def solve_easy_l07(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            col = g[r][c]
            if col != 0 and g[r - 1][c - 1] == col and g[r - 1][c + 1] == col and g[r + 1][c - 1] == col and g[r + 1][c + 1] == col:
                for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                    out[r + dr][c + dc] = col
    return out

# ---- Medium ----

def solve_medium_l08(g: Grid) -> Grid:
    h, w = dims(g)
    out = copy_grid(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and v != 5:
                q = deque([(r, c)])
                seen = {(r, c)}
                while q:
                    rr, cc = q.popleft()
                    for dr, dc in DIR4:
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in seen:
                            if g[nr][nc] == 0 or (nr, nc) == (r, c):
                                seen.add((nr, nc))
                                q.append((nr, nc))
                for rr, cc in seen:
                    if g[rr][cc] == 0:
                        out[rr][cc] = v
    return out

def solve_medium_l09(g: Grid) -> Grid:
    comps = find_components(g)
    ranked = sorted((len(c["cells"]), i) for i, c in enumerate(comps))
    median_idx = ranked[len(ranked) // 2][1]
    keep = set(comps[median_idx]["cells"])
    return [[g[r][c] if (r, c) in keep else 0 for c in range(len(g[0]))] for r in range(len(g))]

def solve_medium_l10(g: Grid) -> Grid:
    for comp in find_components(g):
        if component_holes(g, comp) == 1:
            return crop_to_cells(g, comp["cells"])
    return [[0]]

def solve_medium_l11(g: Grid) -> Grid:
    return pack_components_from_grid(g, find_components(g), key_fn=lambda c: c["color"])

def solve_medium_l12(g: Grid) -> Grid:
    out = blank(*dims(g))
    for comp in find_components(g):
        col = 2 if is_prime(len(comp["cells"])) else 8
        for r, c in comp["cells"]:
            out[r][c] = col
    return out

def solve_medium_l13(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    positions = defaultdict(list)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0:
                positions[v].append((r, c))
    for col, pts in positions.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            r0, r1b = sorted((r1, r2))
            c0, c1b = sorted((c1, c2))
            for r in range(r0, r1b + 1):
                out[r][c0] = col
                out[r][c1b] = col
            for c in range(c0, c1b + 1):
                out[r0][c] = col
                out[r1b][c] = col
    return out

def solve_medium_l14(g: Grid) -> Grid:
    template, markers, mh, mw = extract_template_and_markers(g)
    out = blank(mh, mw)
    for r, c, v in markers:
        tr = transform_by_marker(template, v)
        th, tw = dims(tr)
        r0 = r - th // 2
        c0 = c - tw // 2
        for i, row in enumerate(tr):
            for j, val in enumerate(row):
                if val != 0:
                    rr, cc = r0 + i, c0 + j
                    if 0 <= rr < mh and 0 <= cc < mw:
                        out[rr][cc] = val
    return out

# ---- Hard ----

def solve_hard_l15(g: Grid) -> Grid:
    path = shortest_path_with_waypoints(g, order_colors=[2, 3, 4], start_color=1, end_color=6, wall_colors={5})
    out = copy_grid(g)
    if path is None:
        return out
    for r, c in path:
        if out[r][c] == 0:
            out[r][c] = 8
    return out

def solve_hard_l16(g: Grid) -> Grid:
    return geodesic_voronoi(g, wall_colors={5})

def solve_hard_l17(g: Grid) -> Grid:
    template, lower, frames = extract_template_and_frames(g)
    out = copy_grid(lower)
    for comp in frames:
        t = transform_by_marker(template, comp["color"])
        out = tile_inside_frame(out, comp, t)
    return out

def solve_hard_l18(g: Grid) -> Grid:
    shapes = [(comp["color"], normalize_cells(comp["cells"])) for comp in find_components(g)]
    H = max((max(r for r, c in cells) + 1 for _, cells in shapes), default=1)
    W = max((max(c for r, c in cells) + 1 for _, cells in shapes), default=1)
    count = [[0] * W for _ in range(H)]
    for _, cells in shapes:
        for r, c in cells:
            count[r][c] += 1
    out = blank(H, W)
    for r in range(H):
        for c in range(W):
            if count[r][c] == 2:
                out[r][c] = 2
            elif count[r][c] == 3:
                out[r][c] = 8
    return out

def solve_hard_l19(g: Grid) -> Grid:
    comps, edges = visibility_edges(g)
    order = sorted(range(len(comps)), key=lambda i: (
        sum(c for r, c in comps[i]["cells"]) / len(comps[i]["cells"]),
        sum(r for r, c in comps[i]["cells"]) / len(comps[i]["cells"])
    ))
    idx_map = {old: new for new, old in enumerate(order)}
    n = len(comps)
    out = blank(n, n)
    for old_i in order:
        ni = idx_map[old_i]
        out[ni][ni] = comps[old_i]["color"]
        for old_j in order:
            nj = idx_map[old_j]
            if old_i != old_j and edges[old_i][old_j]:
                out[ni][nj] = 8
    return out

def solve_hard_l20(g: Grid) -> Grid:
    h, w = dims(g)
    mid = w // 2
    left = [row[:mid] for row in g]
    right = [row[mid:] for row in g]
    inserts = find_components(left)
    frames = frame_rectangles(right)
    out = copy_grid(right)
    used = set()
    for frame in frames:
        fr0, fc0, fr1, fc1 = bbox(frame["cells"])
        ih, iw = fr1 - fr0 - 1, fc1 - fc0 - 1
        chosen = None
        chosen_idx = None
        for i, ins in enumerate(inserts):
            if i in used:
                continue
            ir0, ic0, ir1, ic1 = bbox(ins["cells"])
            sh = [row[ic0:ic1 + 1] for row in left[ir0:ir1 + 1]]
            sh_h, sh_w = len(sh), len(sh[0])
            if (sh_h, sh_w) == (ih, iw):
                chosen = sh
                chosen_idx = i
                break
            if (sh_w, sh_h) == (ih, iw):
                chosen = rotate90(sh)
                chosen_idx = i
                break
        if chosen is None:
            continue
        used.add(chosen_idx)
        for r in range(ih):
            for c in range(iw):
                if chosen[r][c] != 0:
                    out[fr0 + 1 + r][fc0 + 1 + c] = chosen[r][c]
    return out

def solve_hard_l21(g: Grid) -> Grid:
    h, w = dims(g)
    out = copy_grid(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and v != 5:
                q = deque([(r, c)])
                dist = {(r, c): 0}
                while q:
                    rr, cc = q.popleft()
                    for dr, dc in DIR4:
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in dist:
                            if g[nr][nc] == 0:
                                dist[(nr, nc)] = dist[(rr, cc)] + 1
                                q.append((nr, nc))
                for (rr, cc), d in dist.items():
                    if g[rr][cc] == 0 and d % 2 == 0:
                        out[rr][cc] = v
    return out
