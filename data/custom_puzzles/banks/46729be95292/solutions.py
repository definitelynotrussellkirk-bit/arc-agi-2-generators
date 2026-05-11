
"""Reference solvers for the eighteenth 21-task ARC-style puzzle bank.

This batch pushes into a different slice of the ARC space: periodic extrapolation, midpoint logic,
distance bands, bounding-box abstraction, row-wise control, flood fills, morphological shells,
relative-offset transfer, transform scripts, extraction galleries, keyed frame embedding, portals,
radial packing, transform timelines, gate-aware floods, dihedral matching, and parity wavefronts.
"""
from typing import List, Dict, Tuple
from collections import deque, defaultdict
import math

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

NEW_PRIMITIVES = {
    'periodic_ray': 'Infer a step from two same-color seeds and continue stamping the color at that period.',
    'segment_midpoint': 'Fill the midpoint of a clear straight segment between matching endpoints.',
    'distance_band': 'Paint cells at an exact Manhattan distance from a seed.',
    'bbox_corners': 'Reduce each object to the four corners of its bounding box.',
    'diagonal_line': 'Complete the full main diagonal that passes through each seed.',
    'row_leader_recolor': 'Use the leftmost nonzero cell in a row as that row’s recolor key.',
    'opposite_pair_fill': 'Fill a zero cell when opposite neighbors horizontally or vertically agree.',
    'room_flood': 'Flood the zero cells inside a walled room from its seed color.',
    'column_histogram': 'Summarize an object by bottom-aligned bars whose heights equal per-column counts.',
    'transform_script': 'Apply a left-to-right sequence of transform codes to a cropped object.',
    'contact_shell': 'Replace an object by its one-step orthogonal shell.',
    'offset_transfer': 'Copy all payload offsets from one anchor to another anchor.',
    'pivot_rays': 'Cast four orthogonal rays from each pivot until a wall or obstacle.',
    'frame_gallery': 'Extract frame interiors and concatenate them as a gallery.',
    'keyed_frame_embed': 'Use a marker above a frame to choose which source object to center inside it.',
    'portal_bfs': 'Route a shortest path while teleporting across matched portal pairs.',
    'radial_order_pack': 'Sort objects by angle around a hub and pack them into a gallery.',
    'transform_timeline': 'Emit every intermediate transformed state, not only the final one.',
    'gated_flood': 'Flood through walls only at gate cells whose color matches the seed.',
    'dihedral_select': 'Find which candidate matches a guide under rotation or reflection.',
    'parity_wavefront': 'Color reachable cells by even or odd shortest-path distance from a seed.'
}


def blank(h, w, v=0):
    return [[v for _ in range(w)] for _ in range(h)]


def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0]) if g else 0


def inb(g, r, c):
    h, w = dims(g)
    return 0 <= r < h and 0 <= c < w


def bbox(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop(g, r0, c0, r1, c1):
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def crop_component(g, cells):
    r0, c0, r1, c1 = bbox(cells)
    return crop(g, r0, c0, r1, c1)


def stamp(g, top, left, shape, color=None):
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if color is None:
                if val:
                    g[top+r][left+c] = val
            else:
                if val:
                    g[top+r][left+c] = color
    return g


def rotate90(g):
    h, w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g):
    return [row[::-1] for row in g[::-1]]


def rotate270(g):
    return rotate90(rotate180(g))


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def all_transforms(g):
    x = copy_grid(g)
    outs = []
    for _ in range(4):
        outs.append(x)
        outs.append(flip_h(x))
        x = rotate90(x)
    uniq = []
    seen = set()
    for m in outs:
        key = tuple(tuple(row) for row in m)
        if key not in seen:
            uniq.append(m)
            seen.add(key)
    return uniq


def binary_crop(g):
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    if not cells:
        return [[]]
    r0, c0, r1, c1 = bbox(cells)
    out = crop(g, r0, c0, r1, c1)
    return [[1 if v else 0 for v in row] for row in out]


def components(g):
    h, w = dims(g)
    seen = [[False]*w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c] == 0:
                continue
            color = g[r][c]
            q = [(r, c)]
            seen[r][c] = True
            cells = []
            while q:
                rr, cc = q.pop()
                cells.append((rr, cc))
                for dr, dc in DIR4:
                    nr, nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == color:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append({'color': color, 'cells': cells})
    return comps


def draw_frame(g, r0, c0, r1, c1, color=5):
    for c in range(c0, c1+1):
        g[r0][c] = color
        g[r1][c] = color
    for r in range(r0, r1+1):
        g[r][c0] = color
        g[r][c1] = color
    return g


def detect_frames(g, frame_color=5):
    comps = components(g)
    frames = []
    for comp in comps:
        if comp['color'] != frame_color:
            continue
        r0, c0, r1, c1 = bbox(comp['cells'])
        border = {(r, c) for r in range(r0, r1+1) for c in range(c0, c1+1)
                  if r in (r0, r1) or c in (c0, c1)}
        if set(comp['cells']) == border and r1-r0 >= 2 and c1-c0 >= 2:
            frames.append({'bbox': (r0, c0, r1, c1), 'cells': comp['cells']})
    frames.sort(key=lambda f: (f['bbox'][1], f['bbox'][0]))
    return frames


def pack_gallery(shapes, align='top', sep=1):
    if not shapes:
        return [[]]
    heights = [len(s) for s in shapes]
    widths = [len(s[0]) if s else 0 for s in shapes]
    H = max(heights)
    W = sum(widths) + sep * (len(shapes)-1)
    out = blank(H, W, 0)
    x = 0
    for s in shapes:
        h = len(s)
        w = len(s[0]) if s else 0
        y = 0 if align == 'top' else H - h
        for r in range(h):
            for c in range(w):
                if s[r][c] != 0:
                    out[y+r][x+c] = s[r][c]
        x += w + sep
    return out


def apply_code(shape, code):
    if code == 1:
        return rotate90(shape)
    if code == 2:
        return flip_h(shape)
    if code == 3:
        return rotate180(shape)
    if code == 4:
        return flip_v(shape)
    return copy_grid(shape)


def find_singletons(g, colors=None):
    cells = []
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and (colors is None or v in colors):
                cells.append((r, c, v))
    return cells


def solve_easy_p01(g):
    out = copy_grid(g)
    h, w = dims(g)
    for r in range(h):
        by_color = defaultdict(list)
        for c, v in enumerate(g[r]):
            if v:
                by_color[v].append(c)
        for color, cols in by_color.items():
            if len(cols) == 2:
                c1, c2 = sorted(cols)
                if all(g[r][cc] == 0 for cc in range(c1+1, c2)):
                    step = c2 - c1
                    k = c2 + step
                    while k < w:
                        out[r][k] = color
                        k += step
    return out


def solve_easy_p02(g):
    out = copy_grid(g)
    h, w = dims(g)
    # horizontal
    for r in range(h):
        for c1 in range(w):
            v = g[r][c1]
            if v == 0:
                continue
            for c2 in range(c1+2, w):
                if g[r][c2] == v and (c2-c1) % 2 == 0 and all(g[r][cc] == 0 for cc in range(c1+1, c2)):
                    out[r][(c1+c2)//2] = v
    # vertical
    for c in range(w):
        for r1 in range(h):
            v = g[r1][c]
            if v == 0:
                continue
            for r2 in range(r1+2, h):
                if g[r2][c] == v and (r2-r1) % 2 == 0 and all(g[rr][c] == 0 for rr in range(r1+1, r2)):
                    out[(r1+r2)//2][c] = v
    return out


def solve_easy_p03(g):
    out = copy_grid(g)
    h, w = dims(g)
    seeds = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    for r, c, v in seeds:
        for dr in range(-2, 3):
            dc = 2 - abs(dr)
            for s in (-1, 1):
                rr, cc = r + dr, c + s*dc
                if inb(g, rr, cc) and out[rr][cc] == 0:
                    out[rr][cc] = v
    return out


def solve_easy_p04(g):
    out = blank(*dims(g), 0)
    for comp in components(g):
        r0, c0, r1, c1 = bbox(comp['cells'])
        for rr, cc in [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]:
            out[rr][cc] = comp['color']
    return out


def solve_easy_p05(g):
    out = copy_grid(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            d = r - c
            for rr in range(h):
                cc = rr - d
                if 0 <= cc < w:
                    out[rr][cc] = v
    return out


def solve_easy_p06(g):
    out = copy_grid(g)
    h, w = dims(g)
    for r in range(h):
        leader = None
        for c in range(w):
            if g[r][c] != 0:
                leader = g[r][c]
                break
        if leader is None:
            continue
        for c in range(w):
            if g[r][c] != 0:
                out[r][c] = leader
    return out


def solve_easy_p07(g):
    out = copy_grid(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                continue
            fill = 0
            if c-1 >= 0 and c+1 < w and g[r][c-1] == g[r][c+1] != 0:
                fill = g[r][c-1]
            if r-1 >= 0 and r+1 < h and g[r-1][c] == g[r+1][c] != 0:
                if fill == 0 or fill == g[r-1][c]:
                    fill = g[r-1][c]
            if fill:
                out[r][c] = fill
    return out


def solve_medium_p01(g):
    out = copy_grid(g)
    h, w = dims(g)
    seeds = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 5)]
    for sr, sc, color in seeds:
        q = deque([(sr, sc)])
        seen = {(sr, sc)}
        while q:
            r, c = q.popleft()
            for dr, dc in DIR4:
                nr, nc = r+dr, c+dc
                if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in seen and out[nr][nc] != 5:
                    if out[nr][nc] == 0:
                        out[nr][nc] = color
                        seen.add((nr, nc))
                        q.append((nr, nc))
                    elif out[nr][nc] == color:
                        seen.add((nr, nc))
                        q.append((nr, nc))
    return out


def solve_medium_p02(g):
    comps = components(g)
    comp = max(comps, key=lambda x: len(x['cells']))
    obj = crop_component(g, comp['cells'])
    h, w = dims(obj)
    counts = [sum(1 for r in range(h) if obj[r][c] != 0) for c in range(w)]
    H = max(counts)
    out = blank(H, w, 0)
    color = comp['color']
    for c, cnt in enumerate(counts):
        for k in range(cnt):
            out[H-1-k][c] = color
    return out


def solve_medium_p03(g):
    script = [v for v in g[0] if v != 0]
    comps = [comp for comp in components(g) if not all(r == 0 for r, c in comp['cells'])]
    comp = max(comps, key=lambda x: len(x['cells']))
    obj = crop_component(g, comp['cells'])
    cur = obj
    for code in script:
        cur = apply_code(cur, code)
    return cur


def solve_medium_p04(g):
    h, w = dims(g)
    occupied = {(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0}
    out = blank(h, w, 0)
    for comp in components(g):
        color = comp['color']
        shell = set()
        for r, c in comp['cells']:
            for dr, dc in DIR4:
                nr, nc = r+dr, c+dc
                if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in occupied:
                    shell.add((nr, nc))
        for r, c in shell:
            out[r][c] = color
    return out


def solve_medium_p05(g):
    h, w = dims(g)
    anchors = {v: (r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v in (1, 2)}
    a1 = anchors[1]
    a2 = anchors[2]
    out = blank(h, w, 0)
    out[a2[0]][a2[1]] = 2
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v in (0, 1, 2):
                continue
            dr, dc = r - a1[0], c - a1[1]
            rr, cc = a2[0] + dr, a2[1] + dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = v
    return out


def solve_medium_p06(g):
    out = copy_grid(g)
    h, w = dims(g)
    pivots = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 5)]
    for r, c, color in pivots:
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            while 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0:
                out[nr][nc] = color
                nr += dr
                nc += dc
    return out


def solve_medium_p07(g):
    frames = detect_frames(g, 5)
    shapes = []
    for fr in frames:
        r0, c0, r1, c1 = fr['bbox']
        shapes.append(crop(g, r0+1, c0+1, r1-1, c1-1))
    return pack_gallery(shapes, align='top', sep=1)


def solve_hard_p01(g):
    h, w = dims(g)
    frames = detect_frames(g, 5)
    source_comps = [comp for comp in components(g) if comp['color'] != 5]
    sources = {comp['color']: crop_component(g, comp['cells']) for comp in source_comps if len(comp['cells']) > 1}
    out = blank(h, w, 0)
    for fr in frames:
        r0, c0, r1, c1 = fr['bbox']
        draw_frame(out, r0, c0, r1, c1, 5)
        marker_c = (c0 + c1) // 2
        marker_r = r0 - 1
        key = g[marker_r][marker_c] if marker_r >= 0 else 0
        if key in sources:
            shape = sources[key]
            ih, iw = r1-r0-1, c1-c0-1
            sh, sw = dims(shape)
            top = r0 + 1 + (ih - sh) // 2
            left = c0 + 1 + (iw - sw) // 2
            stamp(out, top, left, shape)
    return out


def solve_hard_p02(g):
    h, w = dims(g)
    start = goal = None
    portals = defaultdict(list)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 2:
                start = (r, c)
            elif v == 3:
                goal = (r, c)
            elif v in (4, 6, 7, 8, 9):
                portals[v].append((r, c))
    q = deque([start])
    prev = {start: None}
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            break
        neighbors = []
        for dr, dc in DIR4:
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 5:
                neighbors.append((nr, nc))
        v = g[r][c]
        if v in portals and len(portals[v]) == 2:
            a, b = portals[v]
            neighbors.append(b if (r, c) == a else a)
        for nb in neighbors:
            if nb not in prev:
                prev[nb] = (r, c)
                q.append(nb)
    out = copy_grid(g)
    cur = goal
    while cur is not None:
        r, c = cur
        if out[r][c] == 0:
            out[r][c] = 8
        cur = prev[cur]
    return out


def solve_hard_p03(g):
    hub = None
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 9:
                hub = (r, c)
                break
        if hub:
            break
    objs = []
    for comp in components(g):
        if comp['color'] == 9:
            continue
        shape = crop_component(g, comp['cells'])
        rs = [r for r, c in comp['cells']]
        cs = [c for r, c in comp['cells']]
        cr = sum(rs) / len(rs)
        cc = sum(cs) / len(cs)
        ang = (math.atan2(cc - hub[1], -(cr - hub[0])) + 2*math.pi) % (2*math.pi)
        objs.append((ang, shape))
    objs.sort(key=lambda x: x[0])
    return pack_gallery([s for _, s in objs], align='top', sep=1)


def solve_hard_p04(g):
    script = [v for v in g[0] if v != 0]
    comps = [comp for comp in components(g) if not all(r == 0 for r, c in comp['cells'])]
    comp = max(comps, key=lambda x: len(x['cells']))
    cur = crop_component(g, comp['cells'])
    states = [cur]
    for code in script:
        cur = apply_code(cur, code)
        states.append(cur)
    return pack_gallery(states, align='top', sep=1)


def solve_hard_p05(g):
    out = copy_grid(g)
    h, w = dims(g)
    seeds = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 5)]
    for sr, sc, color in seeds:
        q = deque([(sr, sc)])
        seen = {(sr, sc)}
        while q:
            r, c = q.popleft()
            for dr, dc in DIR4:
                nr, nc = r+dr, c+dc
                if not (0 <= nr < h and 0 <= nc < w) or (nr, nc) in seen:
                    continue
                cell = g[nr][nc]
                if cell == 0 or cell == color:
                    seen.add((nr, nc))
                    q.append((nr, nc))
                    if out[nr][nc] == 0:
                        out[nr][nc] = color
    return out


def solve_hard_p06(g):
    comps = components(g)
    guide = next(comp for comp in comps if comp['color'] == 1)
    guide_bin = binary_crop(crop_component(g, guide['cells']))
    for comp in comps:
        if comp['color'] == 1:
            continue
        shape = crop_component(g, comp['cells'])
        shape_bin = [[1 if v else 0 for v in row] for row in shape]
        for t in all_transforms(shape_bin):
            if t == guide_bin:
                out = [[comp['color'] if v else 0 for v in row] for row in t]
                return out
    return [[]]


def solve_hard_p07(g):
    out = copy_grid(g)
    h, w = dims(g)
    seed = None
    for r in range(h):
        for c in range(w):
            if g[r][c] not in (0, 5):
                seed = (r, c, g[r][c])
                break
        if seed:
            break
    sr, sc, color = seed
    q = deque([(sr, sc)])
    dist = {(sr, sc): 0}
    while q:
        r, c = q.popleft()
        for dr, dc in DIR4:
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 5 and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))
    for (r, c), d in dist.items():
        if g[r][c] == 0:
            out[r][c] = color if d % 2 == 0 else 8
    return out
