
"""Reference helper library and 21 reference solve functions for the twenty-fourth custom ARC puzzle bank.

New primitive introduced in this set:

  onion_layers(grid, colors=None, connectivity=4)

Repeatedly peel each connected nonzero component from the boundary inward and
label every occupied cell by its peel depth: 1 for the outermost layer, 2 for
the next layer, and so on. This turns thickness, nesting, inner cores, and
layer profiles into explicit symbolic structure.

All solve_* functions are deterministic reference programs for the
synthetic ARC-style tasks in set 24.
"""
from typing import List, Tuple
from collections import Counter

Grid = List[List[int]]

def blank(h, w, v=0):
    return [[v] * w for _ in range(h)]

def copy_grid(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def rot90(g):
    h, w = dims(g)
    return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]

def rotk(g, k):
    x = copy_grid(g)
    for _ in range(k % 4):
        x = rot90(x)
    return x

def bbox_of_nonzero(g, ignore=None):
    if ignore is None:
        ignore = {0, 9}
    pts = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v not in ignore]
    if not pts:
        return None
    rs = [r for r, _ in pts]
    cs = [c for _, c in pts]
    return min(rs), min(cs), max(rs), max(cs)

def crop_nonzero(g, ignore=None):
    bb = bbox_of_nonzero(g, ignore=ignore)
    if bb is None:
        return [[0]]
    r0, c0, r1, c1 = bb
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]

def pad_to(g, h, w, v=0):
    out = blank(h, w, v)
    gh, gw = dims(g)
    for r in range(gh):
        for c in range(gw):
            out[r][c] = g[r][c]
    return out

def extract_panels(grid, divider_color=9, axis='col'):
    h, w = dims(grid)
    if axis == 'col':
        divs = [c for c in range(w) if all(grid[r][c] == divider_color for r in range(h))]
        bounds = []
        prev = -1
        for c in divs + [w]:
            if c - prev - 1 > 0:
                bounds.append((prev + 1, c))
            prev = c
        return [[row[c0:c1] for row in grid] for c0, c1 in bounds]
    else:
        divs = [r for r in range(h) if all(v == divider_color for v in grid[r])]
        bounds = []
        prev = -1
        for r in divs + [h]:
            if r - prev - 1 > 0:
                bounds.append((prev + 1, r))
            prev = r
        return [grid[r0:r1] for r0, r1 in bounds]

def mask_from_grid(grid, colors=None, ignore=None):
    if ignore is None:
        ignore = {0, 9}
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            keep = (v != 0 and v not in ignore) if colors is None else (v in colors)
            out[r][c] = 1 if keep else 0
    return out

def neighbors4(r, c):
    return ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))

def component_cells_from_mask(mask):
    h, w = dims(mask)
    seen = set()
    comps = []
    for r in range(h):
        for c in range(w):
            if mask[r][c] and (r, c) not in seen:
                stack = [(r, c)]
                seen.add((r, c))
                comp = []
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for nx, ny in neighbors4(x, y):
                        if 0 <= nx < h and 0 <= ny < w and mask[nx][ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                comps.append(comp)
    comps.sort(key=lambda cells: (min(c for _, c in cells), min(r for r, _ in cells)))
    return comps

def cells_to_mask(cells, h, w):
    m = blank(h, w, 0)
    for r, c in cells:
        m[r][c] = 1
    return m

def component_masks(grid, ignore=None):
    if ignore is None:
        ignore = {0, 9}
    mask = mask_from_grid(grid, ignore=ignore)
    h, w = dims(mask)
    return [cells_to_mask(cells, h, w) for cells in component_cells_from_mask(mask)]

def onion_layers(grid, colors=None, connectivity=4):
    mask = grid if all(v in (0, 1) for row in grid for v in row) and colors is None else mask_from_grid(grid, colors=colors)
    h, w = dims(mask)
    layers = blank(h, w, 0)
    for cells in component_cells_from_mask(mask):
        cur = set(cells)
        depth = 1
        while cur:
            boundary = set()
            for r, c in cur:
                for nr, nc in neighbors4(r, c):
                    if not (0 <= nr < h and 0 <= nc < w) or (nr, nc) not in cur:
                        boundary.add((r, c))
                        break
            for r, c in boundary:
                layers[r][c] = depth
            cur -= boundary
            depth += 1
    return layers

def max_depth(grid, colors=None):
    layers = onion_layers(grid, colors=colors)
    return max((v for row in layers for v in row), default=0)

def depth_hist(grid, colors=None):
    layers = onion_layers(grid, colors=colors)
    cnt = Counter(v for row in layers for v in row if v > 0)
    if not cnt:
        return []
    return [cnt[d] for d in range(1, max(cnt) + 1)]

def grow_one_layer(grid, colors=None):
    mask = grid if all(v in (0, 1) for row in grid for v in row) and colors is None else mask_from_grid(grid, colors=colors)
    h, w = dims(mask)
    out = copy_grid(mask)
    for r in range(h):
        for c in range(w):
            if mask[r][c]:
                for nr, nc in neighbors4(r, c):
                    if 0 <= nr < h and 0 <= nc < w:
                        out[nr][nc] = 1
    return out

def exact_match(a, b):
    return a == b

def majority_grid(panels):
    h, w = dims(panels[0])
    out = blank(h, w, 0)
    n = len(panels)
    for r in range(h):
        for c in range(w):
            s = sum(1 for p in panels if p[r][c] != 0)
            out[r][c] = 1 if s * 2 >= n else 0
    return out

def majority_color(values):
    cnt = Counter(v for v in values if v != 0)
    if not cnt:
        return 0
    return max(cnt.items(), key=lambda kv: (kv[1], -kv[0]))[0]

def depth_palette_from_pair(plain_panel, colored_panel):
    layers = onion_layers(plain_panel)
    md = max((v for row in layers for v in row), default=0)
    palette = []
    for d in range(1, md + 1):
        vals = [colored_panel[r][c] for r, row in enumerate(layers) for c, v in enumerate(row) if v == d]
        palette.append(majority_color(vals))
    return palette

def apply_palette_to_panel(panel, palette):
    layers = onion_layers(panel)
    h, w = dims(panel)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            d = layers[r][c]
            if d:
                out[r][c] = palette[min(d - 1, len(palette) - 1)]
    return out

def color_of_component(grid, comp_mask):
    vals = [grid[r][c] for r, row in enumerate(comp_mask) for c, v in enumerate(row) if v]
    return majority_color(vals)

def normalized_depth_map(grid):
    return crop_nonzero(onion_layers(grid))

def solve_S24_E1(grid):
    layers = onion_layers(grid)
    out = copy_grid(grid)
    for r, row in enumerate(layers):
        for c, d in enumerate(row):
            if d == 1:
                out[r][c] = 8
    return out

def solve_S24_E2(grid):
    h, w = dims(grid)
    out = blank(h, w, 0)
    for comp in component_masks(grid):
        layers = onion_layers(comp)
        md = max((v for row in layers for v in row), default=0)
        for r in range(h):
            for c in range(w):
                if layers[r][c] == md and md > 0:
                    out[r][c] = 8
    return out

def solve_S24_E3(grid):
    vals = [max_depth(comp) for comp in component_masks(grid)]
    return [vals]

def solve_S24_E4(grid):
    layers = onion_layers(grid)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            d = layers[r][c]
            if d:
                out[r][c] = 2 if d % 2 == 1 else 3
    return out

def solve_S24_E5(grid):
    layers = onion_layers(grid)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            if layers[r][c] == 2:
                out[r][c] = 8
    return out

def solve_S24_E6(grid):
    comps = component_masks(grid)
    best = max(comps, key=max_depth)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            if best[r][c]:
                out[r][c] = 8
    return out

def solve_S24_E7(grid):
    return crop_nonzero(onion_layers(grid))

def solve_S24_M1(grid):
    palette = [v for v in grid[0] if v != 0]
    out = copy_grid(grid)
    body = grid[1:]
    layers = onion_layers(body)
    for r in range(len(body)):
        for c in range(len(body[0])):
            d = layers[r][c]
            if d:
                out[r + 1][c] = palette[min(d - 1, len(palette) - 1)]
    return out

def solve_S24_M2(grid):
    panels = extract_panels(grid, 9, 'col')
    proto = depth_hist(panels[0])
    ans = [8 if depth_hist(p) == proto else 0 for p in panels[1:]]
    return [ans]

def solve_S24_M3(grid):
    return [depth_hist(grid)]

def solve_S24_M4(grid):
    comps = component_masks(grid)
    ex, target = comps[0], comps[1]
    ex_layers = onion_layers(ex)
    ex_md = max((v for row in ex_layers for v in row), default=0)
    palette = []
    for d in range(1, ex_md + 1):
        vals = [grid[r][c] for r, row in enumerate(ex_layers) for c, v in enumerate(row) if v == d]
        palette.append(majority_color(vals))
    t_layers = onion_layers(target)
    h, w = dims(grid)
    out = copy_grid(grid)
    for r in range(h):
        for c in range(w):
            d = t_layers[r][c]
            if d:
                out[r][c] = palette[min(d - 1, len(palette) - 1)]
    return out

def solve_S24_M5(grid):
    counts = [0, 0, 0, 0]
    for comp in component_masks(grid):
        md = max_depth(comp)
        if 1 <= md <= 4:
            counts[md - 1] += 1
    return [counts]

def solve_S24_M6(grid):
    panels = extract_panels(grid, 9, 'col')
    return [[max_depth(panels[0]), max_depth(panels[1])]]

def solve_S24_M7(grid):
    comps = component_masks(grid)
    info = []
    for comp in comps:
        info.append((max_depth(comp), color_of_component(grid, comp)))
    info.sort()
    return [[color for _, color in info]]

def solve_S24_H1(grid):
    panels = extract_panels(grid, 9, 'col')
    a, b, c = panels[:3]
    cands = panels[3:]
    palette = depth_palette_from_pair(a, b)
    expected = apply_palette_to_panel(c, palette)
    return [[8 if exact_match(expected, cand) else 0 for cand in cands]]

def solve_S24_H2(grid):
    panels = extract_panels(grid, 9, 'col')
    repaired = majority_grid(panels)
    return crop_nonzero(onion_layers(repaired))

def solve_S24_H3(grid):
    panels = extract_panels(grid, 9, 'col')
    ds = [max_depth(p) for p in panels]
    return [[8 if ds[i] == ds[j] else 0 for j in range(len(ds))] for i in range(len(ds))]

def solve_S24_H4(grid):
    panels = extract_panels(grid, 9, 'col')
    query = panels[-1]
    q_hist = depth_hist(query)
    for proto in panels[:-1]:
        key = proto[0][0]
        shape = copy_grid(proto)
        shape[0][0] = 0
        if depth_hist(shape) == q_hist:
            return [[key]]
    return [[0]]

def solve_S24_H5(grid):
    panels = extract_panels(grid, 9, 'col')
    c = panels[2]
    grown = grow_one_layer(c)
    return crop_nonzero(grown)

def solve_S24_H6(grid):
    panels = extract_panels(grid, 9, 'col')
    proto = normalized_depth_map(panels[0])
    ans = []
    for cand in panels[1:]:
        dm = normalized_depth_map(cand)
        ok = any(rotk(dm, k) == proto for k in range(4))
        ans.append(8 if ok else 0)
    return [ans]

def solve_S24_H7(grid):
    panels = extract_panels(grid, 9, 'col')
    a = normalized_depth_map(panels[0])
    b = normalized_depth_map(panels[1])
    h = max(len(a), len(b))
    w = max(len(a[0]), len(b[0]))
    aa = pad_to(a, h, w, 0)
    bb = pad_to(b, h, w, 0)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            out[r][c] = min(aa[r][c], bb[r][c])
    return out
