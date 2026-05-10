
from __future__ import annotations
from collections import deque
from typing import List, Tuple

Grid = List[List[int]]

def zeros(h, w, val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, box):
    r0, c0, r1, c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))

def hflip(g):
    return [list(reversed(row)) for row in g]

def vflip(g):
    return [row[:] for row in reversed(g)]

def rot90(g):
    h, w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g):
    return rot90(rot90(g))

def rot270(g):
    return rot90(rot180(g))

def transpose_square(g):
    n = len(g)
    return [[g[c][r] for c in range(n)] for r in range(n)]

def stamp(g, obj, top, left, transparent=0):
    H, W = dims(g)
    h, w = dims(obj)
    for r in range(h):
        for c in range(w):
            v = obj[r][c]
            if v != transparent:
                rr, cc = top + r, left + c
                if 0 <= rr < H and 0 <= cc < W:
                    g[rr][cc] = v
    return g

def center_stamp(H, W, obj, transparent=0):
    out = zeros(H, W)
    h, w = dims(obj)
    top = (H - h) // 2
    left = (W - w) // 2
    return stamp(out, obj, top, left, transparent=transparent)

def recolor_nonzero(g, color):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[r][c] = color
    return out

def normalize_binary(g):
    cg = crop_nonzero(g)
    return [[1 if v != 0 else 0 for v in row] for row in cg]

def component_grid(g, cells):
    r0, c0, r1, c1 = bbox(cells)
    out = zeros(r1 - r0 + 1, c1 - c0 + 1)
    for r, c in cells:
        out[r-r0][c-c0] = g[r][c]
    return out

def connected_components(g, colors=None, ignore_positions=None):
    colors = None if colors is None else set(colors)
    ignore_positions = set() if ignore_positions is None else set(ignore_positions)
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if (r, c) in ignore_positions:
                seen[r][c] = True
                continue
            v = g[r][c]
            if seen[r][c] or v == 0 or (colors is not None and v not in colors):
                continue
            seen[r][c] = True
            dq = deque([(r, c)])
            cells = []
            while dq:
                rr, cc = dq.popleft()
                cells.append((rr, cc))
                for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and (nr, nc) not in ignore_positions:
                        nv = g[nr][nc]
                        if nv != 0 and (colors is None or nv in colors):
                            seen[nr][nc] = True
                            dq.append((nr, nc))
            comps.append(cells)
    return comps

def flood_regions_nonwall(g, wall=8):
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    regs = []
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c] == wall:
                continue
            seen[r][c] = True
            dq = deque([(r, c)])
            cells = []
            while dq:
                rr, cc = dq.popleft()
                cells.append((rr, cc))
                for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] != wall:
                        seen[nr][nc] = True
                        dq.append((nr, nc))
            regs.append(cells)
    return regs

def all_rotations(g):
    a = normalize_binary(g)
    rots = []
    cur = a
    for _ in range(4):
        if cur not in rots:
            rots.append(cur)
        cur = rot90(cur)
    return rots

def transform_by_code(g, code):
    if code == 0:
        return clone(g)
    if code == 1:
        return rot90(g)
    if code == 2:
        return rot180(g)
    if code == 3:
        return rot270(g)
    if code == 4:
        return hflip(g)
    if code == 5:
        return vflip(g)
    raise ValueError(f"unknown transform code {code}")

def add_rect_border(obj, border_color):
    h, w = dims(obj)
    out = zeros(h + 2, w + 2)
    H, W = dims(out)
    for r in range(H):
        for c in range(W):
            if r in (0, H-1) or c in (0, W-1):
                out[r][c] = border_color
    stamp(out, obj, 1, 1)
    return out

def panelize_row(panels, sep=1):
    h = len(panels[0])
    w = sum(len(p[0]) for p in panels) + sep * (len(panels) - 1)
    out = zeros(h, w)
    c = 0
    for i, p in enumerate(panels):
        stamp(out, p, 0, c)
        c += len(p[0])
        if i < len(panels) - 1:
            c += sep
    return out

def panelize_grid(panel_rows, sep=1):
    panel_h = len(panel_rows[0][0])
    panel_w = len(panel_rows[0][0][0])
    H = len(panel_rows) * panel_h + sep * (len(panel_rows) - 1)
    W = len(panel_rows[0]) * panel_w + sep * (len(panel_rows[0]) - 1)
    out = zeros(H, W)
    r0 = 0
    for i, row in enumerate(panel_rows):
        c0 = 0
        for j, p in enumerate(row):
            stamp(out, p, r0, c0)
            c0 += panel_w
            if j < len(row) - 1:
                c0 += sep
        r0 += panel_h
        if i < len(panel_rows) - 1:
            r0 += sep
    return out

def ray_cells(g, start, direction, wall=8):
    h, w = dims(g)
    r, c = start
    dr, dc = direction
    cells = [(r, c)]
    rr, cc = r + dr, c + dc
    while 0 <= rr < h and 0 <= cc < w and g[rr][cc] != wall:
        cells.append((rr, cc))
        rr += dr
        cc += dc
    return cells

def count_rays(g, emitter_color=2, wall=8):
    h, w = dims(g)
    counts = [[0] * w for _ in range(h)]
    emitters = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == emitter_color]
    for e in emitters:
        for d in ((1,0), (-1,0), (0,1), (0,-1)):
            for r, c in ray_cells(g, e, d, wall=wall):
                counts[r][c] += 1
    return counts

def shortest_paths_from_seed(area_cells_set, start):
    dq = deque([start])
    dist = {start: 0}
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in area_cells_set and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                dq.append((nr, nc))
    return dist

def touch_borders(cells, h, w):
    borders = set()
    for r, c in cells:
        if r == 0:
            borders.add('top')
        if r == h - 1:
            borders.add('bottom')
        if c == 0:
            borders.add('left')
        if c == w - 1:
            borders.add('right')
    return borders

def solve_easy_134_fill_between_matching_row_markers(g):
    h, w = dims(g)
    out = clone(g)
    for r in range(h):
        nz = [(c, v) for c, v in enumerate(g[r]) if v != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            c0, color = nz[0]
            c1, _ = nz[1]
            for c in range(min(c0, c1), max(c0, c1) + 1):
                out[r][c] = color
    return out

def solve_easy_135_complete_main_diagonal_reflection(g):
    n = len(g)
    out = clone(g)
    for r in range(n):
        for c in range(n):
            if g[r][c] != 0:
                out[c][r] = g[r][c]
    return out

def solve_easy_136_expand_singletons_to_diamonds(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for dr, dc in ((0,0), (1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w:
                        out[nr][nc] = v
    return out

def solve_easy_137_left_pack_rows_preserving_order(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        vals = [v for v in g[r] if v != 0]
        for i, v in enumerate(vals):
            out[r][i] = v
    return out

def solve_easy_138_project_markers_to_full_crosses(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for cc in range(w):
                    out[r][cc] = v
                for rr in range(h):
                    out[rr][c] = v
    return out

def solve_easy_139_fill_hollow_rectangles(g):
    out = clone(g)
    for cells in connected_components(g):
        color = g[cells[0][0]][cells[0][1]]
        r0, c0, r1, c1 = bbox(cells)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                out[r][c] = color
    return out

def solve_easy_140_crop_tight_nonzero_bbox(g):
    return crop_nonzero(g)

def solve_medium_134_select_legend_object_and_flip_horizontally(g):
    legend = g[0][0]
    comps = connected_components(g, colors={legend}, ignore_positions={(0, 0)})
    target = max(comps, key=len)
    return hflip(component_grid(g, target))

def solve_medium_135_build_row_column_color_match_map(g):
    top = g[0][1:]
    left = [row[0] for row in g[1:]]
    out = zeros(len(left), len(top))
    for r, lc in enumerate(left):
        for c, tc in enumerate(top):
            if lc != 0 and lc == tc:
                out[r][c] = lc
    return out

def solve_medium_136_apply_rightward_gravity_in_each_walled_segment(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        c = 0
        while c < w:
            if g[r][c] == 8:
                out[r][c] = 8
                c += 1
                continue
            start = c
            while c < w and g[r][c] != 8:
                c += 1
            end = c
            vals = [g[r][cc] for cc in range(start, end) if g[r][cc] != 0]
            write = end - len(vals)
            for i, v in enumerate(vals):
                out[r][write + i] = v
    return out

def solve_medium_137_match_prototype_under_rotation_and_recolor(g):
    target_color = g[5][0]
    proto = [row[0:5] for row in g[0:5]]
    candidates = [[row[c:c+5] for row in g[0:5]] for c in (6, 12, 18)]
    rotset = all_rotations(proto)
    for cand in candidates:
        if normalize_binary(cand) in rotset:
            return recolor_nonzero(crop_nonzero(cand), target_color)
    return [[0]]

def solve_medium_138_paint_blocked_rays_from_emitters(g):
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 2:
                for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                    rr, cc = r + dr, c + dc
                    while 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 8:
                        out[rr][cc] = 2
                        rr += dr
                        cc += dc
    return out

def solve_medium_139_recolor_components_by_area_parity(g):
    h, w = dims(g)
    out = zeros(h, w)
    for cells in connected_components(g):
        color = 3 if (len(cells) % 2 == 1) else 4
        for r, c in cells:
            out[r][c] = color
    return out

def solve_medium_140_select_object_touching_two_borders_and_crop(g):
    h, w = dims(g)
    for cells in connected_components(g):
        if len(touch_borders(cells, h, w)) == 2:
            return component_grid(g, cells)
    return [[0]]

def solve_hard_134_decode_library_with_transform_and_border_codes(g):
    index = g[0][0] - 1
    transform_code = g[0][1]
    fill_color = g[0][2]
    border_color = g[0][3]
    panels = [[row[c:c+5] for row in g[1:6]] for c in (0, 6, 12)]
    obj = crop_nonzero(panels[index])
    obj = transform_by_code(obj, transform_code)
    obj = recolor_nonzero(obj, fill_color)
    return add_rect_border(obj, border_color)

def solve_hard_135_overlay_blocked_ray_counts(g):
    h, w = dims(g)
    counts = count_rays(g, emitter_color=2, wall=8)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 8:
                out[r][c] = 8
            elif counts[r][c] == 1:
                out[r][c] = 2
            elif counts[r][c] == 2:
                out[r][c] = 3
            elif counts[r][c] >= 3:
                out[r][c] = 4
    return out

def solve_hard_136_fill_chambers_by_nearest_seed_with_tie_break(g):
    h, w = dims(g)
    out = clone(g)
    for cells in flood_regions_nonwall(g, wall=8):
        area = set(cells)
        seeds = [(r, c, g[r][c]) for r, c in cells if g[r][c] != 0]
        if not seeds:
            continue
        dmaps = {(r, c): shortest_paths_from_seed(area, (r, c)) for r, c, _ in seeds}
        for r, c in cells:
            if g[r][c] == 8:
                continue
            best = None
            best_color = None
            for sr, sc, color in seeds:
                d = dmaps[(sr, sc)].get((r, c), 10**9)
                cand = (d, color)
                if best is None or cand < best:
                    best = cand
                    best_color = color
            out[r][c] = best_color
    return out

def solve_hard_137_build_rotation_relation_matrix(g):
    panels = [[row[c:c+5] for row in g] for c in (0, 6, 12, 18)]
    norms = [normalize_binary(p) for p in panels]
    out = zeros(4, 4)
    for i, a in enumerate(norms):
        aset = all_rotations(a)
        for j, b in enumerate(norms):
            if i == j:
                out[i][j] = 8
            elif b == a:
                out[i][j] = 1
            elif b in aset:
                out[i][j] = 2
            else:
                out[i][j] = 0
    return out

def solve_hard_138_select_transform_recolor_and_center_stamp(g):
    selector_color = g[0][0]
    transform_code = g[0][1]
    target_color = g[0][2]
    area = [row[:] for row in g[1:8]]
    comps = connected_components(area, colors={selector_color})
    target = max(comps, key=len)
    obj = component_grid(area, target)
    obj = transform_by_code(obj, transform_code)
    obj = recolor_nonzero(obj, target_color)
    return center_stamp(7, 7, obj)

def solve_hard_139_build_cross_product_gallery_of_color_and_transform_codes(g):
    proto = [row[:] for row in g[0:5]]
    transform_codes = g[5][0:3]
    colors = g[6][0:3]
    rows = []
    for color in colors:
        prow = []
        for code in transform_codes:
            obj = transform_by_code(proto, code)
            prow.append(recolor_nonzero(obj, color))
        rows.append(prow)
    return panelize_grid(rows, sep=1)

def solve_hard_140_decode_transform_sequence_and_stamp_row(g):
    proto = [row[:] for row in g[0:5]]
    codes = [v for v in g[5][0:4]]
    target_color = g[5][4]
    panels = []
    cur = clone(proto)
    for code in codes:
        cur = transform_by_code(cur, code)
        panels.append(recolor_nonzero(cur, target_color))
    return panelize_row(panels, sep=1)


TASK_SOLVERS = {
    "solve_easy_134_fill_between_matching_row_markers": solve_easy_134_fill_between_matching_row_markers,
    "solve_easy_135_complete_main_diagonal_reflection": solve_easy_135_complete_main_diagonal_reflection,
    "solve_easy_136_expand_singletons_to_diamonds": solve_easy_136_expand_singletons_to_diamonds,
    "solve_easy_137_left_pack_rows_preserving_order": solve_easy_137_left_pack_rows_preserving_order,
    "solve_easy_138_project_markers_to_full_crosses": solve_easy_138_project_markers_to_full_crosses,
    "solve_easy_139_fill_hollow_rectangles": solve_easy_139_fill_hollow_rectangles,
    "solve_easy_140_crop_tight_nonzero_bbox": solve_easy_140_crop_tight_nonzero_bbox,
    "solve_medium_134_select_legend_object_and_flip_horizontally": solve_medium_134_select_legend_object_and_flip_horizontally,
    "solve_medium_135_build_row_column_color_match_map": solve_medium_135_build_row_column_color_match_map,
    "solve_medium_136_apply_rightward_gravity_in_each_walled_segment": solve_medium_136_apply_rightward_gravity_in_each_walled_segment,
    "solve_medium_137_match_prototype_under_rotation_and_recolor": solve_medium_137_match_prototype_under_rotation_and_recolor,
    "solve_medium_138_paint_blocked_rays_from_emitters": solve_medium_138_paint_blocked_rays_from_emitters,
    "solve_medium_139_recolor_components_by_area_parity": solve_medium_139_recolor_components_by_area_parity,
    "solve_medium_140_select_object_touching_two_borders_and_crop": solve_medium_140_select_object_touching_two_borders_and_crop,
    "solve_hard_134_decode_library_with_transform_and_border_codes": solve_hard_134_decode_library_with_transform_and_border_codes,
    "solve_hard_135_overlay_blocked_ray_counts": solve_hard_135_overlay_blocked_ray_counts,
    "solve_hard_136_fill_chambers_by_nearest_seed_with_tie_break": solve_hard_136_fill_chambers_by_nearest_seed_with_tie_break,
    "solve_hard_137_build_rotation_relation_matrix": solve_hard_137_build_rotation_relation_matrix,
    "solve_hard_138_select_transform_recolor_and_center_stamp": solve_hard_138_select_transform_recolor_and_center_stamp,
    "solve_hard_139_build_cross_product_gallery_of_color_and_transform_codes": solve_hard_139_build_cross_product_gallery_of_color_and_transform_codes,
    "solve_hard_140_decode_transform_sequence_and_stamp_row": solve_hard_140_decode_transform_sequence_and_stamp_row,
}

if __name__ == "__main__":
    import json
    from pathlib import Path
    bank_path = Path(__file__).with_name("arc_puzzle_bank_twentieth_21.json")
    if not bank_path.exists():
        raise SystemExit(f"missing {bank_path.name} for verification")
    tasks = json.loads(bank_path.read_text())
    total = 0
    for task in tasks:
        fn = TASK_SOLVERS[task["solver_name"]]
        for split in ("train", "test"):
            for pair in task[split]:
                got = fn(pair["input"])
                if got != pair["output"]:
                    raise AssertionError(f"verification failed for {task['id']} {split}")
                total += 1
    print(f"verified {len(tasks)} tasks / {total} input-output pairs")
