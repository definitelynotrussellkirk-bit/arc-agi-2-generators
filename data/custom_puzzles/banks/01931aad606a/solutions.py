
from __future__ import annotations
from typing import List, Tuple, Dict, Callable
from collections import deque, Counter

Grid = List[List[int]]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def zeros(h: int, w: int, val: int = 0) -> Grid:
    return [[val] * w for _ in range(h)]

def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0])

def add_cells(g: Grid, cells: List[Tuple[int, int]], color: int) -> Grid:
    h, w = dims(g)
    for r, c in cells:
        assert 0 <= r < h and 0 <= c < w, (r, c, h, w)
        g[r][c] = color
    return g

def bbox(cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def norm(cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    r0, c0, _, _ = bbox(cells)
    return sorted((r - r0, c - c0) for r, c in cells)

def rotate_offsets(offsets: List[Tuple[int, int]], k: int) -> List[Tuple[int, int]]:
    out: List[Tuple[int, int]] = []
    for r, c in offsets:
        rr, cc = r, c
        for _ in range(k % 4):
            rr, cc = cc, -rr
        out.append((rr, cc))
    minr = min(r for r, c in out)
    minc = min(c for r, c in out)
    return sorted((r - minr, c - minc) for r, c in out)

def reflect_offsets_vert(offsets: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    maxc = max(c for r, c in offsets)
    return sorted((r, maxc - c) for r, c in offsets)

def scale_offsets(offsets: List[Tuple[int, int]], k: int) -> List[Tuple[int, int]]:
    out: List[Tuple[int, int]] = []
    for r, c in offsets:
        for dr in range(k):
            for dc in range(k):
                out.append((r * k + dr, c * k + dc))
    return sorted(out)

def crop_to_bbox(g: Grid, cells: List[Tuple[int, int]]) -> Grid:
    r0, c0, r1, c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def rotate_grid_cw(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]

def rotate_grid_times(g: Grid, k: int) -> Grid:
    out = g
    for _ in range(k % 4):
        out = rotate_grid_cw(out)
    return out

def reflect_grid_vert(g: Grid) -> Grid:
    return [list(reversed(row)) for row in g]

def components_by_color(g: Grid, target_colors=None):
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            col = g[r][c]
            if col == 0:
                seen[r][c] = True
                continue
            if target_colors is not None and col not in target_colors:
                seen[r][c] = True
                continue
            q = deque([(r, c)])
            seen[r][c] = True
            cells = []
            while q:
                rr, cc = q.popleft()
                cells.append((rr, cc))
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == col:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append({"color": col, "cells": cells})
    return comps

def place_offsets(g: Grid, offsets: List[Tuple[int, int]], anchor: Tuple[int, int], color: int) -> None:
    ar, ac = anchor
    for dr, dc in offsets:
        g[ar + dr][ac + dc] = color

def canonical_rotations(offsets: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    return [rotate_offsets(offsets, k) for k in range(4)]

def touches_corner(comp_cells: List[Tuple[int, int]], h: int, w: int) -> bool:
    top = any(r == 0 for r, c in comp_cells)
    bottom = any(r == h - 1 for r, c in comp_cells)
    left = any(c == 0 for r, c in comp_cells)
    right = any(c == w - 1 for r, c in comp_cells)
    return (top or bottom) and (left or right)

def has_hole(cells: List[Tuple[int, int]]) -> bool:
    r0, c0, r1, c1 = bbox(cells)
    H, W = r1 - r0 + 1, c1 - c0 + 1
    filled = {(r - r0, c - c0) for r, c in cells}
    seen = set()
    q = deque()
    for r in range(H):
        for c in range(W):
            if r in (0, H - 1) or c in (0, W - 1):
                if (r, c) not in filled and (r, c) not in seen:
                    seen.add((r, c))
                    q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and (nr, nc) not in filled and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    for r in range(H):
        for c in range(W):
            if (r, c) not in filled and (r, c) not in seen:
                return True
    return False

def vertical_symmetric(offsets: List[Tuple[int, int]]) -> bool:
    return offsets == reflect_offsets_vert(offsets)

def grid_from_offsets(offsets: List[Tuple[int, int]], color: int = 1) -> Grid:
    mr = max(r for r, c in offsets)
    mc = max(c for r, c in offsets)
    g = zeros(mr + 1, mc + 1)
    for r, c in offsets:
        g[r][c] = color
    return g

def overlay_sets(a: List[Tuple[int, int]], b: List[Tuple[int, int]], op: str) -> List[Tuple[int, int]]:
    sa, sb = set(a), set(b)
    if op == "union":
        out = sa | sb
    elif op == "intersection":
        out = sa & sb
    elif op == "xor":
        out = sa ^ sb
    else:
        raise ValueError(op)
    if not out:
        return []
    minr = min(r for r, c in out)
    minc = min(c for r, c in out)
    return sorted((r - minr, c - minc) for r, c in out)

def sorted_control_grid_positions(control_cells: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int, int]]:
    rows = sorted({r for r, c, color in control_cells})
    cols = sorted({c for r, c, color in control_cells})
    assert len(rows) == 2 and len(cols) == 2
    out = []
    for r, c, color in control_cells:
        out.append((rows.index(r), cols.index(c), r, c, color))
    out.sort()
    return out

def solve_easy_15_exact_descending_diagonal_pairs(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 2:
                continue
            if r > 0 and c > 0 and g[r - 1][c - 1] == 2:
                continue
            rr, cc = r, c
            cells = []
            while rr < h and cc < w and g[rr][cc] == 2:
                cells.append((rr, cc))
                rr += 1
                cc += 1
            if len(cells) == 2:
                for cr, cc in cells:
                    out[cr][cc] = 8
    return out

def solve_easy_16_fill_x_centers(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if g[r][c] != 0:
                continue
            if g[r - 1][c - 1] == 3 and g[r - 1][c + 1] == 3 and g[r + 1][c - 1] == 3 and g[r + 1][c + 1] == 3:
                out[r][c] = 4
    return out

def solve_easy_17_extend_exact_horizontal_triples(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        c = 0
        while c < w:
            if g[r][c] != 7:
                c += 1
                continue
            s = c
            while c < w and g[r][c] == 7:
                c += 1
            if c - s == 3 and s > 0 and c < w and g[r][s - 1] == 0 and g[r][c] == 0:
                out[r][s - 1] = 7
                out[r][c] = 7
    return out

def solve_easy_18_mirror_singletons_across_vertical_midline(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[r][w - 1 - c] = g[r][c]
    return out

def solve_easy_19_grow_crosses_from_red_seeds(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    seeds = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in seeds:
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and out[nr][nc] == 0:
                out[nr][nc] = 1
    for r, c in seeds:
        out[r][c] = 2
    return out

def solve_easy_20_fill_the_singleton_row(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    cells = [(r, c, g[r][c]) for r in range(h) for c in range(w) if g[r][c] != 0]
    assert len(cells) == 1
    r, c, color = cells[0]
    for cc in range(w):
        out[r][cc] = color
    return out

def solve_easy_21_tight_crop_of_nonzero_bbox(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]

def solve_medium_15_outline_filled_rectangles(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        color = comp["color"]
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if r in (r0, r1) or c in (c0, c1):
                    out[r][c] = color
    return out

def solve_medium_16_shift_all_objects_by_direction_key(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    counts = Counter(v for row in g for v in row if v != 0)
    control = None
    for color in (1, 2, 3, 4):
        if counts.get(color, 0) == 1:
            control = color
            break
    assert control is not None
    delta = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}[control]
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or v == control:
                continue
            nr, nc = r + delta[0], c + delta[1]
            out[nr][nc] = v
    return out

def solve_medium_17_keep_only_hole_bearing_components(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        if has_hole(comp["cells"]):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out

def solve_medium_18_rotate_each_l_triomino_clockwise(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        offsets = norm(comp["cells"])
        rot = rotate_offsets(offsets, 1)
        for dr, dc in rot:
            out[r0 + dr][c0 + dc] = comp["color"]
    return out

def solve_medium_19_keep_corner_touching_components(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        if touches_corner(comp["cells"], h, w):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out

def solve_medium_20_crop_and_pack_components_horizontally(g: Grid) -> Grid:
    comps = components_by_color(g)
    comps.sort(key=lambda comp: (min(c for r, c in comp["cells"]), min(r for r, c in comp["cells"])))
    crops = [crop_to_bbox(g, comp["cells"]) for comp in comps]
    H = max(len(crop) for crop in crops)
    W = sum(len(crop[0]) for crop in crops) + (len(crops) - 1)
    out = zeros(H, W)
    x = 0
    for crop in crops:
        ch, cw = len(crop), len(crop[0])
        for r in range(ch):
            for c in range(cw):
                out[r][x + c] = crop[r][c]
        x += cw + 1
    return out

def solve_medium_21_keep_components_matching_template_under_rotation(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template_comp = components_by_color(g, {1})[0]
    target_shapes = {tuple(shape) for shape in canonical_rotations(norm(template_comp["cells"]))}
    for comp in components_by_color(g, {3}):
        if tuple(norm(comp["cells"])) in target_shapes:
            for r, c in comp["cells"]:
                out[r][c] = 8
    return out

def solve_hard_15_make_transform_panel_from_single_template(g: Grid) -> Grid:
    template_comp = components_by_color(g, {2})[0]
    template = crop_to_bbox(g, template_comp["cells"])
    th, tw = dims(template)
    assert th == tw
    control_cells = [(r, c, g[r][c]) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] in (1, 3, 4, 6)]
    pos = sorted_control_grid_positions(control_cells)
    out = zeros(2 * th + 1, 2 * tw + 1)
    mapping = {1: ("rot", 0), 3: ("rot", 1), 4: ("rot", 2), 6: ("ref", 0)}
    for qr, qc, _r, _c, color in pos:
        kind, arg = mapping[color]
        block = rotate_grid_times(template, arg) if kind == "rot" else reflect_grid_vert(template)
        for r in range(th):
            for c in range(tw):
                if block[r][c] != 0:
                    out[qr * (th + 1) + r][qc * (tw + 1) + c] = 7
    return out

def solve_hard_16_scale_the_unique_vertically_symmetric_component(g: Grid) -> Grid:
    comps = components_by_color(g, {3})
    chosen = None
    for comp in comps:
        if vertical_symmetric(norm(comp["cells"])):
            chosen = comp
            break
    assert chosen is not None
    offsets = scale_offsets(norm(chosen["cells"]), 2)
    mr = max(r for r, c in offsets)
    mc = max(c for r, c in offsets)
    out = zeros(mr + 1, mc + 1)
    for r, c in offsets:
        out[r][c] = 8
    return out

def solve_hard_17_center_template_inside_every_frame(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template_comp = components_by_color(g, {2})[0]
    template_offsets = norm(template_comp["cells"])
    tr, tc = max(r for r, c in template_offsets) + 1, max(c for r, c in template_offsets) + 1
    for comp in components_by_color(g):
        color = comp["color"]
        if color == 2:
            continue
        r0, c0, r1, c1 = bbox(comp["cells"])
        for r, c in comp["cells"]:
            out[r][c] = color
        ih, iw = r1 - r0 - 1, c1 - c0 - 1
        sr = r0 + 1 + (ih - tr) // 2
        sc = c0 + 1 + (iw - tc) // 2
        for dr, dc in template_offsets:
            out[sr + dr][sc + dc] = color
    return out

def solve_hard_18_pack_components_by_area_with_palette_top_to_bottom(g: Grid) -> Grid:
    palette = [(r, c, g[r][c]) for r in range(len(g)) for c in range(len(g[0])) if c == 0 and g[r][c] not in (0, 3)]
    palette.sort()
    colors = [color for _r, _c, color in palette]
    comps = components_by_color(g, {3})
    comps.sort(key=lambda comp: (-len(comp["cells"]), min(r for r, c in comp["cells"]), min(c for r, c in comp["cells"])))
    crops = []
    for comp, color in zip(comps, colors):
        crop = crop_to_bbox(g, comp["cells"])
        recol = [[color if v != 0 else 0 for v in row] for row in crop]
        crops.append(recol)
    H = sum(len(crop) for crop in crops) + (len(crops) - 1)
    W = max(len(crop[0]) for crop in crops)
    out = zeros(H, W)
    y = 0
    for crop in crops:
        ch, cw = len(crop), len(crop[0])
        for r in range(ch):
            for c in range(cw):
                out[y + r][c] = crop[r][c]
        y += ch + 1
    return out

def solve_hard_19_complete_missing_quadrant_by_rotation(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w and h % 2 == 1
    ctr = h // 2
    out = clone(g)
    cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in cells:
        rr, cc = r, c
        for _ in range(3):
            dr, dc = rr - ctr, cc - ctr
            rr, cc = ctr + dc, ctr - dr
            out[rr][cc] = 2
    return out

def solve_hard_20_boolean_combine_two_templates_by_key(g: Grid) -> Grid:
    s1 = norm(components_by_color(g, {1})[0]["cells"])
    s2 = norm(components_by_color(g, {2})[0]["cells"])
    counts = Counter(v for row in g for v in row if v != 0)
    control = None
    for color in (3, 4, 6):
        if counts.get(color, 0) == 1:
            control = color
            break
    assert control is not None
    op = {3: "union", 4: "intersection", 6: "xor"}[control]
    res = overlay_sets(s1, s2, op)
    if not res:
        return [[0]]
    mr = max(r for r, c in res)
    mc = max(c for r, c in res)
    out = zeros(mr + 1, mc + 1)
    for r, c in res:
        out[r][c] = 8
    return out

def solve_hard_21_cartesian_product_of_row_shapes_and_column_colors(g: Grid) -> Grid:
    row_shapes = [crop_to_bbox(g, comp["cells"]) for comp in sorted(components_by_color(g, {2}), key=lambda comp: min(r for r, c in comp["cells"]))]
    col_colors = [g[r][c] for r in range(len(g)) for c in range(len(g[0])) if r == 0 and g[r][c] not in (0, 2)]
    slot_h = max(len(shape) for shape in row_shapes)
    slot_w = max(len(shape[0]) for shape in row_shapes)
    rows = len(row_shapes)
    cols = len(col_colors)
    out = zeros(rows * slot_h + (rows - 1), cols * slot_w + (cols - 1))
    for i, shape in enumerate(row_shapes):
        sh, sw = len(shape), len(shape[0])
        for j, color in enumerate(col_colors):
            y = i * (slot_h + 1)
            x = j * (slot_w + 1)
            for r in range(sh):
                for c in range(sw):
                    if shape[r][c] != 0:
                        out[y + r][x + c] = color
    return out

SOLVERS: Dict[str, Callable[[Grid], Grid]] = {
    "easy_15_exact_descending_diagonal_pairs": solve_easy_15_exact_descending_diagonal_pairs,
    "easy_16_fill_x_centers": solve_easy_16_fill_x_centers,
    "easy_17_extend_exact_horizontal_triples": solve_easy_17_extend_exact_horizontal_triples,
    "easy_18_mirror_singletons_across_vertical_midline": solve_easy_18_mirror_singletons_across_vertical_midline,
    "easy_19_grow_crosses_from_red_seeds": solve_easy_19_grow_crosses_from_red_seeds,
    "easy_20_fill_the_singleton_row": solve_easy_20_fill_the_singleton_row,
    "easy_21_tight_crop_of_nonzero_bbox": solve_easy_21_tight_crop_of_nonzero_bbox,
    "medium_15_outline_filled_rectangles": solve_medium_15_outline_filled_rectangles,
    "medium_16_shift_all_objects_by_direction_key": solve_medium_16_shift_all_objects_by_direction_key,
    "medium_17_keep_only_hole_bearing_components": solve_medium_17_keep_only_hole_bearing_components,
    "medium_18_rotate_each_l_triomino_clockwise": solve_medium_18_rotate_each_l_triomino_clockwise,
    "medium_19_keep_corner_touching_components": solve_medium_19_keep_corner_touching_components,
    "medium_20_crop_and_pack_components_horizontally": solve_medium_20_crop_and_pack_components_horizontally,
    "medium_21_keep_components_matching_template_under_rotation": solve_medium_21_keep_components_matching_template_under_rotation,
    "hard_15_make_transform_panel_from_single_template": solve_hard_15_make_transform_panel_from_single_template,
    "hard_16_scale_the_unique_vertically_symmetric_component": solve_hard_16_scale_the_unique_vertically_symmetric_component,
    "hard_17_center_template_inside_every_frame": solve_hard_17_center_template_inside_every_frame,
    "hard_18_pack_components_by_area_with_palette_top_to_bottom": solve_hard_18_pack_components_by_area_with_palette_top_to_bottom,
    "hard_19_complete_missing_quadrant_by_rotation": solve_hard_19_complete_missing_quadrant_by_rotation,
    "hard_20_boolean_combine_two_templates_by_key": solve_hard_20_boolean_combine_two_templates_by_key,
    "hard_21_cartesian_product_of_row_shapes_and_column_colors": solve_hard_21_cartesian_product_of_row_shapes_and_column_colors,
}

def verify_bank(bank: List[dict]) -> None:
    for task in bank:
        solver = SOLVERS[task["id"]]
        for split in ("train", "test"):
            for i, example in enumerate(task[split]):
                got = solver(example["input"])
                exp = example["output"]
                if got != exp:
                    raise AssertionError(f'{task["id"]} {split}[{i}] mismatch')
    print(f"verified {len(bank)} tasks")

if __name__ == "__main__":
    import json
    from pathlib import Path
    bank_path = Path(__file__).with_name("arc_puzzle_bank_third_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
