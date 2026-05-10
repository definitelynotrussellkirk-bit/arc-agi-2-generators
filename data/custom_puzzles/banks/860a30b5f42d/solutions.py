
"""Reference solvers for the twenty-third 21-task ARC-style puzzle bank.

This batch emphasizes diagonal agreement, shadow casting, topological filters,
gap bridging, square-derived blooms, knight offsets, barbell completion,
border-touch classification, compartment gravity, rectangle generation from
marker pairs, count-key selection, geometric docking, object galleries,
mirror laser tracing, multi-key pathfinding, visibility reasoning,
area-rank frame assignment, boolean composition, orbit stamping, and
multi-frame transform stamping.
"""

from typing import List, Tuple, Dict, Set
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
KNIGHT = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

NEW_PRIMITIVES = {
    "diag_agreement_fill": "Fill an empty cell when its four diagonal neighbors all share one nonzero color.",
    "right_shadow_cast": "Cast each seed color rightward through empty cells until a blocker or the border.",
    "cross_core_filter": "Keep only cells that have same-color neighbors in all four cardinal directions.",
    "exact_two_gap_bridge": "Bridge same-color endpoints separated by exactly two empty cells in a row or column.",
    "square_corner_bloom": "For every solid monochrome 2x2 block, bloom one same-color cell on each diagonal corner.",
    "knight_bloom": "Around each isolated seed, stamp the eight knight-move positions with the seed color.",
    "barbell_fill": "When two same-color 2x2 blocks align, fill the rectangle that connects them.",
    "border_touch_rank": "Recolor each object by how many outer borders it touches.",
    "compartment_gravity": "Let colored cells fall within each wall-bounded vertical compartment.",
    "pair_bbox_fill": "For each color appearing exactly twice as markers, fill the rectangle spanning the pair.",
    "count_key_crop": "Use the count of top-row key markers to select the left-to-right object to crop out.",
    "nearest_corner_dock": "Move the single object to the geometrically nearest corner of the same canvas.",
    "largest_mirror_crop": "Select the largest object, mirror its tight crop left-to-right, and output only that crop.",
    "height_gallery": "Crop objects and lay them out left-to-right, bottom-aligned, sorted by height.",
    "mirror_laser": "Trace a border-launched laser through slash and backslash mirrors until it exits or hits a wall.",
    "dual_key_door_bfs": "Find the shortest path to the goal while collecting up to two keys that unlock matching doors.",
    "visibility_matrix": "Output a matrix showing which objects have unobstructed orthogonal line-of-sight.",
    "area_rank_frame_assign": "Assign cropped objects to hollow frames by matching object-area rank to frame-area rank.",
    "dual_key_boolean": "Transform one normalized object by a key, then combine it with another via a keyed boolean op.",
    "orbit_stamp": "Stamp four rotated copies of a template around an anchor point on the diagonals.",
    "frame_key_stamp": "Stamp a template into each frame after applying the transform indicated by that frame's key."
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

def bbox_of_cells(cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def crop_bbox(g: Grid, bbox: Tuple[int, int, int, int]) -> Grid:
    r0, r1, c0, c1 = bbox
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def paste(dst: Grid, src: Grid, top: int, left: int, transparent: int = 0) -> Grid:
    h, w = dims(dst)
    sh, sw = dims(src)
    out = deepcopy_grid(dst)
    for r in range(sh):
        for c in range(sw):
            rr, cc = top + r, left + c
            if 0 <= rr < h and 0 <= cc < w and src[r][c] != transparent:
                out[rr][cc] = src[r][c]
    return out

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
        return deepcopy_grid(g)
    if key == 2:
        return rotate90(g)
    if key == 3:
        return flip_h(g)
    if key == 4:
        return flip_v(g)
    if key == 5:
        return rotate180(g)
    if key == 6:
        return rotate270(g)
    return deepcopy_grid(g)

def find_components(g: Grid, include_zero: bool = False) -> List[Dict]:
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            if not include_zero and g[r][c] == 0:
                continue
            color = g[r][c]
            q = deque([(r, c)])
            seen[r][c] = True
            cells = []
            while q:
                rr, cc = q.popleft()
                cells.append((rr, cc))
                for dr, dc in DIR4:
                    nr, nc = rr + dr, cc + dc
                    if inb(g, nr, nc) and not seen[nr][nc] and g[nr][nc] == color:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append({"color": color, "cells": cells, "bbox": bbox_of_cells(cells), "size": len(cells)})
    return comps

def crop_component(g: Grid, comp: Dict) -> Grid:
    r0, r1, c0, c1 = comp["bbox"]
    out = blank(r1-r0+1, c1-c0+1)
    for r, c in comp["cells"]:
        out[r-r0][c-c0] = g[r][c]
    return out

def center_in_rect(src: Grid, out: Grid, bbox: Tuple[int, int, int, int]) -> Grid:
    r0, r1, c0, c1 = bbox
    ih, iw = r1-r0-1, c1-c0-1
    sh, sw = dims(src)
    top = r0 + 1 + max(0, (ih - sh) // 2)
    left = c0 + 1 + max(0, (iw - sw) // 2)
    return paste(out, src, top, left)

def normalize_crop(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox_of_cells(cells))

def gallery(crops: List[Grid], gap: int = 1, valign: str = "bottom") -> Grid:
    if not crops:
        return [[0]]
    heights = [len(c) for c in crops]
    widths = [len(c[0]) for c in crops]
    H = max(heights)
    W = sum(widths) + gap * (len(crops) - 1)
    out = blank(H, W)
    cur = 0
    for crop in crops:
        h, w = dims(crop)
        top = 0 if valign == "top" else H - h
        out = paste(out, crop, top, cur)
        cur += w + gap
    return out

def line_of_sight(g: Grid, comp_a: Dict, comp_b: Dict) -> bool:
    cells_a = comp_a["cells"]
    cells_b = set(comp_b["cells"])
    h, w = dims(g)
    for ra, ca in cells_a:
        # right
        c = ca + 1
        seen_zero = False
        while c < w and g[ra][c] == 0:
            seen_zero = True
            c += 1
        if c < w and (ra, c) in cells_b and seen_zero:
            return True
        # left
        c = ca - 1
        seen_zero = False
        while c >= 0 and g[ra][c] == 0:
            seen_zero = True
            c -= 1
        if c >= 0 and (ra, c) in cells_b and seen_zero:
            return True
        # down
        r = ra + 1
        seen_zero = False
        while r < h and g[r][ca] == 0:
            seen_zero = True
            r += 1
        if r < h and (r, ca) in cells_b and seen_zero:
            return True
        # up
        r = ra - 1
        seen_zero = False
        while r >= 0 and g[r][ca] == 0:
            seen_zero = True
            r -= 1
        if r >= 0 and (r, ca) in cells_b and seen_zero:
            return True
    return False

def frame_bboxes(g: Grid, frame_color: int = 5) -> List[Tuple[int,int,int,int]]:
    comps = [c for c in find_components(g) if c["color"] == frame_color]
    bbs = []
    for comp in comps:
        r0, r1, c0, c1 = comp["bbox"]
        cells = set(comp["cells"])
        ok = True
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                border = r in (r0, r1) or c in (c0, c1)
                if border and (r, c) not in cells:
                    ok = False
                if not border and (r, c) in cells:
                    ok = False
        if ok and r1-r0 >= 2 and c1-c0 >= 2:
            bbs.append((r0, r1, c0, c1))
    return sorted(bbs)

def hollow_frame_interior_area(bb):
    r0, r1, c0, c1 = bb
    return max(0, (r1-r0-1) * (c1-c0-1))

def crop_without_markers(g: Grid, colors_to_ignore: Set[int]) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0 and v not in colors_to_ignore]
    if not cells:
        return [[0]]
    out = blank(max(r for r,_ in cells)-min(r for r,_ in cells)+1, max(c for _,c in cells)-min(c for _,c in cells)+1)
    r0 = min(r for r,_ in cells)
    c0 = min(c for _,c in cells)
    for r, c in cells:
        out[r-r0][c-c0] = g[r][c]
    return out

def boolean_overlay(a: Grid, b: Grid, op_key: int) -> Grid:
    na = normalize_crop(a)
    nb = normalize_crop(b)
    ha, wa = dims(na)
    hb, wb = dims(nb)
    H, W = max(ha, hb), max(wa, wb)
    aa = blank(H, W)
    bb = blank(H, W)
    aa = paste(aa, na, 0, 0)
    bb = paste(bb, nb, 0, 0)
    out = blank(H, W)
    for r in range(H):
        for c in range(W):
            av = aa[r][c] != 0
            bv = bb[r][c] != 0
            if op_key == 1:  # union
                if av and not bv:
                    out[r][c] = 2
                elif bv and not av:
                    out[r][c] = 3
                elif av and bv:
                    out[r][c] = 8
            elif op_key == 2:  # intersection
                if av and bv:
                    out[r][c] = 8
            elif op_key == 3:  # xor
                if av and not bv:
                    out[r][c] = 2
                elif bv and not av:
                    out[r][c] = 3
            elif op_key == 4:  # a minus b
                if av and not bv:
                    out[r][c] = 2
            else:
                if bv and not av:
                    out[r][c] = 3
    return out

def solve_easy_p01(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(1, h-1):
        for c in range(1, w-1):
            if g[r][c] != 0:
                continue
            vals = [g[r-1][c-1], g[r-1][c+1], g[r+1][c-1], g[r+1][c+1]]
            if vals[0] != 0 and all(v == vals[0] for v in vals):
                out[r][c] = vals[0]
    return out

def solve_easy_p02(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            cc = c + 1
            while cc < w and g[r][cc] == 0:
                out[r][cc] = v
                cc += 1
    return out

def solve_easy_p03(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r in range(1, h-1):
        for c in range(1, w-1):
            v = g[r][c]
            if v == 0:
                continue
            if g[r-1][c] == v and g[r+1][c] == v and g[r][c-1] == v and g[r][c+1] == v:
                out[r][c] = v
    return out

def solve_easy_p04(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h):
        for c in range(w-3):
            v = g[r][c]
            if v != 0 and g[r][c+1] == 0 and g[r][c+2] == 0 and g[r][c+3] == v:
                out[r][c+1] = out[r][c+2] = v
    for r in range(h-3):
        for c in range(w):
            v = g[r][c]
            if v != 0 and g[r+1][c] == 0 and g[r+2][c] == 0 and g[r+3][c] == v:
                out[r+1][c] = out[r+2][c] = v
    return out

def solve_easy_p05(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            v = g[r][c]
            if v == 0:
                continue
            if g[r][c+1] == v and g[r+1][c] == v and g[r+1][c+1] == v:
                for dr, dc in [(-1,-1),(-1,2),(2,-1),(2,2)]:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w and out[rr][cc] == 0:
                        out[rr][cc] = v
    return out

def solve_easy_p06(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            isolated = True
            for dr, dc in DIR8:
                rr, cc = r+dr, c+dc
                if 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 0:
                    isolated = False
                    break
            if not isolated:
                continue
            for dr, dc in KNIGHT:
                rr, cc = r+dr, c+dc
                if 0 <= rr < h and 0 <= cc < w and out[rr][cc] == 0:
                    out[rr][cc] = v
    return out

def solve_easy_p07(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    blocks = []
    for r in range(h-1):
        for c in range(w-1):
            v = g[r][c]
            if v != 0 and g[r][c+1] == v and g[r+1][c] == v and g[r+1][c+1] == v:
                blocks.append((v, r, c))
    for i in range(len(blocks)):
        v1, r1, c1 = blocks[i]
        for j in range(i+1, len(blocks)):
            v2, r2, c2 = blocks[j]
            if v1 != v2:
                continue
            if r1 == r2:
                left = min(c1, c2)
                right = max(c1, c2) + 1
                for rr in [r1, r1+1]:
                    for cc in range(left, right+1):
                        out[rr][cc] = v1
            if c1 == c2:
                top = min(r1, r2)
                bot = max(r1, r2) + 1
                for cc in [c1, c1+1]:
                    for rr in range(top, bot+1):
                        out[rr][cc] = v1
    return out

def solve_medium_p01(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for comp in find_components(g):
        touch = 0
        cells = comp["cells"]
        if any(r == 0 for r, _ in cells): touch += 1
        if any(r == h-1 for r, _ in cells): touch += 1
        if any(c == 0 for _, c in cells): touch += 1
        if any(c == w-1 for _, c in cells): touch += 1
        color = {0:1, 1:2, 2:3}.get(touch, 4)
        for r, c in cells:
            out[r][c] = color
    return out

def solve_medium_p02(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    for c in range(w):
        start = 0
        while start < h:
            end = start
            while end < h and g[end][c] != 5:
                end += 1
            segment = [g[r][c] for r in range(start, end)]
            falling = [v for v in segment if v not in (0,5)]
            newseg = [0]*(len(segment)-len(falling)) + falling
            for idx, r in enumerate(range(start, end)):
                out[r][c] = newseg[idx]
            if end < h:
                out[end][c] = 5
            start = end + 1
    return out

def solve_medium_p03(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    pos = defaultdict(list)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                pos[v].append((r, c))
    for color, cells in pos.items():
        if len(cells) == 2:
            (r1, c1), (r2, c2) = cells
            for r in range(min(r1,r2), max(r1,r2)+1):
                for c in range(min(c1,c2), max(c1,c2)+1):
                    out[r][c] = color
    return out

def solve_medium_p04(g: Grid) -> Grid:
    h, w = dims(g)
    k = sum(1 for c in range(w) if g[0][c] == 2)
    gg = deepcopy_grid(g)
    for c in range(w):
        if gg[0][c] == 2:
            gg[0][c] = 0
    comps = sorted(find_components(gg), key=lambda comp: (comp["bbox"][2], comp["bbox"][0]))
    if not comps:
        return [[0]]
    idx = min(max(k,1), len(comps)) - 1
    return crop_component(gg, comps[idx])

def solve_medium_p05(g: Grid) -> Grid:
    h, w = dims(g)
    comps = find_components(g)
    if not comps:
        return deepcopy_grid(g)
    comp = comps[0]
    crop = crop_component(g, comp)
    r0, r1, c0, c1 = comp["bbox"]
    ch, cw = dims(crop)
    cr = (r0 + r1) / 2.0
    cc = (c0 + c1) / 2.0
    corners = [
        (0, 0),
        (0, w-cw),
        (h-ch, 0),
        (h-ch, w-cw),
    ]
    def dist(pos):
        tr, tc = pos
        center_r = tr + (ch - 1) / 2.0
        center_c = tc + (cw - 1) / 2.0
        return (center_r - cr) ** 2 + (center_c - cc) ** 2
    target = min(corners, key=dist)
    out = blank(h, w)
    return paste(out, crop, target[0], target[1])

def solve_medium_p06(g: Grid) -> Grid:
    comps = find_components(g)
    if not comps:
        return [[0]]
    best = max(comps, key=lambda comp: (comp["size"], -(comp["bbox"][0]), -(comp["bbox"][2])))
    crop = crop_component(g, best)
    return flip_h(crop)

def solve_medium_p07(g: Grid) -> Grid:
    comps = find_components(g)
    if not comps:
        return [[0]]
    comps = sorted(comps, key=lambda comp: (- (comp["bbox"][1]-comp["bbox"][0]+1), - (comp["bbox"][3]-comp["bbox"][2]+1), comp["bbox"][2], comp["bbox"][0]))
    crops = [crop_component(g, comp) for comp in comps]
    return gallery(crops, gap=1, valign="bottom")

def solve_hard_p01(g: Grid) -> Grid:
    h, w = dims(g)
    out = deepcopy_grid(g)
    starts = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    if not starts:
        return out
    r, c = starts[0]
    if c == 0:
        dr, dc = 0, 1
    elif c == w-1:
        dr, dc = 0, -1
    elif r == 0:
        dr, dc = 1, 0
    else:
        dr, dc = -1, 0
    rr, cc = r, c
    visited = set()
    while True:
        rr += dr
        cc += dc
        if not (0 <= rr < h and 0 <= cc < w):
            break
        if g[rr][cc] == 5:
            break
        state = (rr, cc, dr, dc)
        if state in visited:
            break
        visited.add(state)
        if g[rr][cc] == 0:
            out[rr][cc] = 8
        elif g[rr][cc] == 3:  # /
            dr, dc = -dc, -dr
        elif g[rr][cc] == 4:  # \
            dr, dc = dc, dr
        elif g[rr][cc] == 2:
            pass
        else:
            # any other colored object acts as blocker
            break
    return out

def solve_hard_p02(g: Grid) -> Grid:
    h, w = dims(g)
    start = goal = None
    for r in range(h):
        for c in range(w):
            if g[r][c] == 2:
                start = (r, c)
            elif g[r][c] == 3:
                goal = (r, c)
    q = deque()
    q.append((start[0], start[1], 0))
    prev = {(start[0], start[1], 0): None}
    def can_enter(v, keys):
        if v == 4:
            return False
        if v == 6 and not (keys & 1):
            return False
        if v == 8 and not (keys & 2):
            return False
        return True
    end_state = None
    while q:
        r, c, keys = q.popleft()
        if (r, c) == goal:
            end_state = (r, c, keys)
            break
        for dr, dc in DIR4:
            rr, cc = r+dr, c+dc
            if not inb(g, rr, cc):
                continue
            v = g[rr][cc]
            if not can_enter(v, keys):
                continue
            nkeys = keys
            if v == 5:
                nkeys |= 1
            if v == 7:
                nkeys |= 2
            state = (rr, cc, nkeys)
            if state not in prev:
                prev[state] = (r, c, keys)
                q.append(state)
    out = deepcopy_grid(g)
    if end_state is None:
        return out
    cur = end_state
    specials = {2,3,4,5,6,7,8}
    while cur is not None:
        r, c, _ = cur
        if out[r][c] not in specials:
            out[r][c] = 9
        cur = prev[cur]
    return out

def solve_hard_p03(g: Grid) -> Grid:
    comps = sorted(find_components(g), key=lambda comp: (comp["bbox"][0], comp["bbox"][2]))
    n = len(comps)
    out = blank(n, n)
    for i in range(n):
        out[i][i] = 1
    for i in range(n):
        for j in range(i+1, n):
            if line_of_sight(g, comps[i], comps[j]):
                out[i][j] = out[j][i] = 8
    return out

def solve_hard_p04(g: Grid) -> Grid:
    frames = frame_bboxes(g, frame_color=5)
    frame_set = set()
    for bb in frames:
        r0, r1, c0, c1 = bb
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    frame_set.add((r,c))
    comps = [comp for comp in find_components(g) if comp["color"] != 5 and not any((r,c) in frame_set for r,c in comp["cells"])]
    comps = sorted(comps, key=lambda comp: (comp["size"], comp["bbox"][0], comp["bbox"][2]))
    frames_sorted = sorted(frames, key=hollow_frame_interior_area)
    out = blank(*dims(g))
    for bb in frames:
        r0,r1,c0,c1 = bb
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c] = 5
    for comp, bb in zip(comps, frames_sorted):
        crop = crop_component(g, comp)
        out = center_in_rect(crop, out, bb)
    return out

def solve_hard_p05(g: Grid) -> Grid:
    h, w = dims(g)
    op_key = g[0][0]
    tf_key = g[0][w-1]
    gg = deepcopy_grid(g)
    gg[0][0] = 0
    gg[0][w-1] = 0
    comps = sorted(find_components(gg), key=lambda comp: (comp["bbox"][0], comp["bbox"][2]))
    if len(comps) < 2:
        return [[0]]
    a = crop_component(gg, comps[0])
    b = crop_component(gg, comps[1])
    b2 = transform_by_key(b, tf_key)
    return boolean_overlay(a, b2, op_key)

def solve_hard_p06(g: Grid) -> Grid:
    h, w = dims(g)
    anchor = None
    for r in range(h):
        for c in range(w):
            if g[r][c] == 9:
                anchor = (r, c)
    gg = deepcopy_grid(g)
    if anchor:
        gg[anchor[0]][anchor[1]] = 0
    crop = normalize_crop(gg)
    out = blank(h, w)
    if anchor:
        out[anchor[0]][anchor[1]] = 9
    variants = [crop, rotate90(crop), rotate180(crop), rotate270(crop)]
    ch, cw = dims(crop)
    offsets = [(-ch-1, -cw-1), (-ch-1, 1), (1, -cw-1), (1, 1)]
    ar, ac = anchor
    for var, (dr, dc) in zip(variants, offsets):
        out = paste(out, var, ar+dr, ac+dc)
    return out

def solve_hard_p07(g: Grid) -> Grid:
    h, w = dims(g)
    frames = frame_bboxes(g, frame_color=5)
    frame_cells = set()
    for bb in frames:
        r0,r1,c0,c1 = bb
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    frame_cells.add((r,c))
    template_cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] not in (0,1,2,3,4,5) and (r,c) not in frame_cells]
    if not template_cells:
        return deepcopy_grid(g)
    template = crop_bbox(g, bbox_of_cells(template_cells))
    out = blank(h, w)
    for bb in frames:
        r0,r1,c0,c1 = bb
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c] = 5
    for bb in frames:
        r0,r1,c0,c1 = bb
        keys = []
        for rr, cc in [(r0-1,c0), (r0-1,c1), (r1+1,c0), (r1+1,c1), (r0,c0-1), (r0,c1+1), (r1,c0-1), (r1,c1+1)]:
            if 0 <= rr < h and 0 <= cc < w and 1 <= g[rr][cc] <= 4:
                keys.append(g[rr][cc])
        key = min(keys) if keys else 1
        var = transform_by_key(template, key)
        out = center_in_rect(var, out, bb)
    return out

SOLVERS = {
    "easy_p01": solve_easy_p01,
    "easy_p02": solve_easy_p02,
    "easy_p03": solve_easy_p03,
    "easy_p04": solve_easy_p04,
    "easy_p05": solve_easy_p05,
    "easy_p06": solve_easy_p06,
    "easy_p07": solve_easy_p07,
    "medium_p01": solve_medium_p01,
    "medium_p02": solve_medium_p02,
    "medium_p03": solve_medium_p03,
    "medium_p04": solve_medium_p04,
    "medium_p05": solve_medium_p05,
    "medium_p06": solve_medium_p06,
    "medium_p07": solve_medium_p07,
    "hard_p01": solve_hard_p01,
    "hard_p02": solve_hard_p02,
    "hard_p03": solve_hard_p03,
    "hard_p04": solve_hard_p04,
    "hard_p05": solve_hard_p05,
    "hard_p06": solve_hard_p06,
    "hard_p07": solve_hard_p07,
}
