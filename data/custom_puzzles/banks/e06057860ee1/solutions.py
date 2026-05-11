
"""Reference solvers for the twenty-second 21-task ARC-style puzzle bank.

This batch emphasizes local completion, pruning, reflection, beam propagation,
object selection, galleries, interior filling, vector cloning, keyed transforms,
frame insertion, normalized overlays, relation matrices, transform scripts,
symmetry-based assignment, and stateful pathfinding.
"""

from typing import List, Tuple, Dict
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "four_ortho_center": "Fill an empty center cell when its four orthogonal neighbors share one nonzero color.",
    "prune_singletons": "Remove every nonzero cell that has no orthogonally adjacent cell of the same color.",
    "complete_mono_2x2": "Complete any 2x2 block containing exactly three equal nonzero cells and one zero.",
    "mirror_down": "Reflect all nonzero cells in the top half across the horizontal midline into the bottom half.",
    "diag_extend_one": "Extend each same-color diagonal domino by one cell at every open end along its diagonal.",
    "top_beam_fill": "Let each top-border seed color beam downward until a blocker is hit.",
    "seed_plus_bloom": "Grow a four-arm plus around each isolated interior seed.",
    "largest_crop": "Crop out the largest monochrome object by area.",
    "aspect_recolor": "Recolor every object by its bounding-box aspect class.",
    "rect_outline_fill": "Turn each rectangular outline into a filled rectangle of the same color.",
    "area_gallery": "Crop objects and concatenate them left-to-right sorted by area.",
    "frame_seed_fill": "Fill each hollow frame interior with the color of its interior seed.",
    "vector_clone_union": "Clone the main object by the vector between two marker cells and union the result.",
    "corner_key_transform_crop": "Use a corner key to transform the main object crop and output only that crop.",
    "dual_key_frame_insert": "Select an object by one key, transform it by another, and center it inside a frame.",
    "normalize_overlay_priority": "Normalize two objects to one origin and overlay them with keyed overlap priority.",
    "key_door_bfs": "Find a shortest path that may pass through a door only after collecting the key.",
    "contact_matrix": "Output an adjacency matrix for top-left-sorted objects using orthogonal contact.",
    "transform_script_gallery": "Emit the initial object crop and each cumulative transform state in a gallery.",
    "symmetry_frame_match": "Insert each object into the frame matching its reflection-symmetry class.",
    "portal_checkpoint_path": "Find a shortest path that must visit a checkpoint and may use linked portals."
}

def blank(h: int, w: int, val: int = 0) -> Grid:
    return [[val] * w for _ in range(h)]

def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0]) if g else 0

def inb(g: Grid, r: int, c: int) -> bool:
    h, w = dims(g)
    return 0 <= r < h and 0 <= c < w

def deepcopy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]

def bbox_of_cells(cells):
    r0 = min(r for r, c in cells)
    r1 = max(r for r, c in cells)
    c0 = min(c for r, c in cells)
    c1 = max(c for r, c in cells)
    return r0, r1, c0, c1

def crop_bbox(g: Grid, bg: int = 0) -> Grid:
    h, w = dims(g)
    cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] != bg]
    if not cells:
        return [[bg]]
    r0, r1, c0, c1 = bbox_of_cells(cells)
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]

def paste(g: Grid, crop: Grid, r0: int, c0: int, overwrite_zero: bool = False) -> Grid:
    h, w = dims(g)
    ch, cw = dims(crop)
    for r in range(ch):
        for c in range(cw):
            v = crop[r][c]
            if v == 0 and not overwrite_zero:
                continue
            rr, cc = r0 + r, c0 + c
            if 0 <= rr < h and 0 <= cc < w:
                g[rr][cc] = v
    return g

def rotate90(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]

def rotate180(g: Grid) -> Grid:
    return [row[::-1] for row in g[::-1]]

def rotate270(g: Grid) -> Grid:
    return rotate90(rotate180(g))

def flip_h(g: Grid) -> Grid:
    return [row[::-1] for row in g]

def flip_v(g: Grid) -> Grid:
    return g[::-1]

def transform_by_key(g: Grid, key: int) -> Grid:
    if key == 1:
        return rotate90(g)
    if key == 2:
        return rotate180(g)
    if key == 3:
        return flip_h(g)
    if key == 4:
        return flip_v(g)
    return deepcopy_grid(g)

def find_components(g: Grid, bg: int = 0, color_sensitive: bool = True):
    h, w = dims(g)
    seen = set()
    comps = []
    for r in range(h):
        for c in range(w):
            if (r, c) in seen or g[r][c] == bg:
                continue
            color = g[r][c]
            q = deque([(r, c)])
            seen.add((r, c))
            cells = []
            while q:
                cr, cc = q.popleft()
                cells.append((cr, cc))
                for dr, dc in DIR4:
                    nr, nc = cr + dr, cc + dc
                    if not inb(g, nr, nc) or (nr, nc) in seen or g[nr][nc] == bg:
                        continue
                    if color_sensitive and g[nr][nc] != color:
                        continue
                    seen.add((nr, nc))
                    q.append((nr, nc))
            comps.append({"color": color, "cells": cells})
    return comps

def crop_component(g: Grid, comp) -> Grid:
    cells = comp["cells"]
    r0, r1, c0, c1 = bbox_of_cells(cells)
    out = blank(r1 - r0 + 1, c1 - c0 + 1, 0)
    for r, c in cells:
        out[r - r0][c - c0] = g[r][c]
    return out

def is_rect_outline(comp) -> bool:
    cells = set(comp["cells"])
    r0, r1, c0, c1 = bbox_of_cells(comp["cells"])
    outline = set()
    for c in range(c0, c1 + 1):
        outline.add((r0, c))
        outline.add((r1, c))
    for r in range(r0, r1 + 1):
        outline.add((r, c0))
        outline.add((r, c1))
    return cells == outline

def center_in_rect(g: Grid, crop: Grid, r0: int, r1: int, c0: int, c1: int):
    ch, cw = dims(crop)
    ih, iw = (r1 - r0 + 1), (c1 - c0 + 1)
    sr = r0 + (ih - ch) // 2
    sc = c0 + (iw - cw) // 2
    return paste(g, crop, sr, sc)

def normalize_crop(comp_crop: Grid) -> Grid:
    return crop_bbox(comp_crop, 0)

def object_symmetry_class(crop: Grid) -> str:
    lr = crop == flip_h(crop)
    tb = crop == flip_v(crop)
    if lr and tb:
        return "both"
    if lr:
        return "lr"
    if tb:
        return "tb"
    return "none"

def overlay_priority(a: Grid, b: Grid, first_wins: bool = True) -> Grid:
    ha, wa = dims(a)
    hb, wb = dims(b)
    h, w = max(ha, hb), max(wa, wb)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            va = a[r][c] if r < ha and c < wa else 0
            vb = b[r][c] if r < hb and c < wb else 0
            if va and vb:
                out[r][c] = va if first_wins else vb
            else:
                out[r][c] = va or vb
    return crop_bbox(out, 0)

def gallery(crops: List[Grid]) -> Grid:
    if not crops:
        return [[0]]
    h = max(len(c) for c in crops)
    total_w = sum(len(c[0]) for c in crops) + (len(crops) - 1)
    out = blank(h, total_w, 0)
    x = 0
    for i, crop in enumerate(crops):
        paste(out, crop, 0, x)
        x += len(crop[0])
        if i + 1 < len(crops):
            x += 1
    return out

def solve_easy_p01(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if g[r][c] != 0:
                continue
            vals = [g[r - 1][c], g[r + 1][c], g[r][c - 1], g[r][c + 1]]
            colors = set(vals)
            if len(colors) == 1 and 0 not in colors:
                out[r][c] = vals[0]
    return out

def solve_easy_p02(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            if any(inb(g, r + dr, c + dc) and g[r + dr][c + dc] == v for dr, dc in DIR4):
                out[r][c] = v
    return out

def solve_easy_p03(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h - 1):
        for c in range(w - 1):
            vals = [g[r][c], g[r][c + 1], g[r + 1][c], g[r + 1][c + 1]]
            nz = [v for v in vals if v != 0]
            if len(nz) == 3 and len(set(nz)) == 1:
                color = nz[0]
                if g[r][c] == 0:
                    out[r][c] = color
                if g[r][c + 1] == 0:
                    out[r][c + 1] = color
                if g[r + 1][c] == 0:
                    out[r + 1][c] = color
                if g[r + 1][c + 1] == 0:
                    out[r + 1][c + 1] = color
    return out

def solve_easy_p04(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h // 2):
        for c in range(w):
            if g[r][c] != 0:
                out[h - 1 - r][c] = g[r][c]
    return out

def solve_easy_p05(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            color = g[r][c]
            if color == 0:
                continue
            for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                r1, c1 = r + dr, c + dc
                r2, c2 = r + 2 * dr, c + 2 * dc
                rp, cp = r - dr, c - dc
                if inb(g, r1, c1) and inb(g, r2, c2) and g[r1][c1] == color and g[r2][c2] == 0:
                    if not inb(g, rp, cp) or g[rp][cp] != color:
                        out[r2][c2] = color
    return out

def solve_easy_p06(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for c in range(w):
        color = g[0][c]
        if color in (0, 9):
            continue
        for r in range(1, h):
            if g[r][c] == 9:
                break
            out[r][c] = color
    return out

def solve_easy_p07(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            color = g[r][c]
            if color == 0:
                continue
            if all(g[r + dr][c + dc] == 0 for dr, dc in DIR4):
                for dr, dc in DIR4:
                    out[r + dr][c + dc] = color
    return out

def solve_medium_p01(g: Grid) -> Grid:
    comps = find_components(g, 0, True)
    comps.sort(key=lambda comp: (-len(comp["cells"]), bbox_of_cells(comp["cells"])))
    return crop_component(g, comps[0])

def solve_medium_p02(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w, 0)
    for comp in find_components(g, 0, True):
        r0, r1, c0, c1 = bbox_of_cells(comp["cells"])
        hh, ww = r1 - r0 + 1, c1 - c0 + 1
        color = 4 if hh == ww else (2 if ww > hh else 3)
        for r, c in comp["cells"]:
            out[r][c] = color
    return out

def solve_medium_p03(g: Grid) -> Grid:
    out = deepcopy_grid(g)
    for comp in find_components(g, 0, True):
        if not is_rect_outline(comp):
            continue
        color = comp["color"]
        r0, r1, c0, c1 = bbox_of_cells(comp["cells"])
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                out[r][c] = color
    return out

def solve_medium_p04(g: Grid) -> Grid:
    comps = find_components(g, 0, True)
    comps.sort(key=lambda comp: (-len(comp["cells"]), bbox_of_cells(comp["cells"])))
    crops = [crop_component(g, comp) for comp in comps]
    return gallery(crops)

def solve_medium_p05(g: Grid) -> Grid:
    out = deepcopy_grid(g)
    comps = find_components(g, 0, True)
    for comp in comps:
        if not is_rect_outline(comp):
            continue
        r0, r1, c0, c1 = bbox_of_cells(comp["cells"])
        seeds = []
        for r in range(r0 + 1, r1):
            for c in range(c0 + 1, c1):
                if g[r][c] != 0 and g[r][c] != comp["color"]:
                    seeds.append((r, c, g[r][c]))
        if len(seeds) >= 1:
            seed_color = seeds[0][2]
            for r in range(r0 + 1, r1):
                for c in range(c0 + 1, c1):
                    out[r][c] = seed_color
    return out

def solve_medium_p06(g: Grid) -> Grid:
    h, w = dims(g)
    markers = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 9]
    markers.sort()
    (r0, c0), (r1, c1) = markers[:2]
    dr, dc = r1 - r0, c1 - c0
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or v == 9:
                continue
            out[r][c] = v
            rr, cc = r + dr, c + dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = v
    return out

def solve_medium_p07(g: Grid) -> Grid:
    key = g[0][0]
    h, w = dims(g)
    work = deepcopy_grid(g)
    work[0][0] = 0
    crop = crop_bbox(work, 0)
    return transform_by_key(crop, key)

def solve_hard_p01(g: Grid) -> Grid:
    h, w = dims(g)
    select_color = g[0][0]
    tkey = g[0][w - 1]
    work = deepcopy_grid(g)
    work[0][0] = 0
    work[0][w - 1] = 0
    comps = find_components(work, 0, True)
    target = None
    frame = None
    for comp in comps:
        if is_rect_outline(comp):
            frame = comp
        elif comp["color"] == select_color:
            if target is None or len(comp["cells"]) > len(target["cells"]):
                target = comp
    out = blank(h, w, 0)
    if frame is not None:
        for r, c in frame["cells"]:
            out[r][c] = frame["color"]
        r0, r1, c0, c1 = bbox_of_cells(frame["cells"])
        interior = (r0 + 1, r1 - 1, c0 + 1, c1 - 1)
        transformed = transform_by_key(crop_component(work, target), tkey)
        center_in_rect(out, transformed, *interior)
    return out

def solve_hard_p02(g: Grid) -> Grid:
    h, w = dims(g)
    key = g[0][0]
    work = deepcopy_grid(g)
    work[0][0] = 0
    comps = find_components(work, 0, True)
    comps.sort(key=lambda comp: bbox_of_cells(comp["cells"]))
    a = crop_component(work, comps[0])
    b = crop_component(work, comps[1])
    return overlay_priority(a, b, first_wins=(key == 1))

def solve_hard_p03(g: Grid) -> Grid:
    h, w = dims(g)
    start = goal = key = None
    for r in range(h):
        for c in range(w):
            if g[r][c] == 2:
                start = (r, c)
            elif g[r][c] == 3:
                goal = (r, c)
            elif g[r][c] == 5:
                key = (r, c)
    q = deque([(start[0], start[1], 0)])
    prev = {(start[0], start[1], 0): None}
    end_state = None
    while q:
        r, c, has_key = q.popleft()
        if (r, c) == goal and has_key:
            end_state = (r, c, has_key)
            break
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if not inb(g, nr, nc) or g[nr][nc] == 8:
                continue
            if g[nr][nc] == 6 and not has_key:
                continue
            nk = has_key or ((nr, nc) == key)
            st = (nr, nc, 1 if nk else 0)
            if st not in prev:
                prev[st] = (r, c, has_key)
                q.append(st)
    out = deepcopy_grid(g)
    if end_state is None:
        return out
    cur = end_state
    while cur is not None:
        r, c, hk = cur
        if out[r][c] == 0:
            out[r][c] = 4
        cur = prev[cur]
    return out

def solve_hard_p04(g: Grid) -> Grid:
    comps = find_components(g, 0, True)
    comps.sort(key=lambda comp: bbox_of_cells(comp["cells"]))
    n = len(comps)
    out = blank(n, n, 0)
    cellsets = [set(comp["cells"]) for comp in comps]
    for i in range(n):
        out[i][i] = 1
    for i in range(n):
        for j in range(i + 1, n):
            touch = False
            for r, c in cellsets[i]:
                if any((r + dr, c + dc) in cellsets[j] for dr, dc in DIR4):
                    touch = True
                    break
            if touch:
                out[i][j] = out[j][i] = 2
    return out

def solve_hard_p05(g: Grid) -> Grid:
    h, w = dims(g)
    keys = [v for v in g[0] if v != 0]
    work = [row[:] for row in g[1:]]
    crop = crop_bbox(work, 0)
    crops = [crop]
    cur = crop
    for k in keys:
        cur = transform_by_key(cur, k)
        crops.append(cur)
    return gallery(crops)

def solve_hard_p06(g: Grid) -> Grid:
    h, w = dims(g)
    comps = find_components(g, 0, True)
    frames = []
    objs = []
    for comp in comps:
        if is_rect_outline(comp):
            frames.append(comp)
        else:
            objs.append(comp)
    mapping = {"lr": 2, "tb": 3, "both": 4}
    chosen = {}
    for obj in objs:
        cls = object_symmetry_class(crop_component(g, obj))
        if cls in mapping:
            chosen[mapping[cls]] = obj
    out = blank(h, w, 0)
    for fr in frames:
        for r, c in fr["cells"]:
            out[r][c] = fr["color"]
        target = chosen.get(fr["color"])
        if target is not None:
            r0, r1, c0, c1 = bbox_of_cells(fr["cells"])
            center_in_rect(out, crop_component(g, target), r0 + 1, r1 - 1, c0 + 1, c1 - 1)
    return out

def solve_hard_p07(g: Grid) -> Grid:
    h, w = dims(g)
    start = goal = checkpoint = None
    portal_groups = defaultdict(list)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 2:
                start = (r, c)
            elif v == 3:
                goal = (r, c)
            elif v == 5:
                checkpoint = (r, c)
            elif v in (6, 7):
                portal_groups[v].append((r, c))

    def portal_dest(pos):
        r, c = pos
        v = g[r][c]
        if v not in portal_groups or len(portal_groups[v]) != 2:
            return pos
        a, b = portal_groups[v]
        return b if pos == a else a

    q = deque([(start[0], start[1], 0)])
    prev = {(start[0], start[1], 0): None}
    end_state = None
    while q:
        r, c, hit = q.popleft()
        if (r, c) == goal and hit:
            end_state = (r, c, hit)
            break
        for dr, dc in DIR4:
            nr, nc = r + dr, c + dc
            if not inb(g, nr, nc) or g[nr][nc] == 8:
                continue
            hit2 = hit or ((nr, nc) == checkpoint)
            if g[nr][nc] in (6, 7):
                nr, nc = portal_dest((nr, nc))
                hit2 = hit2 or ((nr, nc) == checkpoint)
            st = (nr, nc, 1 if hit2 else 0)
            if st not in prev:
                prev[st] = (r, c, hit)
                q.append(st)
    out = deepcopy_grid(g)
    if end_state is None:
        return out
    cur = end_state
    while cur is not None:
        r, c, hit = cur
        if out[r][c] == 0:
            out[r][c] = 4
        cur = prev[cur]
    return out
