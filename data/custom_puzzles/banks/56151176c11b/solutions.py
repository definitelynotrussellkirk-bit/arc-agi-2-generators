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

def components_by_color(g: Grid, target_colors=None):
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c] == 0:
                continue
            col = g[r][c]
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

def solve_easy_08_exact_vertical_quadruples(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for c in range(w):
        r = 0
        while r < h:
            if g[r][c] != 1:
                r += 1
                continue
            s = r
            while r < h and g[r][c] == 1:
                r += 1
            if r - s == 4:
                for rr in range(s, r):
                    out[rr][c] = 2
    return out

def solve_easy_09_fill_plus_centers(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                continue
            vals = []
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    vals.append(g[nr][nc])
                else:
                    vals.append(None)
            if vals == [3,3,3,3]:
                out[r][c] = 4
    return out

def solve_easy_10_fill_single_frame_by_key(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    counts = Counter(v for row in g for v in row if v != 0)
    key = None
    for color, count in counts.items():
        if color != 8 and count == 1:
            key = color
            break
    assert key is not None
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 8]
    r1, c1, r2, c2 = bbox(cells)
    for r in range(r1+1, r2):
        for c in range(c1+1, c2):
            out[r][c] = key
    return out

def solve_easy_11_bridge_single_horizontal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c] == 2 and g[r][c+1] == 0 and g[r][c+2] == 2:
                out[r][c+1] = 7
    return out

def solve_easy_12_diagonal_shadow_down_right(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 3:
                nr, nc = r + 1, c + 1
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0:
                    out[nr][nc] = 5
    return out

def solve_easy_13_keep_leftmost_component(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g, {2})
    def keyfn(comp):
        r1, c1, _, _ = bbox(comp['cells'])
        return (c1, r1)
    best = min(comps, key=keyfn)
    for r, c in best['cells']:
        out[r][c] = 8
    return out

def solve_easy_14_mark_vertical_run_endpoints(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for c in range(w):
        r = 0
        while r < h:
            if g[r][c] != 6:
                r += 1
                continue
            s = r
            while r < h and g[r][c] == 6:
                r += 1
            if r - s >= 3:
                out[s][c] = 1
                out[r-1][c] = 1
    return out

def solve_medium_08_complete_rectangle_borders_from_diagonal_corners(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    colors = sorted({v for row in g for v in row if v != 0})
    for color in colors:
        cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == color]
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 == r2 or c1 == c2:
            continue
        ra, rb = sorted((r1,r2))
        ca, cb = sorted((c1,c2))
        for c in range(ca, cb+1):
            out[ra][c] = color
            out[rb][c] = color
        for r in range(ra, rb+1):
            out[r][ca] = color
            out[r][cb] = color
    return out

def solve_medium_09_fill_component_bounding_boxes(g: Grid) -> Grid:
    out = clone(g)
    comps = components_by_color(g, {4})
    for comp in comps:
        r1, c1, r2, c2 = bbox(comp['cells'])
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                out[r][c] = 4
    return out

def solve_medium_10_recolor_objects_by_above_key(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    comps = components_by_color(g, {3})
    for comp in comps:
        r1, c1, r2, c2 = bbox(comp['cells'])
        kr, kc = r1 - 1, c1
        assert 0 <= kr < h and 0 <= kc < w
        key = g[kr][kc]
        assert key not in (0, 3)
        for r, c in comp['cells']:
            out[r][c] = key
    return out

def solve_medium_11_keep_shape_matching_template(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            for r, c in comp['cells']:
                out[r][c] = 8
    return out

def solve_medium_12_reflect_left_objects_across_center_axis(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    axis = w // 2
    for r in range(h):
        for c in range(axis):
            if g[r][c] == 2:
                mc = 2 * axis - c
                if 0 <= mc < w:
                    out[r][mc] = 7
    return out

def solve_medium_13_fill_rectangles_from_diagonal_corners(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    colors = sorted({v for row in g for v in row if v != 0})
    for color in colors:
        cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == color]
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 == r2 or c1 == c2:
            continue
        ra, rb = sorted((r1,r2))
        ca, cb = sorted((c1,c2))
        for r in range(ra, rb+1):
            for c in range(ca, cb+1):
                out[r][c] = color
    return out

def solve_medium_14_select_diagonal_touching_components(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w
    out = zeros(h, w)
    for comp in components_by_color(g, {6}):
        if any(r == c for r, c in comp['cells']):
            for r, c in comp['cells']:
                out[r][c] = 2
    return out

def solve_hard_08_rotate_template_by_control_and_stamp(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template = components_by_color(g, {2})
    assert len(template) == 1
    template_offsets = norm(template[0]['cells'])
    counts = Counter(v for row in g for v in row if v != 0)
    control_color = None
    for color, count in counts.items():
        if color in (1, 3, 4, 6) and count == 1:
            control_color = color
            break
    assert control_color is not None
    rotation_map = {1: 0, 3: 1, 4: 2, 6: 3}
    k = rotation_map[control_color]
    target = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 8]
    assert len(target) == 1
    tr, tc = target[0]
    rot = rotate_offsets(template_offsets, k)
    for dr, dc in rot:
        out[tr + dr][tc + dc] = 7
    return out

def solve_hard_09_scale_second_smallest_component_2x(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g, {3})
    assert len(comps) >= 2
    comps = sorted(comps, key=lambda comp: (len(comp['cells']), bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    target = comps[1]
    r1, c1, _, _ = bbox(target['cells'])
    scaled = scale_offsets(norm(target['cells']), 2)
    for dr, dc in scaled:
        out[r1 + dr][c1 + dc] = 8
    return out

def solve_hard_10_palette_recolor_components_left_to_right(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    palette = [g[0][c] for c in range(w) if g[0][c] not in (0, 2)]
    assert len(palette) >= 3
    comps = components_by_color(g, {2})
    comps = sorted(comps, key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    for comp, color in zip(comps, palette):
        for r, c in comp['cells']:
            out[r][c] = color
    return out

def solve_hard_11_intersection_of_two_frame_interiors(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g)
    frames = [comp for comp in comps if len(comp['cells']) >= 8]
    assert len(frames) >= 2
    # choose first two colors by sorted color order for determinism
    frames = sorted(frames, key=lambda comp: comp['color'])[:2]
    interiors = []
    for comp in frames:
        r1, c1, r2, c2 = bbox(comp['cells'])
        inside = {(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)}
        interiors.append(inside)
    for r, c in sorted(interiors[0] & interiors[1]):
        out[r][c] = 7
    return out

def solve_hard_12_make_matching_shapes_symmetric(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            r1, c1, r2, c2 = bbox(comp['cells'])
            pts = {(r, c) for r, c in comp['cells']}
            for r, c in list(pts):
                mc = c1 + c2 - c
                pts.add((r, mc))
            for r, c in pts:
                out[r][c] = 8
    return out

def solve_hard_13_multi_marker_rotated_stamping(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template = components_by_color(g, {2})
    assert len(template) == 1
    template_offsets = norm(template[0]['cells'])
    rotation_map = {1: 0, 3: 1, 4: 2, 6: 3}
    for r in range(h):
        for c in range(w):
            if g[r][c] in rotation_map:
                rot = rotate_offsets(template_offsets, rotation_map[g[r][c]])
                for dr, dc in rot:
                    out[r + dr][c + dc] = 8
    return out

def solve_hard_14_select_shape_match_and_recolor_by_majority_singleton(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    counts = Counter()
    for color, count in Counter(v for row in g for v in row if v != 0).items():
        if color not in (1, 3) and count >= 1:
            counts[color] += count
    # majority by total singleton count
    majority_color = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            for r, c in comp['cells']:
                out[r][c] = majority_color
    return out

SOLVERS: Dict[str, Callable[[Grid], Grid]] = {
    "easy_08_exact_vertical_quadruples": solve_easy_08_exact_vertical_quadruples,
    "easy_09_fill_plus_centers": solve_easy_09_fill_plus_centers,
    "easy_10_fill_single_frame_by_key": solve_easy_10_fill_single_frame_by_key,
    "easy_11_bridge_single_horizontal_gaps": solve_easy_11_bridge_single_horizontal_gaps,
    "easy_12_diagonal_shadow_down_right": solve_easy_12_diagonal_shadow_down_right,
    "easy_13_keep_leftmost_component": solve_easy_13_keep_leftmost_component,
    "easy_14_mark_vertical_run_endpoints": solve_easy_14_mark_vertical_run_endpoints,
    "medium_08_complete_rectangle_borders_from_diagonal_corners": solve_medium_08_complete_rectangle_borders_from_diagonal_corners,
    "medium_09_fill_component_bounding_boxes": solve_medium_09_fill_component_bounding_boxes,
    "medium_10_recolor_objects_by_above_key": solve_medium_10_recolor_objects_by_above_key,
    "medium_11_keep_shape_matching_template": solve_medium_11_keep_shape_matching_template,
    "medium_12_reflect_left_objects_across_center_axis": solve_medium_12_reflect_left_objects_across_center_axis,
    "medium_13_fill_rectangles_from_diagonal_corners": solve_medium_13_fill_rectangles_from_diagonal_corners,
    "medium_14_select_diagonal_touching_components": solve_medium_14_select_diagonal_touching_components,
    "hard_08_rotate_template_by_control_and_stamp": solve_hard_08_rotate_template_by_control_and_stamp,
    "hard_09_scale_second_smallest_component_2x": solve_hard_09_scale_second_smallest_component_2x,
    "hard_10_palette_recolor_components_left_to_right": solve_hard_10_palette_recolor_components_left_to_right,
    "hard_11_intersection_of_two_frame_interiors": solve_hard_11_intersection_of_two_frame_interiors,
    "hard_12_make_matching_shapes_symmetric": solve_hard_12_make_matching_shapes_symmetric,
    "hard_13_multi_marker_rotated_stamping": solve_hard_13_multi_marker_rotated_stamping,
    "hard_14_select_shape_match_and_recolor_by_majority_singleton": solve_hard_14_select_shape_match_and_recolor_by_majority_singleton,
}

def verify_bank(bank: List[dict]) -> None:
    for task in bank:
        solver = SOLVERS[task["id"]]
        for split in ("train", "test"):
            for i, example in enumerate(task[split]):
                got = solver(example["input"])
                exp = example["output"]
                if got != exp:
                    raise AssertionError(f"{task['id']} {split}[{i}] mismatch")
    print(f"verified {len(bank)} tasks")

if __name__ == "__main__":
    import json
    from pathlib import Path
    bank_path = Path(__file__).with_name("arc_puzzle_bank_next_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
